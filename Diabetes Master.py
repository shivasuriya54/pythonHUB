from tkinter import *
from PIL import Image,ImageTk
import pickle
import sklearn
import sqlite3
import time
import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from tkinter import messagebox as ms
import re


model=pickle.load(open("diabetes.pkl","rb"))

print("*************************** APP IS RUNNING PLEASE DON'T CLOSE THIS WINDOW  ********************************")
app=Tk()
app.title("Diabetes Prediction App")
app.geometry("400x175")
app.resizable(width=False,height=False)
app.configure(background="skyblue")

bg_image=Image.open("sign.jpg")
test_img=ImageTk.PhotoImage(bg_image)

bg_image1=Image.open("symptoms1.jpg")
test_img1=ImageTk.PhotoImage(bg_image1)

bg_image2=Image.open("search.jpeg")
test_img2=ImageTk.PhotoImage(bg_image2)

bg_image10=Image.open("healthy1.jpg")
test_img10=ImageTk.PhotoImage(bg_image10)

bg_image11=Image.open("unhealthy1.jpg")
test_img11=ImageTk.PhotoImage(bg_image11)

bg_image5=Image.open("dia.png")
test_img5=ImageTk.PhotoImage(bg_image5)

bg_image6=Image.open("sign1.jpg")
test_img6=ImageTk.PhotoImage(bg_image6)


e = 'T'+datetime.datetime.now().strftime('%d%m%y')

dbase=sqlite3.connect("'Diabetes_det.db")

##dbase.execute('''CREATE TABLE IF NOT EXISTS
##               DIABETES(
##               ID INTEGER PRIMARY KEY AUTOINCREMENT,
##               GLUCOSE TEXT NOT NULL,
##               BLOODPRESSURE TEXT NOT NULL,
##               SKINTHICKNESS TEXT NOT NULL,
##               INSULIN TEXT NOT NULL,
##               BMI TEXT NOT NULL,
##               DIABETES_PED_FUN TEXT NOT NULL,
##               AGE TEXT NOT NULL,
##               PREDICTED_RESULT TEXT NOT NULL)''')



cur=dbase.cursor()

dbase.execute('''CREATE TABLE IF NOT EXISTS
                REG(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME TEXT NOT NULL,
                    USERNAME TEXT UNIQUE,
                    PASSWORD TEXT NOT NULL,
                    MOBILE_NUMBER INTEGER UNIQUE)''')

username1=StringVar()
password1=StringVar()
def log():
    global newWindow6
    newWindow6=Toplevel(app)
    newWindow6.title("login page")
    newWindow6.geometry("900x400")
    newWindow6.configure(background='light yellow')
    bg_lb5=Label(newWindow6,image=test_img5)
    bg_lb5.place(x=0,y=0,relwidth=1,relheight=1)
    newWindow6.resizable(width=False,height=False)
    def login():
        cur=dbase.cursor()
        usernameval=username1.get()
        passwordval=password1.get()
         
        if usernameval and passwordval:
            cur.execute("SELECT * FROM REG WHERE USERNAME=? AND PASSWORD=?",(usernameval,passwordval))
            data=cur.fetchone()
            if data:
                ms.showinfo("SUCCESS","YOU HAVE LOGIN SUCESSFULLY")
                #pred()
                mainapp()
            else:
                ms.showinfo("ERROR","INVALID USERNAME OR PASSWORD")
        else:
            ms.showinfo("ERROR","FILL ALL DATA")
            ent1.delete(first=0,last=END)
            ent2.delete(first=0,last=END)
    name=StringVar()     
    username=StringVar()
    password=StringVar()
    confirmpassword=StringVar()
    mobile=StringVar()
    def signup():    
        newWindow3=Toplevel(app)
        newWindow3.title("signup page")
        newWindow3.geometry("800x500")
        newWindow3.configure(background='light yellow')

        bg_lb6=Label(newWindow3,image=test_img6)
        bg_lb6.place(x=0,y=0,relwidth=1,relheight=1)
        newWindow3.resizable(width=False,height=False)



        def submit():
            nameval=ent1.get()
            usernameval=ent2.get()
            passwordval=ent3.get()
            confirm_passwordval=ent4.get()
            mobileval=ent5.get()
          
            if nameval and usernameval and passwordval and confirm_passwordval and mobileval:
                
                if passwordval==confirm_passwordval:
                    
                    dbase.execute("INSERT INTO REG(NAME,USERNAME,PASSWORD,MOBILE_NUMBER) VALUES(?,?,?,?)",(nameval,usernameval,passwordval,mobileval))
                    
                    dbase.commit()
                    ms.showinfo("SUCCESS","YOUR ACCOUNT CREATED SUCESSFULLY")
                    ent1.delete(first=0,last=END)
                    ent2.delete(first=0,last=END)
                    ent3.delete(first=0,last=END)
                    ent4.delete(first=0,last=END)
                    newWindow3.destroy()
                else:
                    ms.showinfo("ERROR","PASSWORD DON'T MATCH")
            else:
                ms.showinfo("ERROR","FILL ALL DATA")
##
##            except sqlite3.IntegrityError as s:
##                ms.showinfo("ERROR","USERNAME ALREADY EXISTS")
               


        lb1=Label(newWindow3,text="NAME:",font=("ALGERIAN",26),bg="#106394",fg="white",relief=RAISED)
        lb1.grid(row=0,column=0,padx=15,pady=15)
        ent1=Entry(newWindow3,font=("AREIAL",26),bg="white",fg="black",textvariable=name,relief=RAISED)
        ent1.grid(row=0,column=1,padx=15,pady=15)
        lb2=Label(newWindow3,text="USERNAME:",font=("ALGERIAN",26),bg="#106394",fg="white",relief=RAISED)
        lb2.grid(row=1,column=0,padx=15,pady=15)
        ent2=Entry(newWindow3,font=("AREIAL",26),bg="white",fg="black",textvariable=username,relief=RAISED)
        ent2.grid(row=1,column=1,padx=15,pady=15)
        lb3=Label(newWindow3,text="PASSWORD:",font=("ALGERIAN",26),bg="#106394",fg="white",relief=RAISED)
        lb3.grid(row=2,column=0,padx=15,pady=15)
        ent3=Entry(newWindow3, show="*",font=("AREIAL",26),bg="white",fg="black",textvariable=password,relief=RAISED)
        ent3.grid(row=2,column=1,padx=15,pady=15)    
        lb4=Label(newWindow3,text="CONFIRM PASSWORD:",font=("ALGERIAN",26),bg="#106394",fg="white",relief=RAISED)
        lb4.grid(row=3,column=0,padx=15,pady=15)
        ent4=Entry(newWindow3, show="*",font=("AREIAL",26),bg="white",fg="black",textvariable=confirmpassword,relief=RAISED)
        ent4.grid(row=3,column=1,padx=15,pady=15)
        lb5=Label(newWindow3,text="MOBILE NUMBER:",font=("ALGERIAN",26),bg="#106394",fg="white",relief=RAISED)
        lb5.grid(row=4,column=0,padx=15,pady=15)
        ent5=Entry(newWindow3,font=("AREIAL",26),bg="white",fg="black",textvariable=mobile,relief=RAISED)
        ent5.grid(row=4,column=1,padx=15,pady=15)


        btn3=Button(newWindow3,text="SUBMIT",font=("ALGERIAN",20),bg="#245551",fg="white",command=submit,activebackground="yellow",bd=3)
        btn3.grid(row=5,column=1,padx=15,pady=15)

    lb1=Label(newWindow6,text="USERNAME:",font=("ALGERIAN",26),bg="#106394",fg="white",relief=RAISED)
    lb1.grid(row=0,column=0,padx=15,pady=15)
    ent1=Entry(newWindow6,font=("AREIAL",26),bg="white",fg="black",textvariable=username1,relief=RAISED)
    ent1.grid(row=0,column=1,padx=15,pady=15)
    lb2=Label(newWindow6,text="PASSWORD:",font=("ALGERIAN",26),bg="#106394",fg="white",relief=RAISED)
    lb2.grid(row=1,column=0,padx=15,pady=15)
    ent2=Entry(newWindow6, show="*",font=("AREIAL",26),bg="white",fg="black",textvariable=password1,relief=RAISED)
    ent2.grid(row=1,column=1,padx=15,pady=15)
    lb3=Label(newWindow6,text="CREATE NEW ACCOUNT:",font=("ALGERIAN",26),bg="#106394",fg="white",relief=RAISED)
    lb3.grid(row=4,column=0,padx=15,pady=15)


    btn1=Button(newWindow6,text="LOGIN",font=("ALGERIAN",20),bg="#245551",fg="white",command=login,activebackground="Pink",bd=3)
    btn1.grid(row=2,column=1,padx=15,pady=15)

    btn2=Button(newWindow6,text="SIGNUP",font=("ALGERIAN",20),bg="#245551",fg="white",command=signup,activebackground="Pink",bd=3)
    btn2.grid(row=4,column=1,padx=15,pady=15)


def mainapp():
    newWindow6.destroy()
    newWindow7=Toplevel(app)
    newWindow7.title("Diabetes Prediction App")
    newWindow7.geometry("1200x1000")
    newWindow7.configure(background="skyblue")
    newWindow7.resizable(width=False,height=False)

    cur=dbase.cursor()
##    bg_image=Image.open("dia.png")
##    test_img=ImageTk.PhotoImage(bg_image)

    def submit():

        

        dbase.execute(f'''CREATE TABLE IF NOT EXISTS
               {e}(
               ID INTEGER PRIMARY KEY AUTOINCREMENT,
               NAME TEXT NOT NULL,
               GENTER TEXT NOT NULL,
               GLUCOSE TEXT NOT NULL,
               BLOODPRESSURE TEXT NOT NULL,
               SKINTHICKNESS TEXT NOT NULL,
               INSULIN TEXT NOT NULL,
               BMI TEXT NOT NULL,
               DIABETES_PED_FUN TEXT NOT NULL,
               AGE TEXT NOT NULL,
               PREDICTED_RESULT TEXT NOT NULL)''')

        Nameval = Name.get()
        
        Genterval = Genter.get()
        
        Glucoseval=Glucose.get()
        
        BloodPressureval=BloodPressure.get()
        
        SkinThicknessval=SkinThickness.get()                                                
        
        Insulinval=Insulin.get()
        
        BMIval=BMI.get()
        
        DiabetesPedigreeFunctionval=DiabetesPedigreeFunction.get()
        
        Ageval=Age.get()
        

        def createNewWindow():
            newWindow = Toplevel(app)
            newWindow.title("STOP ANAEMIA")
            newWindow.geometry("650x450")

            
            bg_lb1=Label(newWindow,image=test_img1)
            bg_lb1.place(x=0,y=0,relwidth=1,relheight=1)
            newWindow.resizable(width=False,height=False)

            

            def hel():
                newWindow10=Toplevel(app)
                newWindow10.title("healthy page")
                newWindow10.geometry("800x750")
                newWindow10.configure(background='light yellow')
                bg_lb1=Label(newWindow10,image=test_img10)
                bg_lb1.place(x=0,y=0,relwidth=1,relheight=1)
                newWindow10.resizable(width=False,height=False)

            def unhel():
                newWindow11=Toplevel(app)
                newWindow11.title("unhealthy page")
                newWindow11.geometry("800x700")
                newWindow11.configure(background='light yellow')
                bg_lb2=Label(newWindow11,image=test_img11)
                bg_lb2.place(x=0,y=0,relwidth=1,relheight=1)
                newWindow11.resizable(width=False,height=False)
            

            btn3=Button(newWindow,command=hel,text="HEALTHY",font=("bold",18),bg="lightgray",fg="black",activebackground="red",activeforeground="yellow",width=10,bd=5)
##            btn3.grid(row=0,column=2,padx=15,pady=15)
            btn3.place(x = 20,y = 5)

            btn4=Button(newWindow,command=unhel,text="UN-HEALTHY",font=("bold",18),bg="lightgray",fg="black",activebackground="red",activeforeground="yellow",width=10,bd=5)
##            btn4.grid(row=0,column=3,padx=15,pady=15)
            btn4.place(x = 450,y = 5 )

        
        
        result=model.predict([[Glucoseval,BloodPressureval,SkinThicknessval,Insulinval,BMIval,DiabetesPedigreeFunctionval,Ageval]])
        result_percentage=model.predict_proba([[Glucoseval,BloodPressureval,SkinThicknessval,Insulinval,BMIval,DiabetesPedigreeFunctionval,Ageval]])

        if result[0]==1:
            a='have diabetes'
            diabetes=round(max(result_percentage[0])*100,2)
            diabetes="{} % may {}".format(round(max(result_percentage[0])*100,2),a)
            
            butt2 = Button(newWindow7, text="SYMPTOMS",command=createNewWindow,font=("Bahnschrift",20),bg="#d4ca19",fg="#050505")
            butt2.grid(row=10,column=1,padx=15,pady=15)
        else:
            a='not have diabetes'
            diabetes=round(max(result_percentage[0])*100,2)
            diabetes="{} % may {}".format(round(max(result_percentage[0])*100,2),a)
            
       

        ans.configure(text=diabetes)

        
        dbase.execute(f'''INSERT INTO {e}(NAME,GENTER,GLUCOSE,BLOODPRESSURE,SKINTHICKNESS,
                                    INSULIN,BMI,DIABETES_PED_FUN,AGE,PREDICTED_RESULT
                                   )VALUES(?,?,?,?,?,?,?,?,?,?)''',(Nameval,Genterval,Glucoseval,BloodPressureval,SkinThicknessval,Insulinval,BMIval,
                                                                                DiabetesPedigreeFunctionval,Ageval,diabetes))
                                                                      
        dbase.commit()
        cur.execute(f"select * from {e} order by id desc")
        data1 = cur.fetchone()
        
        ms.showinfo('Note',data1[0])

       
        ent1.delete(first=0,last=END)
        ent2.delete(first=0,last=END)
        ent3.delete(first=0,last=END)
        ent4.delete(first=0,last=END)
        ent5.delete(first=0,last=END)
        ent6.delete(first=0,last=END)
        ent7.delete(first=0,last=END)
        ent9.delete(first=0,last=END)
    
    def createNewWindow2():
        newWindow1 = Toplevel(app)
        newWindow1.title("Quick Search")
        newWindow1.geometry("600x270")
        newWindow1.resizable(width=False,height=False)

        bg_lb2=Label(newWindow1,image=test_img2)
        bg_lb2.place(x=0,y=0,relwidth=1,relheight=1)
        
        date=StringVar()
        p_id=StringVar()

        def search():
            dateval = date.get()
            p_idval = p_id.get()
            
        
            x = re.search("\d\d-\d\d-\d\d", dateval)

            

            if dateval and p_idval:
                if x:
                    dateval=dateval.replace('-','')
                    dateval='T'+dateval



                    cur=dbase.cursor()
                    cur.execute(f"SELECT * FROM {dateval} WHERE ID=?",(p_idval))
                    data=cur.fetchone()

                  
                    data_id=data[0]
                    data_name=data[1]
                    data_Gen=data[2]
                    data_GLUCOSE=data[3]
                    data_BLOODPRESSURE=data[4]
                    data_SKINTHICKNESS=data[5]
                    data_INSULIN=data[6]
                    data_BMI=data[7]
                    data_DIABETES_PED_FUN=data[8]
                    data_AGE=data[9]
                    data_result=data[10]
                    data=f'''
                    Patient_ID:{data_id}
                    Name:{data_name}
                    Gender:{data_Gen}
                    GLUCOSE:{data_GLUCOSE}
                    BLOODPRESSURE:{data_BLOODPRESSURE}
                    SKINTHICKNESS:{data_SKINTHICKNESS}
                    INSULIN:{data_INSULIN}
                    BMI:{data_BMI}
                    DIABETES_PED_FUN:{data_DIABETES_PED_FUN}
                    AGE:{data_AGE}
                    RESULT:{data_result}'''

                ent11.delete(first=0,last=END)
                ent215.delete(first=0,last=END)
                if data:
                        ms.showinfo('Search Result',data)
                else:
                    ms.showerror('Error','Please Enter Correct Format')
            else:
                ms.showerror('Error','Please enter all data')

    


        lb11 = Label(newWindow1,text="Enter Recorded Date",font=("Georgia",20),bg="black",fg="white",relief=RAISED)
        lb11.grid(row=0,column=0,padx=15,pady=15)
        ent11=Entry(newWindow1,textvariable=date,font=("bold",20),bg="#b8f0a5",fg="black",relief=RAISED,width=13)
        ent11.grid(row=0,column=1,padx=15,pady=15)


        lb21=Label(newWindow1,text="Enter Patient ID",font=("Georgia",20),bg="black",fg="white",relief=RAISED)
        lb21.grid(row=1,column=0,padx=15,pady=15)
        ent215=Entry(newWindow1,textvariable=p_id,font=("bold",20),bg="#b8f0a5",fg="black",relief=RAISED,width=13)
        ent215.grid(row=1,column=1,padx=15,pady=15)
        

        btn41=Button(newWindow1,command=search,text="Search",font=("bold",14),bg="green",fg="black",activebackground="red",activeforeground="yellow",width=10,bd=5)
        btn41.grid(row=2,column=1,padx=15,pady=15)

    

    Name = StringVar()
   
    Glucose=DoubleVar()
    BloodPressure=DoubleVar()
    SkinThickness=DoubleVar()
    Insulin=DoubleVar()
    BMI=DoubleVar()
    DiabetesPedigreeFunction=DoubleVar()
    Age=DoubleVar()
    Genter = StringVar()
      

    bg_lb=Label(newWindow7,image=test_img)
    bg_lb.place(x=0,y=0,relwidth=1,relheight=1)

    lb101=Label(newWindow7,text="Enter the GENDER_level",font=("Georgia",22),bg="skyblue",fg="black")
    lb101.grid(row=8,column=0,padx=15,pady=15)
    Radiobutton(newWindow7, text="Male",variable=Genter,value='Male',font=("Georgia",22),bg="#b8f0a5",fg="black").grid(row=8,column=1,padx=15,pady=15)
    Radiobutton(newWindow7, text="Female",variable=Genter,value='Female',font=("Georgia",22),bg="#b8f0a5",fg="black").grid(row=8,column=2,padx=15,pady=15)
    

    lb9=Label(newWindow7,text="Patient Name",font=("Georgia",20),bg="skyblue",fg="#663300")
    lb9.grid(row=0,column=0,padx=15,pady=15)
    ent9=Entry(newWindow7,textvariable=Name,font=("Georgia",20),bg="skyblue")
    ent9.grid(row=0,column=1,padx=15,pady=15)

    lb1=Label(newWindow7,text="Enter the Glucose_level",font=("Georgia",20),bg="skyblue",fg="#663300")
    lb1.grid(row=1,column=0,padx=15,pady=15)
    ent1=Entry(newWindow7,textvariable=Glucose,font=("Georgia",20),bg="skyblue")
    ent1.grid(row=1,column=1,padx=15,pady=15)


    lb2=Label(newWindow7,text="Enter the BloodPressure_level",font=("Georgia",20),bg="skyblue",fg="#663300")
    lb2.grid(row=2,column=0,padx=15,pady=15)
    ent2=Entry(newWindow7,textvariable=BloodPressure,font=("Georgia",20),bg="skyblue")
    ent2.grid(row=2,column=1,padx=15,pady=15)



    lb3=Label(newWindow7,text="Enter the SkinThickness_level",font=("Georgia",20),bg="skyblue",fg="#663300")
    lb3.grid(row=3,column=0,padx=15,pady=15)
    ent3=Entry(newWindow7,textvariable=SkinThickness,font=("Georgia",20),bg="skyblue")
    ent3.grid(row=3,column=1,padx=15,pady=15)

    lb4=Label(newWindow7,text="Enter the Insulin_level",font=("Georgia",20),bg="skyblue",fg="#663300")
    lb4.grid(row=4,column=0,padx=15,pady=15)
    ent4=Entry(newWindow7,textvariable=Insulin,font=("Georgia",20),bg="skyblue")
    ent4.grid(row=4,column=1,padx=15,pady=15)

    lb5=Label(newWindow7,text="Enter the BMI_level",font=("Georgia",20),bg="skyblue",fg="#663300")
    lb5.grid(row=5,column=0,padx=15,pady=15)
    ent5=Entry(newWindow7,textvariable=BMI,font=("Georgia",20),bg="skyblue")
    ent5.grid(row=5,column=1,padx=15,pady=15)


    lb6=Label(newWindow7,text="Enter the DiabetesPedigreeFunction",font=("Georgia",20),bg="skyblue",fg="#663300")
    lb6.grid(row=6,column=0,padx=15,pady=15)
    ent6=Entry(newWindow7,textvariable=DiabetesPedigreeFunction,font=("Georgia",20),bg="skyblue")
    ent6.grid(row=6,column=1,padx=15,pady=15)



    lb7=Label(newWindow7,text="Enter the Age",font=("Georgia",20),bg="skyblue",fg="#663300")
    lb7.grid(row=7,column=0,padx=15,pady=15)
    ent7=Entry(newWindow7,textvariable=Age,font=("Georgia",20),bg="skyblue")
    ent7.grid(row=7,column=1,padx=15,pady=15)

    
    lb8=Label(newWindow7,text="Predicted Diabetes ",font=("Georgia",20),bg="skyblue",fg="#663300")
    lb8.grid(row=9,column=0,padx=15,pady=15)
    ans=Label(newWindow7,font=("Georgia",26),width=25,bg="skyblue")
    ans.grid(row=9,column=1,padx=15,pady=15)

    def quit():
            print('*********************************  APP CLOSED  ************************************')
            newWindow7.destroy()



    btn51=Button(newWindow7,command=submit,text="submit",font=("Georgia",16),bg="green",fg="white",activebackground="red",activeforeground="yellow",width=10,bd=5)
    btn51.place(x = 495, y = 700)

    btn52=Button(newWindow7,command=quit,text="Quit",font=("Georgia",16),bg="green",fg="white",activebackground="red",activeforeground="yellow",width=10,bd=5)
    btn52.place(x = 495, y = 770)
  
    btn53=Button(newWindow7,command=createNewWindow2,text="Quick Search",font=("bold",16),bg="green",fg="white",activebackground="red",activeforeground="yellow",width=10,bd=5)
    btn53.place(x = 900, y = 770)

    

    newWindow7.mainloop()

       

lb1=Label(app,text="Diabetes Prediction APP",font=("Georgia",22),bg="black",fg="white",relief=RAISED)
lb1.grid(row=1,column=0,padx=15,pady=15)

btn1=Button(app,command=log,text="GET STARTED",font=("bold",14),bg="green",fg="black",activebackground="red",activeforeground="yellow",width=12,bd=5)
btn1.grid(row=2,column=0,padx=15,pady=15)

app.mainloop()




