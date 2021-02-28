from mtTkinter import *
import cv2
import sqlite3
import numpy as np
import pickle
from tkMessageBox import *
from PIL import ImageTk, Image
import os

rec=cv2.createLBPHFaceRecognizer();
path = 'dataSet'
faceCascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class New(Frame):
    def __init__(self,parent=None):
        Frame.__init__(self,parent)
        self.pack()
        photo1 = PhotoImage(file="addstudent.gif")
        font = 'times 11'
        addbutton=Button(self,compound=TOP,image=photo1,  text="Add Student",command=self.submit,font=font,bg='white')
        addbutton.pack(fill=BOTH,side='bottom')
        addbutton.image = photo1

    def submit(self):
        def getImagesWithID(path):
            imagePaths=[os.path.join(path,f)for f in os.listdir(path)]
            faces=[]
            IDs=[]
            for imagePath in imagePaths:
                faceImg=Image.open(imagePath).convert('L');
                faceNp=np.array(faceImg,'uint8')
                ID=int(os.path.split(imagePath)[-1].split('.')[1])
                faces.append(faceNp)
                IDs.append(ID)
                cv2.waitKey(10)
            return IDs, faces
        
    
        def delete1():
            roll=ent1.get()
            new.destroy()
            conn=sqlite3.connect("Facebase.db")
            cmd="SELECT * FROM Student WHERE Roll="+str(roll)
            cursor=conn.execute(cmd)
            isRecordExist=0
            for row in cursor:
                isRecordExist=1
            if(isRecordExist==1):
                cmd='DELETE FROM Student WHERE Roll='+str(roll)
            else:
                showerror('Error!', "No Data Found")
            conn.execute(cmd)
            conn.commit()
            conn.close()
            self.submit()

        def save(roll,n):
           new.destroy()
           conn=sqlite3.connect("Facebase.db")
           cmd="SELECT * FROM Student WHERE Roll="+str(roll)
           cursor=conn.execute(cmd)
           isRecordExist=0
           for row in cursor:
              isRecordExist=1
           if(isRecordExist==1):
              cmd='UPDATE Student SET Name="'+str(n)+'" WHERE Roll='+str(roll)
           else:
               cmd='INSERT INTO Student(Roll,Name) Values('+str(roll)+',"'+str(n)+'")'
           conn.execute(cmd)
           conn.commit()
           conn.close()
        def getface():
           cam=cv2.VideoCapture(0)
           roll=ent1.get()
           n=ent.get()
           save(roll,n)
           sampleNum=0
           while True:
               ret, im =cam.read()
               gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
               faces=faceCascade.detectMultiScale(gray,1.3,5);
               for(x,y,w,h) in faces:
                   sampleNum=sampleNum+1
                   cv2.imwrite("dataSet/User."+str(roll)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
                   cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(0,255,0),2)
               cv2.imshow("im",im);
               cv2.waitKey(30);
               if sampleNum>15:
                   cam.release()
                   cv2.destroyAllWindows()
                   break
           Ids,faces=getImagesWithID(path)
           rec.train(faces,np.array(Ids))
           rec.save('recognizer/trainningData.yml')
           self.submit()
            
        new=Tk()
        nframe = Frame(new)
        nframe.pack(side='top', padx=20, pady=20)

        font = 'times 25 bold'
        ntext = Label(nframe, text='Smart Attendance System', font=font)
        ntext.pack(side='top', pady=20,padx=20)

        rframe=Frame(new)
        rframe.pack(side='top', padx=20, pady=20)
        conn = sqlite3.connect('Facebase.db')
        cursor=conn.cursor()
        cursor.execute("SELECT Roll FROM Student")
        i=0
        j=0
        for row in cursor:
            if i==0:
                e = Label(rframe,text='Roll No.',width=20,relief=RIDGE,bg='sky blue')
                e.grid(row=i, column=j, sticky=NSEW)
                i=i+1
            else:
                e = Label(rframe,text=row,relief=RIDGE)
                e.grid(row=i, column=j, sticky=NSEW)
                i=i+1

        cursor.execute("SELECT Name FROM Student")
        i=0
        j=1
        for row in cursor:
            if i==0:
                e = Label(rframe,text='Name',width=20,relief=RIDGE,bg='sky blue')
                e.grid(row=i, column=j, sticky=NSEW)
                i=i+1
            else:
                e = Label(rframe,text=row,relief=RIDGE)
                e.grid(row=i, column=j, sticky=NSEW)
                i=i+1
        naframe = Frame(new)
        naframe.pack(side='top', padx=20, pady=20)
        
        n_label = Label(naframe, text='Full Name')
        n_label.pack(side='left')
        ent= Entry(naframe, width=22)  
        ent.insert(0,'' )
        ent.pack(side='left')

        lframe=Frame(new)
        lframe.pack(side='top', padx=20, pady=20)
        n_label = Label(lframe, text='Roll No.  ')
        n_label.pack(side='left')
        ent1= Entry(lframe, width=22)  
        ent1.insert(0,'')
        ent1.pack(side='left')
    
        bframe=Frame(new)
        bframe.pack(side='top', padx=20, pady=20)

        quit_botton=Button(bframe,text='Remove Student ',command=delete1,foreground='white',bg='red')
        quit_botton.pack(side='right', pady=5,padx=20, fill='y')

        quit_botton=Button(bframe,text='Add Or Update',command=getface,bg='green')
        quit_botton.pack(side='right', pady=5,padx=20, fill='y')

class Take(Frame):
    def __init__(kelf,parent=None):
        Frame.__init__(kelf,parent)
        kelf.pack()
        photo1 = PhotoImage(file="take.gif")
        font = 'times 11'
        addbutton=Button(kelf,compound=TOP,image=photo1,  text="Take Attendance",command=kelf.takea,font=font,bg='white')
        addbutton.pack(fill=BOTH,side='bottom')
        addbutton.image = photo1

    def takea(kelf):
        def attendancerep(red):
            new=Tk()
            nframe = Frame(new)
            nframe.pack(side='top', padx=100, pady=20)
            font = 'times 18 bold'
            ntext = Label(nframe, text='Smart Attendance System', font=font)
            ntext.pack(side='top', pady=50,padx=50)
            
            rframe=Frame(new)
            rframe.pack(side='top', padx=100, pady=20)
            conn = sqlite3.connect('Facebase.db')
            cursor=conn.cursor()
            cursor.execute('SELECT Roll FROM "'+str(red)+'"')
            i=0
            j=0
            for row in cursor:
                if i==0:
                    e = Label(rframe,text='Roll no.',width=20,relief=RIDGE,bg='sky blue')
                    e.grid(row=i, column=j, sticky=NSEW)
                    i=i+1
                else:
                    e = Label(rframe,text=row,relief=RIDGE)
                    e.grid(row=i, column=j, sticky=NSEW)
                    i=i+1
            cursor.execute('SELECT Name FROM "'+str(red)+'"')
            i=0
            j=1
            for row in cursor:
                if i==0:
                    e = Label(rframe,text='Name',width=20,relief=RIDGE,bg='sky blue')
                    e.grid(row=i, column=j, sticky=NSEW)
                    i=i+1
                else:
                    e = Label(rframe,text=row,relief=RIDGE)
                    e.grid(row=i, column=j, sticky=NSEW)
                    i=i+1

            cursor.execute('SELECT Attendance FROM "'+str(red)+'"')
            i=0
            j=2
            for row in cursor:
                if i==0:
                    e = Label(rframe,text='Attendance',width=20,relief=RIDGE,bg='sky blue')
                    e.grid(row=i, column=j, sticky=NSEW)
                    i=i+1
                else:
                    e = Label(rframe,text=row,relief=RIDGE)
                    e.grid(row=i, column=j, sticky=NSEW)
                    i=i+1
            
        def takeAttendance(tab):
            def getProfile(tab,id):
                conn=sqlite3.connect("Facebase.db")
                cmd='SELECT * FROM "'+str(tab)+'" WHERE Roll='+str(id)
                cursor=conn.execute(cmd)
                profile=None
                for row in cursor:
                    profile=row
                conn.close()
                return profile

            rec.load("recognizer/trainningData.yml")
            cam=cv2.VideoCapture(0);
            font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX,1,1,0,1,1)
            an="Present"
            Attend=0
            while True:
                ret,img=cam.read()
                gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                faces=faceCascade.detectMultiScale(gray,1.3,5);
                for(x,y,w,h) in faces:
                    id, conf=rec.predict(gray[y:y+h,x:x+w])
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                    profile=getProfile(tab,id)
                    if(profile!=None):
                        cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[0]),(x,y+h+30),font,(248,248,255));
                        cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[1]),(x,y+h+60),font,(248,248,255));
                        cv2.cv.PutText(cv2.cv.fromarray(img),str(profile[2]),(x,y+h+90),font,(248,248,255));
                        if(Attend!=0 & Attend<20):
                            conn=sqlite3.connect("Facebase.db")
                            cmd='UPDATE "'+str(tab)+'" SET Attendance="'+str(an)+'" WHERE Roll='+str(id)
                            cursor=conn.execute(cmd)
                            conn.execute(cmd)
                            conn.commit()
                            conn.close()
                            Attend=0
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        red=tab
                        attendancerep(red)
                        break
                    if cv2.waitKey(1) & 0xFF == ord('t'):
                        Attend=Attend+1
                            
                cv2.imshow("Face",img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    red=tab
                    attendancerep(red)
                    break
                
            cam.release()
            cv2.destroyAllWindows()

        def create():
            tab=ent3.get()
            new.destroy()
            conn=sqlite3.connect("Facebase.db")
            cmd='SELECT * FROM Tablelist WHERE Tab="'+str(tab)+'"'
            cursor=conn.execute(cmd)
            isRecordExist=0
            for row in cursor:
                isRecordExist=1
            if(isRecordExist==1):
                takeAttendance(tab)
            else:
                cmd='INSERT INTO Tablelist(Tab) Values("'+str(tab)+'")'
                conn.execute(cmd)
                cmd='CREATE TABLE "'+str(tab)+'" AS SELECT * FROM Student'
                conn.execute(cmd)
                conn.commit()
                conn.close()
                takeAttendance(tab)
                red=tab
                attendancerep(red)

        new=Tk()
        nframe = Frame(new)
        nframe.pack(side='top', padx=1, pady=1)
        font = 'times 18 bold'
        ntext = Label(nframe, text='Smart Attendance System', font=font)
        ntext.pack(side='top', pady=1,padx=1)
        tframe=Frame(new)
        tframe.pack(side='top', padx=100, pady=20)
        conn = sqlite3.connect('Facebase.db')
        cursor=conn.cursor()
        cursor.execute("SELECT Tab FROM Tablelist")
        i=0
        j=1
        for row in cursor:
            if i==0:
                e = Label(tframe,text='Date',width=20,relief=RIDGE,bg='sky blue')
                e.grid(row=i, column=j, sticky=NSEW)
                i=i+1
            else:
                e = Label(tframe,text=row,relief=RIDGE)
                e.grid(row=i, column=j, sticky=NSEW)
                i=i+1
        dframe=Frame(new)
        dframe.pack(side='top', padx=1, pady=1)
        n_label = Label(dframe, text='Enter Date :')
        n_label.pack(side='left')
        ent3= Entry(dframe, width=22)
        ent3.insert(0,'')
        ent3.pack(side='left')
        quit_botton=Button(dframe,text='Take Attendance',command=create,bg='blue',foreground='white')
        quit_botton.pack( pady=5, fill='y')

class Quit(Frame):
    def __init__(helf,parent=None):
        Frame.__init__(helf,parent)
        helf.pack()
        photo1 = PhotoImage(file="quit.gif")
        font = 'times 11'
        addbutton=Button(helf,compound=TOP,image=photo1,  text="Quit",command=helf.takea,font=font,bg='white')
        addbutton.pack(fill=BOTH,side='bottom')
        addbutton.image = photo1

    def takea(helf): 
        def quit(event=None):
            ans = askokcancel('Verify exit', "Really quit?")
            if ans:root.destroy()
        quit()

class Report(Frame):
    def __init__(telf,parent=None):
        Frame.__init__(telf,parent)
        telf.pack()
        photo1 = PhotoImage(file="report.gif")
        font = 'times 11'
        addbutton=Button(telf,compound=TOP,image=photo1,  text="Get Report",command=telf.rep,font=font,bg='white')
        addbutton.pack(fill=BOTH,side='bottom')
        addbutton.image = photo1

    def rep(telf):
        def tablerep():
            def deleterep(rep):
                new.destroy()
                conn=sqlite3.connect("Facebase.db")
                cmd='SELECT * FROM Tablelist WHERE Tab="'+str(rep)+'"'
                cursor=conn.execute(cmd)
                isRecordExist=0
                for row in cursor:
                    isRecordExist=1
                if(isRecordExist==1):
                    cmd='DELETE FROM Tablelist WHERE Tab="'+str(rep)+'"'
                    conn.execute(cmd)
                    cmd='DROP TABLE "'+str(rep)+'"'
                    conn.execute(cmd)
                else:
                    showerror('Error!', "No Data Found")
                conn.commit()
                conn.close()
                tablerep()

            def deleter():
                rep=ent3.get()
                deleterep(rep)

            def attendancerep(red):
                new=Tk()
                nframe = Frame(new)
                nframe.pack(side='top', padx=20, pady=20)
                font = 'times 18 bold'
                ntext = Label(nframe, text='Smart Attendance System', font=font)
                ntext.pack(side='top', pady=10,padx=10)

                rframe=Frame(new)
                rframe.pack(side='top', padx=20, pady=20)
                conn = sqlite3.connect('Facebase.db')
                cursor=conn.cursor()
                cursor.execute('SELECT Roll FROM "'+str(red)+'"')
                i=0
                j=0
                for row in cursor:
                    if i==0:
                        e = Label(rframe,text='Roll no.',width=20,relief=RIDGE,bg='sky blue')
                        e.grid(row=i, column=j, sticky=NSEW)
                        i=i+1
                    else:
                        e = Label(rframe,text=row,relief=RIDGE)
                        e.grid(row=i, column=j, sticky=NSEW)
                        i=i+1
                cursor.execute('SELECT Name FROM "'+str(red)+'"')
                i=0
                j=1
                for row in cursor:
                    if i==0:
                        e = Label(rframe,text='Name',width=20,relief=RIDGE,bg='sky blue')
                        e.grid(row=i, column=j, sticky=NSEW)
                        i=i+1
                    else:
                        e = Label(rframe,text=row,relief=RIDGE)
                        e.grid(row=i, column=j, sticky=NSEW)
                        i=i+1

                cursor.execute('SELECT Attendance FROM "'+str(red)+'"')
                i=0
                j=2
                for row in cursor:
                    if i==0:
                        e = Label(rframe,text='Attendance',width=20,relief=RIDGE,bg='sky blue')
                        e.grid(row=i, column=j, sticky=NSEW)
                        i=i+1
                    else:
                        e = Label(rframe,text=row,relief=RIDGE)
                        e.grid(row=i, column=j, sticky=NSEW)
                        i=i+1

            def atten():
                red=ent3.get()
                attendancerep(red)

            new=Tk()
            nframe=Frame(new)
            nframe.pack(side='top', padx=20, pady=20)
            font = 'times 18 bold'
            ntext = Label(nframe, text='Smart Attendance System', font=font)
            ntext.pack(side='top', pady=20,padx=20)
            tframe=Frame(new)
            tframe.pack(side='top', padx=20, pady=20)
            conn = sqlite3.connect('Facebase.db')
            cursor=conn.cursor()
            cursor.execute("SELECT Tab FROM Tablelist")
            i=0
            j=1
            for row in cursor:
                if i==0:
                    e = Label(tframe,text='Date',width=20,relief=RIDGE,bg='sky blue')
                    e.grid(row=i, column=j, sticky=NSEW)
                    i=i+1
                else:
                    e = Label(tframe,text=row,relief=RIDGE)
                    e.grid(row=i, column=j, sticky=NSEW)
                    i=i+1

            dframe=Frame(new)
            dframe.pack(side='top', padx=100, pady=20)
            n_label = Label(dframe, text='Enter Date')
            n_label.pack(side='left')
            rframe=Frame(new)
            rframe.pack(side='bottom', padx=1, pady=1)
            ent3= Entry(dframe, width=22)  
            ent3.insert(0,'')
            ent3.pack(side='left')

            drframe=Frame(new)
            drframe.pack(side='top', padx=20, pady=20)
            quit_botton=Button(drframe,text='Delete Report',command=deleter,foreground='white',bg='red')
            quit_botton.pack(side='left', pady=5,padx=10 ,fill='y')
            quit_botton=Button(drframe,text='Get Report',command=atten,bg='green')
            quit_botton.pack(side='right', pady=5,padx=10, fill='y') 
        tablerep()

directory='recognizer'
if not os.path.exists(directory):
    os.makedirs(directory)

directory='dataSet'
if not os.path.exists(directory):
    os.makedirs(directory)
    
root=Tk()
root.resizable(width=False, height=False)
root.config(bg='sky blue')
root.wm_title("Smart Attendance System")
img = ImageTk.PhotoImage(Image.open("Header1.jpg"))
panel = Label(root, image = img ,bg='sky blue')
panel.pack(side='top',pady=30,expand = "yes")
top = Frame(root,bg='sky blue')
top.pack(side='top')
hwframe = Frame(top)
hwframe.pack(side='top')
font = 'times 25 bold'
hwtext = Label(hwframe, text='Smart Attendance System', font=font,bg='sky blue',padx=45)

wframe = Frame(top,bg='sky blue')
wframe.pack(side='bottom')


Quit(wframe).pack(side='right',padx=10,pady=10,fill=BOTH)

Report(wframe).pack(side='left',padx=10,pady=10,fill=BOTH)

wtframe = Frame(top,bg='sky blue')
wtframe.pack(side='top')

Take(wtframe).pack(side='right',padx=10,pady=10,fill=BOTH)

New(wtframe).pack(side='left',padx=10,pady=10,fill=BOTH)

hwtext.pack(side='top')
root.mainloop()
