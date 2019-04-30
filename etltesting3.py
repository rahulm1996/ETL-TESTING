import sys
import cx_Oracle as db
import pandas as pd
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def vp_start_gui():
    
    global val, w, root,top
    root = tk.Tk()
    top = ETL (root)
#     root.wm_attributes('-alpha', 0.8)

    root.mainloop()

w = None

class ETL:
   
    def connectdatabase(self):
        
        global connection
        global cursor1
        global cursor2
        global cursor3
#         connection = db.connect(self.UserName.get()+'/'+self.Password.get()+'@'+self.IpAddressEntry.get()+':'+self.PortNo.get()+'/'+self.ServerName.get())
        connection = db.connect('T562829/T562829@10.123.79.59:1521/georli04')
        
    
        print('connected to database')
        
        
    def fetchTableDetails(self):
        try:
            print('fetchTableDetails')
            cursor1 = connection.cursor()
            cursor2 = connection.cursor()
            
            sourcet=cursor1.execute('select * from '+self.sourceTableEntry.get())
            targett=cursor2.execute('select * from '+self.targetTableEntry.get())
            sourcedf=pd.DataFrame(sourcet.fetchall())
            targetdf=pd.DataFrame(targett.fetchall())
            
            print('source',sourcedf)
            print('target',targetdf)
            global columnslist
            
            self.relationlop=['<','>','<=','=>','<>','=','LIKE']   
            self.conditionalop=['AND','OR']
            self.rrrr=["SUM","SPACE"] 
            columnslist=[i[0] for i in sourcet.description]
            self.columsList.insert(tk.END,*columnslist)
            self.Field1.configure(values=columnslist)
            self.Field2.configure(values=columnslist)
            self.Field3.configure(values=columnslist)
            self.Field4.configure(values=columnslist)
            
            self.Relation1.configure(values=self.relationlop)
            self.Relation2.configure(values=self.relationlop)
            self.Relation3.configure(values=self.relationlop)
            self.Relation4.configure(values=self.relationlop)
            
            self.Condition1.configure(values=self.conditionalop)
            self.Condition2.configure(values=self.conditionalop)
            self.Condition3.configure(values=self.conditionalop)
            self.Relation.configure(values=self.rrrr)
        except:
            self.Listbox1.insert(tk.END,"Enter Valid table Name") 
        
    def addcolumn(self):
        selec=[self.columsList.get(i) for i in self.columsList.curselection()]
        if(len(self.columsList.curselection())==1):
            self.selectedcolumns.append((",".join(selec)[0:]))
            
        elif(len(self.columsList.curselection())>1):
            
            
            if(self.vartest.get()==3 or self.vartest.get()==4):
                if(self.Relation.get()=="SPACE"):
                    s="("+("|| ' ' ||".join(selec)[0:])+")"
                    self.selectedcolumns.append(s+" AS "+self.AsEntry.get())
                elif(self.Relation.get()=="SUM"):
                    s="("+("+".join(selec)[0:])+")"
                    self.selectedcolumns.append(s+" AS "+self.AsEntry.get())     
        
        
    
    def testselected(self):
        
#         print(self.selectedcolumns,"jsiksjs")
        if(self.vartest.get()==1):
            return "COUNT("+(",".join(self.selectedcolumns)[0:])+")"
        if(self.vartest.get()==2):
            return "SUM("+(",".join(self.selectedcolumns)[0:])+")"
        if(self.vartest.get()==3):
            return ",".join(self.selectedcolumns)[0:]
        if(self.vartest.get()==4):
            return (",".join(self.selectedcolumns)[0:])
    def conditions(self):
        
        cond=self.Field1.get()+" "+self.Relation1.get()+" "+self.Value1.get()
        
        if(self.Condition1 is not None):
            cond+=" "+self.Condition1.get()+" "+self.Field2.get()+" "+self.Relation2.get()+" "+self.Value2.get()
        if(self.Condition2 is not None):
            cond+=" "+self.Condition2.get()+" "+self.Field3.get()+" "+self.Relation3.get()+" "+self.Value3.get()
        if(self.Condition3 is not None):
            cond+=" "+self.Condition3.get()+" "+self.Field4.get()+" "+self.Relation4.get()+" "+self.Value4.get()
        return cond     
            
    def genratequery(self):
        try:
            
            self.sqlsource="SELECT "+self.testselected()+" FROM "+self.sourceTableEntry.get()+" "+self.clause.get()+" "+self.conditions()
            
            self.sqltarget="SELECT "+self.testselected()+" FROM "+self.targetTableEntry.get()
            if(self.vartest.get()==3):
                self.sqltarget="SELECT * FROM "+self.targetTableEntry.get()
                self.sqlsource=self.sqlsource+" INTERSECT "+self.sqltarget
            elif(self.vartest.get()==4):
                self.sqltarget="SELECT * FROM "+self.targetTableEntry.get()
                self.sqlsource=self.sqlsource+" MINUS "+self.sqltarget
            print(self.sqlsource)
            print(self.sqltarget)
        except:
            self.Listbox1.insert(tk.END,"Invalid Inputs Or Conditions")
        
    def executequery(self): 
        
        cursor3 = connection.cursor()
        cursor4 = connection.cursor()
        if(self.vartest.get()==1 or self.vartest.get()==2):
            cursor3.execute(self.sqlsource)
            cursor4.execute(self.sqltarget)
            x=pd.Series(cursor3)
            y=pd.Series(cursor4)
            print('source Table Details\n',x)
            print('Target Table Details\n',y)
        
            if(x.equals(y)):
                print(True)
                self.Listbox1.insert(tk.END,"TRUE")
            else:
                print(False)
                self.Listbox1.insert(tk.END,"False")
                
        if(self.vartest.get()==3):
            
            cursor3.execute(self.sqlsource)
            cursor4.execute(self.sqltarget)
            x=pd.DataFrame(cursor3)
            y=pd.DataFrame(cursor4)
            print('source Table Details\n',x)
            print('Target Table Details\n',y)
            print(x.count())
            print(y.count())
            if(x.count().equals(y.count())):
                print(True)
                self.Listbox1.insert(tk.END,"TRUE")
            else:
                print(False)
                self.Listbox1.insert(tk.END,"False")
        if(self.vartest.get()==4):
            cursor3.execute(self.sqlsource)
            cursor4.execute(self.sqltarget)
            x=pd.DataFrame(cursor3)
            y=pd.DataFrame(cursor4)
            print('source Table Details\n',x)
            print('Target Table Details\n',y)
            
        
        
    
    def reset_window(self):   
        pass
    def __init__(self, top=None):
        self.selectedcolumns=[]
        
        self.vartest=tk.IntVar()
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
   # image = tk.PhotoImage(file="stonehenge_england_1024.png")
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("1280x720+-25+33")
        top.title("ETL Testing")
        top.configure(background="#d8d8d8")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.TestFrame = tk.Frame(top)
        self.TestFrame.place(relx=0.25, rely=0.292, relheight=0.16
                , relwidth=0.207)
        self.TestFrame.configure(relief='groove')
        self.TestFrame.configure(borderwidth="2")
        self.TestFrame.configure(relief="groove")
        self.TestFrame.configure(background="#d9d9d9")
        self.TestFrame.configure(highlightbackground="#d9d9d9")
        self.TestFrame.configure(highlightcolor="black")
        self.TestFrame.configure(width=265)

        self.TestType = tk.Label(self.TestFrame)
        self.TestType.place(relx=0.038, rely=0.087, height=26, width=72)
        self.TestType.configure(activebackground="#f9f9f9")
        self.TestType.configure(activeforeground="black")
        self.TestType.configure(background="#d9d9d9")
        self.TestType.configure(disabledforeground="#a3a3a3")
        self.TestType.configure(foreground="#000000")
        self.TestType.configure(highlightbackground="#d9d9d9")
        self.TestType.configure(highlightcolor="black")
        self.TestType.configure(text='''Test Type''')

        self.count = tk.Radiobutton(self.TestFrame)
        self.count.place(relx=0.34, rely=0.087, relheight=0.217, relwidth=0.23)
        self.count.configure(activebackground="#ececec")
        self.count.configure(activeforeground="#000000")
        self.count.configure(background="#d9d9d9")
        self.count.configure(disabledforeground="#a3a3a3")
        self.count.configure(foreground="#000000")
        self.count.configure(highlightbackground="#d9d9d9")
        self.count.configure(highlightcolor="black")
        self.count.configure(justify='left')
        self.count.configure(text='''Count''')
        self.count.configure(variable=self.vartest,value=1,command=self.testselected)

        self.checkSum = tk.Radiobutton(self.TestFrame)
        self.checkSum.place(relx=0.604, rely=0.087, relheight=0.217
                , relwidth=0.332)
        self.checkSum.configure(activebackground="#ececec")
        self.checkSum.configure(activeforeground="#000000")
        self.checkSum.configure(background="#d9d9d9")
        self.checkSum.configure(disabledforeground="#a3a3a3")
        self.checkSum.configure(foreground="#000000")
        self.checkSum.configure(highlightbackground="#d9d9d9")
        self.checkSum.configure(highlightcolor="black")
        self.checkSum.configure(justify='left')
        self.checkSum.configure(text='''Check Sum''')
        self.checkSum.configure(variable=self.vartest,value=2,command=self.testselected)
        
        self.matchTest = tk.Radiobutton(self.TestFrame)
        self.matchTest.place(relx=0.34, rely=0.348, relheight=0.217
                , relwidth=0.234)
        self.matchTest.configure(activebackground="#ececec")
        self.matchTest.configure(activeforeground="#000000")
        self.matchTest.configure(background="#d9d9d9")
        self.matchTest.configure(disabledforeground="#a3a3a3")
        self.matchTest.configure(foreground="#000000")
        self.matchTest.configure(highlightbackground="#d9d9d9")
        self.matchTest.configure(highlightcolor="black")
        self.matchTest.configure(justify='left')
        self.matchTest.configure(text='''Match''')
        self.matchTest.configure(variable=self.vartest,value=3,command=self.testselected)
        
        self.misMatch = tk.Radiobutton(self.TestFrame)
        self.misMatch.place(relx=0.604, rely=0.348, relheight=0.217
                , relwidth=0.306)
        self.misMatch.configure(activebackground="#ececec")
        self.misMatch.configure(activeforeground="#000000")
        self.misMatch.configure(background="#d9d9d9")
        self.misMatch.configure(disabledforeground="#a3a3a3")
        self.misMatch.configure(foreground="#000000")
        self.misMatch.configure(highlightbackground="#d9d9d9")
        self.misMatch.configure(highlightcolor="black")
        self.misMatch.configure(justify='left')
        self.misMatch.configure(text='''MisMatch''')
        self.misMatch.configure(variable=self.vartest,value=4,command=self.testselected)
        
#         self.setTestTypeButton = tk.Button(self.TestFrame)
#         self.setTestTypeButton.place(relx=0.34, rely=0.696, height=24, width=81)
#         self.setTestTypeButton.configure(activebackground="#ececec")
#         self.setTestTypeButton.configure(activeforeground="#000000")
#         self.setTestTypeButton.configure(background="#d9d9d9")
#         self.setTestTypeButton.configure(disabledforeground="#a3a3a3")
#         self.setTestTypeButton.configure(foreground="#000000")
#         self.setTestTypeButton.configure(highlightbackground="#d9d9d9")
#         self.setTestTypeButton.configure(highlightcolor="black")
#         self.setTestTypeButton.configure(pady="0")
#         self.setTestTypeButton.configure(text='''Set Test Type''')
       
        
        self.TableFrame = tk.Frame(top)
        self.TableFrame.place(relx=0.25, rely=0.056, relheight=0.188
                , relwidth=0.207)
        self.TableFrame.configure(relief='groove')
        self.TableFrame.configure(borderwidth="2")
        self.TableFrame.configure(relief="groove")
        self.TableFrame.configure(background="#d9d9d9")
        self.TableFrame.configure(highlightbackground="#d9d9d9")
        self.TableFrame.configure(highlightcolor="black")
        self.TableFrame.configure(width=265)

        self.SourceTable = tk.Label(self.TableFrame)
        self.SourceTable.place(relx=0.075, rely=0.148, height=21, width=74)
        self.SourceTable.configure(activebackground="#f9f9f9")
        self.SourceTable.configure(activeforeground="black")
        self.SourceTable.configure(background="#d9d9d9")
        self.SourceTable.configure(disabledforeground="#a3a3a3")
        self.SourceTable.configure(foreground="#000000")
        self.SourceTable.configure(highlightbackground="#d9d9d9")
        self.SourceTable.configure(highlightcolor="black")
        self.SourceTable.configure(text='''Source Table''')

        self.TargetTable = tk.Label(self.TableFrame)
        self.TargetTable.place(relx=0.075, rely=0.444, height=21, width=72)
        self.TargetTable.configure(activebackground="#f9f9f9")
        self.TargetTable.configure(activeforeground="black")
        self.TargetTable.configure(background="#d9d9d9")
        self.TargetTable.configure(disabledforeground="#a3a3a3")
        self.TargetTable.configure(foreground="#000000")
        self.TargetTable.configure(highlightbackground="#d9d9d9")
        self.TargetTable.configure(highlightcolor="black")
        self.TargetTable.configure(text='''Target Table''')

        self.sourceTableEntry = tk.Entry(self.TableFrame)
        self.sourceTableEntry.place(relx=0.453, rely=0.148, height=24
                , relwidth=0.468)
        self.sourceTableEntry.configure(background="white")
        self.sourceTableEntry.configure(disabledforeground="#a3a3a3")
        self.sourceTableEntry.configure(font="TkFixedFont")
        self.sourceTableEntry.configure(foreground="#000000")
        self.sourceTableEntry.configure(highlightbackground="#d9d9d9")
        self.sourceTableEntry.configure(highlightcolor="black")
        self.sourceTableEntry.configure(insertbackground="black")
        self.sourceTableEntry.configure(selectbackground="#c4c4c4")
        self.sourceTableEntry.configure(selectforeground="black")

        self.targetTableEntry = tk.Entry(self.TableFrame)
        self.targetTableEntry.place(relx=0.453, rely=0.444, height=24
                , relwidth=0.468)
        self.targetTableEntry.configure(background="white")
        self.targetTableEntry.configure(disabledforeground="#a3a3a3")
        self.targetTableEntry.configure(font="TkFixedFont")
        self.targetTableEntry.configure(foreground="#000000")
        self.targetTableEntry.configure(highlightbackground="#d9d9d9")
        self.targetTableEntry.configure(highlightcolor="black")
        self.targetTableEntry.configure(insertbackground="black")
        self.targetTableEntry.configure(selectbackground="#c4c4c4")
        self.targetTableEntry.configure(selectforeground="black")

        self.TableFetchButton = tk.Button(self.TableFrame)
        self.TableFetchButton.place(relx=0.34, rely=0.741, height=24, width=79)
        self.TableFetchButton.configure(activebackground="#ececec")
        self.TableFetchButton.configure(activeforeground="#000000")
        self.TableFetchButton.configure(background="#d9d9d9")
        self.TableFetchButton.configure(disabledforeground="#a3a3a3")
        self.TableFetchButton.configure(foreground="#000000")
        self.TableFetchButton.configure(highlightbackground="#d9d9d9")
        self.TableFetchButton.configure(highlightcolor="black")
        self.TableFetchButton.configure(command=self.fetchTableDetails,pady="0")
        self.TableFetchButton.configure(text='''Select Tables''')

        self.ClauseFrame = tk.Frame(top)
        self.ClauseFrame.place(relx=0.492, rely=0.056, relheight=0.396, relwidth=0.395)
        self.ClauseFrame.configure(relief='groove')
        self.ClauseFrame.configure(borderwidth="2")
        self.ClauseFrame.configure(relief="groove")
        self.ClauseFrame.configure(background="#d9d9d9")
        self.ClauseFrame.configure(highlightbackground="#d9d9d9")
        self.ClauseFrame.configure(highlightcolor="black")
        self.ClauseFrame.configure(width=265)

        self.Clause = tk.Label(self.ClauseFrame)
        self.Clause.place(relx=0.04, rely=0.842, height=21, width=41)
        self.Clause.configure(activebackground="#f9f9f9")
        self.Clause.configure(activeforeground="black")
        self.Clause.configure(background="#d9d9d9")
        self.Clause.configure(disabledforeground="#a3a3a3")
        self.Clause.configure(foreground="#000000")
        self.Clause.configure(highlightbackground="#d9d9d9")
        self.Clause.configure(highlightcolor="black")
        self.Clause.configure(text='''Clause''')

        self.clause = ttk.Combobox(self.ClauseFrame)
        self.clause.place(relx=0.198, rely=0.842, relheight=0.091
                , relwidth=0.251)
        self.clause.configure(foreground="#000000")
        self.clause.configure(takefocus="")
        self.clause.configure(values=['WHERE','HAVING'])

        self.Columns = tk.Label(self.ClauseFrame)
        self.Columns.place(relx=0.04, rely=0.105, height=21, width=54)
        self.Columns.configure(activebackground="#f9f9f9")
        self.Columns.configure(activeforeground="black")
        self.Columns.configure(background="#d9d9d9")
        self.Columns.configure(disabledforeground="#a3a3a3")
        self.Columns.configure(foreground="#000000")
        self.Columns.configure(highlightbackground="#d9d9d9")
        self.Columns.configure(highlightcolor="black")
        self.Columns.configure(text='''Columns''')

        self.columsList = tk.Listbox(self.ClauseFrame)
        self.columsList.place(relx=0.198, rely=0.105, relheight=0.519
                , relwidth=0.246)
        self.columsList.configure(background="white")
        self.columsList.configure(disabledforeground="#a3a3a3")
        self.columsList.configure(font="TkFixedFont")
        self.columsList.configure(foreground="#000000")
        self.columsList.configure(highlightbackground="#d9d9d9")
        self.columsList.configure(highlightcolor="black")
        self.columsList.configure(selectbackground="#c4c4c4")
        self.columsList.configure(selectforeground="black")
        self.columsList.configure(selectmode='multiple')
        self.columsList.configure(takefocus="0")
        self.columsList.configure(width=124)
        self.columsList.insert(tk.END,"*")
 
 
        self.RelationLabel = tk.Label(self.ClauseFrame)
        self.RelationLabel.place(relx=0.515, rely=0.105, height=21, width=49)
        self.RelationLabel.configure(background="#d9d9d9")
        self.RelationLabel.configure(disabledforeground="#a3a3a3")
        self.RelationLabel.configure(foreground="#000000")
        self.RelationLabel.configure(text='''Operator''')
        
        self.Relation = ttk.Combobox(self.ClauseFrame)
        self.Relation.place(relx=0.653, rely=0.105, relheight=0.074
                  , relwidth=0.244)
        self.Relation.configure(width=123)
        self.Relation.configure(takefocus="")
   
        self.AsLabel = tk.Label(self.ClauseFrame)
        self.AsLabel.place(relx=0.515, rely=0.386, height=21, width=20)
        self.AsLabel.configure(background="#d9d9d9")
        self.AsLabel.configure(disabledforeground="#a3a3a3")
        self.AsLabel.configure(foreground="#000000")
        self.AsLabel.configure(text='''AS''')
        
        self.AsEntry = tk.Entry(self.ClauseFrame)
        self.AsEntry.place(relx=0.653, rely=0.386,height=20, relwidth=0.246)
        self.AsEntry.configure(background="white")
        self.AsEntry.configure(disabledforeground="#a3a3a3")
        self.AsEntry.configure(font="TkFixedFont")
        self.AsEntry.configure(foreground="#000000")
        self.AsEntry.configure(insertbackground="black")
        self.AsEntry.configure(width=124)

        self.SelectColumns = tk.Button(self.ClauseFrame)
        self.SelectColumns.place(relx=0.198, rely=0.702, height=24, width=93)
        self.SelectColumns.configure(activebackground="#ececec")
        self.SelectColumns.configure(activeforeground="#000000")
        self.SelectColumns.configure(background="#d9d9d9")
        self.SelectColumns.configure(disabledforeground="#a3a3a3")
        self.SelectColumns.configure(foreground="#000000")
        self.SelectColumns.configure(highlightbackground="#d9d9d9")
        self.SelectColumns.configure(highlightcolor="black")
        self.SelectColumns.configure(command=self.addcolumn,pady="0")
        self.SelectColumns.configure(text='''Select Columns''')

        self.GenrateButton = tk.Button(top)
        self.GenrateButton.place(relx=0.398, rely=0.806, height=24, width=87)
        self.GenrateButton.configure(activebackground="#ececec")
        self.GenrateButton.configure(activeforeground="#000000")
        self.GenrateButton.configure(background="#d9d9d9")
        self.GenrateButton.configure(disabledforeground="#a3a3a3")
        self.GenrateButton.configure(foreground="#000000")
        self.GenrateButton.configure(highlightbackground="#d9d9d9")
        self.GenrateButton.configure(highlightcolor="black")
        self.GenrateButton.configure(command=self.genratequery,pady="0")
        self.GenrateButton.configure(text='''Genrate Query''')

        self.ConditionFrame = tk.Frame(top)
        self.ConditionFrame.place(relx=0.023, rely=0.5, relheight=0.257
                , relwidth=0.957)
        self.ConditionFrame.configure(relief='groove')
        self.ConditionFrame.configure(borderwidth="2")
        self.ConditionFrame.configure(relief="groove")
        self.ConditionFrame.configure(background="#d9d9d9")
        self.ConditionFrame.configure(highlightbackground="#d9d9d9")
        self.ConditionFrame.configure(highlightcolor="black")
        self.ConditionFrame.configure(width=1225)

        self.Conditionframe1 = tk.LabelFrame(self.ConditionFrame)
        self.Conditionframe1.place(relx=0.016, rely=0.108, relheight=0.73
                , relwidth=0.18)
        self.Conditionframe1.configure(relief='groove')
        self.Conditionframe1.configure(foreground="black")
        self.Conditionframe1.configure(text='''Condition 1''')
        self.Conditionframe1.configure(background="#d9d9d9")
        self.Conditionframe1.configure(highlightbackground="#d9d9d9")
        self.Conditionframe1.configure(highlightcolor="black")
        self.Conditionframe1.configure(width=220)

        self.Field1 = ttk.Combobox(self.Conditionframe1)
        self.Field1.place(relx=0.409, rely=0.222, relheight=0.193, relwidth=0.532
                , bordermode='ignore')
        self.Field1.configure(takefocus="")
        
        self.Relation1 = ttk.Combobox(self.Conditionframe1)
        self.Relation1.place(relx=0.409, rely=0.444, relheight=0.193
                , relwidth=0.532, bordermode='ignore')
        self.Relation1.configure(takefocus="")

        self.Value1 = tk.Entry(self.Conditionframe1)
        self.Value1.place(relx=0.409, rely=0.667, height=24, relwidth=0.518
                , bordermode='ignore')
        self.Value1.configure(background="white")
        self.Value1.configure(disabledforeground="#a3a3a3")
        self.Value1.configure(font="TkFixedFont")
        self.Value1.configure(foreground="#000000")
        self.Value1.configure(highlightbackground="#d9d9d9")
        self.Value1.configure(highlightcolor="black")
        self.Value1.configure(insertbackground="black")
        self.Value1.configure(selectbackground="#c4c4c4")
        self.Value1.configure(selectforeground="black")

        self.FieldLabel1 = tk.Label(self.Conditionframe1)
        self.FieldLabel1.place(relx=0.045, rely=0.222, height=21, width=37
                , bordermode='ignore')
        self.FieldLabel1.configure(activebackground="#f9f9f9")
        self.FieldLabel1.configure(activeforeground="black")
        self.FieldLabel1.configure(background="#d9d9d9")
        self.FieldLabel1.configure(disabledforeground="#a3a3a3")
        self.FieldLabel1.configure(foreground="#000000")
        self.FieldLabel1.configure(highlightbackground="#d9d9d9")
        self.FieldLabel1.configure(highlightcolor="black")
        self.FieldLabel1.configure(text='''Field1''')

        self.RelationLabel1 = tk.Label(self.Conditionframe1)
        self.RelationLabel1.place(relx=0.045, rely=0.444, height=21, width=55
                , bordermode='ignore')
        self.RelationLabel1.configure(activebackground="#f9f9f9")
        self.RelationLabel1.configure(activeforeground="black")
        self.RelationLabel1.configure(background="#d9d9d9")
        self.RelationLabel1.configure(disabledforeground="#a3a3a3")
        self.RelationLabel1.configure(foreground="#000000")
        self.RelationLabel1.configure(highlightbackground="#d9d9d9")
        self.RelationLabel1.configure(highlightcolor="black")
        self.RelationLabel1.configure(text='''Relation1''')

        self.ValueLabel1 = tk.Label(self.Conditionframe1)
        self.ValueLabel1.place(relx=0.045, rely=0.667, height=21, width=41
                , bordermode='ignore')
        self.ValueLabel1.configure(activebackground="#f9f9f9")
        self.ValueLabel1.configure(activeforeground="black")
        self.ValueLabel1.configure(background="#d9d9d9")
        self.ValueLabel1.configure(disabledforeground="#a3a3a3")
        self.ValueLabel1.configure(foreground="#000000")
        self.ValueLabel1.configure(highlightbackground="#d9d9d9")
        self.ValueLabel1.configure(highlightcolor="black")
        self.ValueLabel1.configure(text='''Value1''')

        self.Conditionframe2 = tk.LabelFrame(self.ConditionFrame)
        self.Conditionframe2.place(relx=0.278, rely=0.108, relheight=0.73
                , relwidth=0.18)
        self.Conditionframe2.configure(relief='groove')
        self.Conditionframe2.configure(foreground="black")
        self.Conditionframe2.configure(text='''Condition 2''')
        self.Conditionframe2.configure(background="#d9d9d9")
        self.Conditionframe2.configure(highlightbackground="#d9d9d9")
        self.Conditionframe2.configure(highlightcolor="black")
        self.Conditionframe2.configure(width=220)

        self.Field2 = ttk.Combobox(self.Conditionframe2)
        self.Field2.place(relx=0.409, rely=0.222, relheight=0.193, relwidth=0.532
                , bordermode='ignore')
        self.Field2.configure(takefocus="")

        self.Relation2 = ttk.Combobox(self.Conditionframe2)
        self.Relation2.place(relx=0.409, rely=0.444, relheight=0.193
                , relwidth=0.532, bordermode='ignore')
        self.Relation2.configure(takefocus="")

        self.Value2 = tk.Entry(self.Conditionframe2)
        self.Value2.place(relx=0.409, rely=0.667, height=24, relwidth=0.518
                , bordermode='ignore')
        self.Value2.configure(background="white")
        self.Value2.configure(disabledforeground="#a3a3a3")
        self.Value2.configure(font="TkFixedFont")
        self.Value2.configure(foreground="#000000")
        self.Value2.configure(highlightbackground="#d9d9d9")
        self.Value2.configure(highlightcolor="black")
        self.Value2.configure(insertbackground="black")
        self.Value2.configure(selectbackground="#c4c4c4")
        self.Value2.configure(selectforeground="black")

        self.FieldLabel2 = tk.Label(self.Conditionframe2)
        self.FieldLabel2.place(relx=0.045, rely=0.222, height=21, width=37
                , bordermode='ignore')
        self.FieldLabel2.configure(activebackground="#f9f9f9")
        self.FieldLabel2.configure(activeforeground="black")
        self.FieldLabel2.configure(background="#d9d9d9")
        self.FieldLabel2.configure(disabledforeground="#a3a3a3")
        self.FieldLabel2.configure(foreground="#000000")
        self.FieldLabel2.configure(highlightbackground="#d9d9d9")
        self.FieldLabel2.configure(highlightcolor="black")
        self.FieldLabel2.configure(text='''Field2''')

        self.RelationLabel2 = tk.Label(self.Conditionframe2)
        self.RelationLabel2.place(relx=0.045, rely=0.444, height=21, width=55
                , bordermode='ignore')
        self.RelationLabel2.configure(activebackground="#f9f9f9")
        self.RelationLabel2.configure(activeforeground="black")
        self.RelationLabel2.configure(background="#d9d9d9")
        self.RelationLabel2.configure(disabledforeground="#a3a3a3")
        self.RelationLabel2.configure(foreground="#000000")
        self.RelationLabel2.configure(highlightbackground="#d9d9d9")
        self.RelationLabel2.configure(highlightcolor="black")
        self.RelationLabel2.configure(text='''Relation2''')

        self.ValueLabel2 = tk.Label(self.Conditionframe2)
        self.ValueLabel2.place(relx=0.045, rely=0.667, height=21, width=41
                , bordermode='ignore')
        self.ValueLabel2.configure(activebackground="#f9f9f9")
        self.ValueLabel2.configure(activeforeground="black")
        self.ValueLabel2.configure(background="#d9d9d9")
        self.ValueLabel2.configure(disabledforeground="#a3a3a3")
        self.ValueLabel2.configure(foreground="#000000")
        self.ValueLabel2.configure(highlightbackground="#d9d9d9")
        self.ValueLabel2.configure(highlightcolor="black")
        self.ValueLabel2.configure(text='''Value2''')

        self.Conditionframe3 = tk.LabelFrame(self.ConditionFrame)
        self.Conditionframe3.place(relx=0.539, rely=0.108, relheight=0.73
                , relwidth=0.18)
        self.Conditionframe3.configure(relief='groove')
        self.Conditionframe3.configure(foreground="black")
        self.Conditionframe3.configure(text='''Condition 3''')
        self.Conditionframe3.configure(background="#d9d9d9")
        self.Conditionframe3.configure(highlightbackground="#d9d9d9")
        self.Conditionframe3.configure(highlightcolor="black")
        self.Conditionframe3.configure(width=220)

        self.Field3 = ttk.Combobox(self.Conditionframe3)
        self.Field3.place(relx=0.409, rely=0.222, relheight=0.193, relwidth=0.532
                , bordermode='ignore')
        self.Field3.configure(takefocus="")

        self.Relation3 = ttk.Combobox(self.Conditionframe3)
        self.Relation3.place(relx=0.409, rely=0.444, relheight=0.193
                , relwidth=0.532, bordermode='ignore')
        self.Relation3.configure(takefocus="")

        self.Value3 = tk.Entry(self.Conditionframe3)
        self.Value3.place(relx=0.409, rely=0.667, height=24, relwidth=0.518
                , bordermode='ignore')
        self.Value3.configure(background="white")
        self.Value3.configure(disabledforeground="#a3a3a3")
        self.Value3.configure(font="TkFixedFont")
        self.Value3.configure(foreground="#000000")
        self.Value3.configure(highlightbackground="#d9d9d9")
        self.Value3.configure(highlightcolor="black")
        self.Value3.configure(insertbackground="black")
        self.Value3.configure(selectbackground="#c4c4c4")
        self.Value3.configure(selectforeground="black")

        self.FieldLabel3 = tk.Label(self.Conditionframe3)
        self.FieldLabel3.place(relx=0.045, rely=0.222, height=21, width=37
                , bordermode='ignore')
        self.FieldLabel3.configure(activebackground="#f9f9f9")
        self.FieldLabel3.configure(activeforeground="black")
        self.FieldLabel3.configure(background="#d9d9d9")
        self.FieldLabel3.configure(disabledforeground="#a3a3a3")
        self.FieldLabel3.configure(foreground="#000000")
        self.FieldLabel3.configure(highlightbackground="#d9d9d9")
        self.FieldLabel3.configure(highlightcolor="black")
        self.FieldLabel3.configure(text='''Field3''')

        self.RelationLabel3 = tk.Label(self.Conditionframe3)
        self.RelationLabel3.place(relx=0.045, rely=0.444, height=21, width=55
                , bordermode='ignore')
        self.RelationLabel3.configure(activebackground="#f9f9f9")
        self.RelationLabel3.configure(activeforeground="black")
        self.RelationLabel3.configure(background="#d9d9d9")
        self.RelationLabel3.configure(disabledforeground="#a3a3a3")
        self.RelationLabel3.configure(foreground="#000000")
        self.RelationLabel3.configure(highlightbackground="#d9d9d9")
        self.RelationLabel3.configure(highlightcolor="black")
        self.RelationLabel3.configure(text='''Relation3''')

        self.ValueLabel3 = tk.Label(self.Conditionframe3)
        self.ValueLabel3.place(relx=0.045, rely=0.667, height=21, width=41
                , bordermode='ignore')
        self.ValueLabel3.configure(activebackground="#f9f9f9")
        self.ValueLabel3.configure(activeforeground="black")
        self.ValueLabel3.configure(background="#d9d9d9")
        self.ValueLabel3.configure(disabledforeground="#a3a3a3")
        self.ValueLabel3.configure(foreground="#000000")
        self.ValueLabel3.configure(highlightbackground="#d9d9d9")
        self.ValueLabel3.configure(highlightcolor="black")
        self.ValueLabel3.configure(text='''Value3''')

        self.Conditionframe4 = tk.LabelFrame(self.ConditionFrame)
        self.Conditionframe4.place(relx=0.8, rely=0.108, relheight=0.73
                , relwidth=0.18)
        self.Conditionframe4.configure(relief='groove')
        self.Conditionframe4.configure(foreground="black")
        self.Conditionframe4.configure(text='''Condition 4''')
        self.Conditionframe4.configure(background="#d9d9d9")
        self.Conditionframe4.configure(highlightbackground="#d9d9d9")
        self.Conditionframe4.configure(highlightcolor="black")
        self.Conditionframe4.configure(width=220)

        self.Field4 = ttk.Combobox(self.Conditionframe4)
        self.Field4.place(relx=0.409, rely=0.222, relheight=0.193, relwidth=0.532
                , bordermode='ignore')
        self.Field4.configure(takefocus="")

        self.Relation4 = ttk.Combobox(self.Conditionframe4)
        self.Relation4.place(relx=0.409, rely=0.444, relheight=0.193
                , relwidth=0.532, bordermode='ignore')
        self.Relation4.configure(takefocus="")

        self.Value4 = tk.Entry(self.Conditionframe4)
        self.Value4.place(relx=0.409, rely=0.667, height=24, relwidth=0.518
                , bordermode='ignore')
        self.Value4.configure(background="white")
        self.Value4.configure(disabledforeground="#a3a3a3")
        self.Value4.configure(font="TkFixedFont")
        self.Value4.configure(foreground="#000000")
        self.Value4.configure(highlightbackground="#d9d9d9")
        self.Value4.configure(highlightcolor="black")
        self.Value4.configure(insertbackground="black")
        self.Value4.configure(selectbackground="#c4c4c4")
        self.Value4.configure(selectforeground="black")

        self.FieldLabel4 = tk.Label(self.Conditionframe4)
        self.FieldLabel4.place(relx=0.045, rely=0.222, height=21, width=37
                , bordermode='ignore')
        self.FieldLabel4.configure(activebackground="#f9f9f9")
        self.FieldLabel4.configure(activeforeground="black")
        self.FieldLabel4.configure(background="#d9d9d9")
        self.FieldLabel4.configure(disabledforeground="#a3a3a3")
        self.FieldLabel4.configure(foreground="#000000")
        self.FieldLabel4.configure(highlightbackground="#d9d9d9")
        self.FieldLabel4.configure(highlightcolor="black")
        self.FieldLabel4.configure(text='''Field4''')

        self.RelationLabel4 = tk.Label(self.Conditionframe4)
        self.RelationLabel4.place(relx=0.045, rely=0.444, height=21, width=55
                , bordermode='ignore')
        self.RelationLabel4.configure(activebackground="#f9f9f9")
        self.RelationLabel4.configure(activeforeground="black")
        self.RelationLabel4.configure(background="#d9d9d9")
        self.RelationLabel4.configure(disabledforeground="#a3a3a3")
        self.RelationLabel4.configure(foreground="#000000")
        self.RelationLabel4.configure(highlightbackground="#d9d9d9")
        self.RelationLabel4.configure(highlightcolor="black")
        self.RelationLabel4.configure(text='''Relation4''')

        self.ValueLabel4 = tk.Label(self.Conditionframe4)
        self.ValueLabel4.place(relx=0.045, rely=0.667, height=21, width=41
                , bordermode='ignore')
        self.ValueLabel4.configure(activebackground="#f9f9f9")
        self.ValueLabel4.configure(activeforeground="black")
        self.ValueLabel4.configure(background="#d9d9d9")
        self.ValueLabel4.configure(disabledforeground="#a3a3a3")
        self.ValueLabel4.configure(foreground="#000000")
        self.ValueLabel4.configure(highlightbackground="#d9d9d9")
        self.ValueLabel4.configure(highlightcolor="black")
        self.ValueLabel4.configure(text='''Value4''')

        self.Condition1 = ttk.Combobox(self.ConditionFrame)
        self.Condition1.place(relx=0.204, rely=0.432, relheight=0.141
                , relwidth=0.063)
        self.Condition1.configure(takefocus="")

        self.Condition2 = ttk.Combobox(self.ConditionFrame)
        self.Condition2.place(relx=0.465, rely=0.432, relheight=0.141
                , relwidth=0.063)
        self.Condition2.configure(takefocus="")

        self.Condition3 = ttk.Combobox(self.ConditionFrame)
        self.Condition3.place(relx=0.727, rely=0.432, relheight=0.141
                , relwidth=0.063)
        self.Condition3.configure(takefocus="")

        self.ExecuteButton = tk.Button(top)
        self.ExecuteButton.place(relx=0.398, rely=0.903, height=24, width=86)
        self.ExecuteButton.configure(activebackground="#ececec")
        self.ExecuteButton.configure(activeforeground="#000000")
        self.ExecuteButton.configure(background="#d9d9d9")
        self.ExecuteButton.configure(disabledforeground="#a3a3a3")
        self.ExecuteButton.configure(foreground="#000000")
        self.ExecuteButton.configure(highlightbackground="#d9d9d9")
        self.ExecuteButton.configure(highlightcolor="black")
        self.ExecuteButton.configure(command=self.executequery,pady="0")
        self.ExecuteButton.configure(text='''Execute Query''')

        self.DatabaseConnection = tk.LabelFrame(top)
        self.DatabaseConnection.place(relx=0.023, rely=0.042, relheight=0.41
                , relwidth=0.203)
        self.DatabaseConnection.configure(relief='groove')
        self.DatabaseConnection.configure(foreground="black")
        self.DatabaseConnection.configure(text='''Database Connection''')
        self.DatabaseConnection.configure(background="#d9d9d9")
        self.DatabaseConnection.configure(highlightbackground="#d9d9d9")
        self.DatabaseConnection.configure(highlightcolor="black")
        self.DatabaseConnection.configure(width=260)

        self.Ip = tk.Label(self.DatabaseConnection)
        self.Ip.place(relx=0.038, rely=0.136, height=21, width=61
                , bordermode='ignore')
        self.Ip.configure(activebackground="#f9f9f9")
        self.Ip.configure(activeforeground="black")
        self.Ip.configure(background="#d9d9d9")
        self.Ip.configure(disabledforeground="#a3a3a3")
        self.Ip.configure(foreground="#000000")
        self.Ip.configure(highlightbackground="#d9d9d9")
        self.Ip.configure(highlightcolor="black")
        self.Ip.configure(text='''IP Address''')

        self.Port = tk.Label(self.DatabaseConnection)
        self.Port.place(relx=0.038, rely=0.237, height=21, width=50
                , bordermode='ignore')
        self.Port.configure(activebackground="#f9f9f9")
        self.Port.configure(activeforeground="black")
        self.Port.configure(background="#d9d9d9")
        self.Port.configure(disabledforeground="#a3a3a3")
        self.Port.configure(foreground="#000000")
        self.Port.configure(highlightbackground="#d9d9d9")
        self.Port.configure(highlightcolor="black")
        self.Port.configure(text='''Port No.''')

        self.Server = tk.Label(self.DatabaseConnection)
        self.Server.place(relx=0.038, rely=0.339, height=21, width=73
                , bordermode='ignore')
        self.Server.configure(activebackground="#f9f9f9")
        self.Server.configure(activeforeground="black")
        self.Server.configure(background="#d9d9d9")
        self.Server.configure(disabledforeground="#a3a3a3")
        self.Server.configure(foreground="#000000")
        self.Server.configure(highlightbackground="#d9d9d9")
        self.Server.configure(highlightcolor="black")
        self.Server.configure(text='''Server Name''')

        self.User = tk.Label(self.DatabaseConnection)
        self.User.place(relx=0.038, rely=0.441, height=21, width=59
                , bordermode='ignore')
        self.User.configure(activebackground="#f9f9f9")
        self.User.configure(activeforeground="black")
        self.User.configure(background="#d9d9d9")
        self.User.configure(disabledforeground="#a3a3a3")
        self.User.configure(foreground="#000000")
        self.User.configure(highlightbackground="#d9d9d9")
        self.User.configure(highlightcolor="black")
        self.User.configure(text='''Username''')

        self.Pass = tk.Label(self.DatabaseConnection)
        self.Pass.place(relx=0.038, rely=0.542, height=21, width=56
                , bordermode='ignore')
        self.Pass.configure(activebackground="#f9f9f9")
        self.Pass.configure(activeforeground="black")
        self.Pass.configure(background="#d9d9d9")
        self.Pass.configure(disabledforeground="#a3a3a3")
        self.Pass.configure(foreground="#000000")
        self.Pass.configure(highlightbackground="#d9d9d9")
        self.Pass.configure(highlightcolor="black")
        self.Pass.configure(text='''Password''')

        self.IpAddressEntry = tk.Entry(self.DatabaseConnection)
        self.IpAddressEntry.place(relx=0.462, rely=0.136, height=24
                , relwidth=0.477, bordermode='ignore')
        self.IpAddressEntry.configure(background="white")
        self.IpAddressEntry.configure(disabledforeground="#a3a3a3")
        self.IpAddressEntry.configure(font="TkFixedFont")
        self.IpAddressEntry.configure(foreground="#000000")
        self.IpAddressEntry.configure(highlightbackground="#d9d9d9")
        self.IpAddressEntry.configure(highlightcolor="black")
        self.IpAddressEntry.configure(insertbackground="black")
        self.IpAddressEntry.configure(selectbackground="#c4c4c4")
        self.IpAddressEntry.configure(selectforeground="black")

        self.PortNo = tk.Entry(self.DatabaseConnection)
        self.PortNo.place(relx=0.462, rely=0.237, height=24, relwidth=0.477
                , bordermode='ignore')
        self.PortNo.configure(background="white")
        self.PortNo.configure(disabledforeground="#a3a3a3")
        self.PortNo.configure(font="TkFixedFont")
        self.PortNo.configure(foreground="#000000")
        self.PortNo.configure(highlightbackground="#d9d9d9")
        self.PortNo.configure(highlightcolor="black")
        self.PortNo.configure(insertbackground="black")
        self.PortNo.configure(selectbackground="#c4c4c4")
        self.PortNo.configure(selectforeground="black")

        self.ServerName = tk.Entry(self.DatabaseConnection)
        self.ServerName.place(relx=0.462, rely=0.339, height=24, relwidth=0.477
                , bordermode='ignore')
        self.ServerName.configure(background="white")
        self.ServerName.configure(disabledforeground="#a3a3a3")
        self.ServerName.configure(font="TkFixedFont")
        self.ServerName.configure(foreground="#000000")
        self.ServerName.configure(highlightbackground="#d9d9d9")
        self.ServerName.configure(highlightcolor="black")
        self.ServerName.configure(insertbackground="black")
        self.ServerName.configure(selectbackground="#c4c4c4")
        self.ServerName.configure(selectforeground="black")

        self.UserName = tk.Entry(self.DatabaseConnection)
        self.UserName.place(relx=0.462, rely=0.441, height=24, relwidth=0.477
                , bordermode='ignore')
        self.UserName.configure(background="white")
        self.UserName.configure(disabledforeground="#a3a3a3")
        self.UserName.configure(font="TkFixedFont")
        self.UserName.configure(foreground="#000000")
        self.UserName.configure(highlightbackground="#d9d9d9")
        self.UserName.configure(highlightcolor="black")
        self.UserName.configure(insertbackground="black")
        self.UserName.configure(selectbackground="#c4c4c4")
        self.UserName.configure(selectforeground="black")

        self.Password = tk.Entry(self.DatabaseConnection)
        self.Password.place(relx=0.462, rely=0.542, height=24, relwidth=0.477
                , bordermode='ignore')
        self.Password.configure(background="white")
        self.Password.configure(disabledforeground="#a3a3a3")
        self.Password.configure(font="TkFixedFont")
        self.Password.configure(foreground="#000000")
        self.Password.configure(highlightbackground="#d9d9d9")
        self.Password.configure(highlightcolor="black")
        self.Password.configure(insertbackground="black")
        self.Password.configure(selectbackground="#c4c4c4")
        self.Password.configure(selectforeground="black")

        self.Connect = tk.Button(self.DatabaseConnection)
        self.Connect.place(relx=0.346, rely=0.847, height=24, width=56
                , bordermode='ignore')
        self.Connect.configure(activebackground="#ececec")
        self.Connect.configure(activeforeground="#000000")
        self.Connect.configure(background="#d9d9d9")
        self.Connect.configure(disabledforeground="#a3a3a3")
        self.Connect.configure(foreground="#000000")
        self.Connect.configure(highlightbackground="#d9d9d9")
        self.Connect.configure(highlightcolor="black")
        self.Connect.configure(command=self.connectdatabase,pady="0")
        self.Connect.configure(text='''Connect''')

        self.Listbox1 = tk.Listbox(top)
        self.Listbox1.place(relx=0.023, rely=0.806, relheight=0.142
                , relwidth=0.363)
        self.Listbox1.configure(background="white")
        self.Listbox1.configure(disabledforeground="#a3a3a3")
        self.Listbox1.configure(font="TkFixedFont")
        self.Listbox1.configure(foreground="#000000")
        self.Listbox1.configure(highlightbackground="#d9d9d9")
        self.Listbox1.configure(highlightcolor="black")
        self.Listbox1.configure(selectbackground="#c4c4c4")
        self.Listbox1.configure(selectforeground="black")
        self.Listbox1.configure(width=464)
        self.Listbox1.insert(tk.END,"RESULTS")

        
        
        self.ResetButton = tk.Button(top)
        self.ResetButton.place(relx=0.93, rely=0.903, height=24, width=39)
        self.ResetButton.configure(activebackground="#ececec")
        self.ResetButton.configure(activeforeground="#000000")
        self.ResetButton.configure(background="#d9d9d9")
        self.ResetButton.configure(disabledforeground="#a3a3a3")
        self.ResetButton.configure(foreground="#000000")
        self.ResetButton.configure(highlightbackground="#d9d9d9")
        self.ResetButton.configure(highlightcolor="black")
        self.ResetButton.configure(command=self.reset_window,pady="0")
        self.ResetButton.configure(text='''Reset''')
        

if __name__ == '__main__':
    vp_start_gui()





