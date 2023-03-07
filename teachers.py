import pymongo
import tkinter as tk
from tkinter import messagebox

class TeachersForm:
    def teacherform():
        #for database connection
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient['enrollmentsystem']
        mycol = mydb["teachers"]

        #two-dimensional list
        lst=[["ID","Name","Department","Contact"]]

        #to assign to the 2 dimensional list to the grid
        def callback(event):
            li=[]
            li=event.widget._values
            teacherid.set(lst[li[1]][0])
            teachername.set(lst[li[1]][1])
            teacherdept.set(lst[li[1]][2])
            teachercontact.set(lst[li[1]][3])
            
        def creategrid(n):
            lst.clear()
            lst.append(["ID","Name","Dept","Contact"])
            cursor = mycol.find({})
            for text_fromDB in cursor:
                teachid = str(text_fromDB["teachid"])
                teachname = str(text_fromDB["teachname"].encode("utf-8").decode("utf-8"))
                teachdept = str(text_fromDB["teachdept"].encode("utf-8").decode("utf-8"))
                teachcontact = str(text_fromDB["teachcontact"])
                lst.append([teachid,teachname,teachdept,teachcontact])
                print(f"{teachid} {teachname} {teachdept} {teachcontact}")
        #to catch the 2 dimensional list and put it in a multiple entries or the grid
                #i is the row and j is the column
            for i in range(len(lst)):
                    for j in range(len(lst[0])):
                            mgrid = tk.Entry(teachersWindow, width=25)
                            mgrid.insert(tk.END,lst[i][j])
                            mgrid._values = mgrid.get(), i
                            mgrid.grid(row=i+7, column=j+6)
                            mgrid.bind("<Button-1>", callback)
        #to clear all of the text entries for rows that is greater than 6
            if n==1:
                    for label in teachersWindow.grid_slaves():
                        if int(label.grid_info()["row"]) > 6:
                            label.grid_forget()


        def msgbox(msg,titlebar):
            result=messagebox.askokcancel (title=titlebar,message=msg)
            return result

        #funtions for buttons
        def save():
            r=msgbox("save record?","record")
            if r==True:
                #saves and counts the number of documents in the students selection
                newid = mycol.count_documents({})
                if newid!=0:
                    newid= mycol.find_one(sort=[("teachid",-1)])["teachid"]
                id=newid+1
                teacherid.set(id)
                mydict = {"teachid":int(float(teachid.get())), "teachname": teachname.get(),"teachdept":teachdept.get(), "teachcontact": teachcontact.get()} 
        #to insert one document in the collection "insert_one"
                x = mycol.insert_one(mydict)
                creategrid(1)
                creategrid(0)

        def delete():
            r=msgbox("delete record?","record")
            if r==True:
                #deletes the certain variable in the collection using the ID
                myquery = {"teachid":int(float(teachid.get()))}
                mycol.delete_one(myquery)
                creategrid(1)
                creategrid(0)

        def update():
            option = messagebox.askokcancel("Update", "Update record?")
            if option:
                idQuery = {"teachid": int(float(teachid.get()))}
                updateValues = {
                    "$set": {
                        "teachname": teachname.get(),
                        "teachdept": teachdept.get(),
                        "teachcontact": teachcontact.get(),
                    }
                }
                mycol.update_one(idQuery, updateValues)
                creategrid(1)
                creategrid(0)


        #Teachers GUI Form
        teachersWindow = tk.Tk()
        teachersWindow.title("Teachers Form")
        teachersWindow.geometry("1050x400")
        teachersWindow.configure(bg="green")

        #Students Enlisment Form GUI
        label = tk.Label(teachersWindow,text="Teachers Enlistment Form", width=30, height=1, bg="white", anchor="center")
        label.config(font=("Courier",10))
        label.grid(column=2,row=1)
        #Student ID
        label = tk.Label(teachersWindow,text="Teacher ID:", width=10, height=1, bg="white")
        label.grid(column=1,row=2)

        teacherid=tk.StringVar(teachersWindow)
        teachid=tk.Entry(teachersWindow, textvariable=teacherid)
        teachid.grid(column=2, row=2)
        teachid.configure(state=tk.DISABLED)
        #Student Name
        label = tk.Label(teachersWindow,text="Teacher Name:", width=15, height=1, bg="white")
        label.grid(column=1,row=3)

        teachername=tk.StringVar(teachersWindow)
        teachname=tk.Entry(teachersWindow, textvariable=teachername)
        teachname.grid(column=2, row=3)
        #Student Email
        label = tk.Label(teachersWindow,text="Teacher Dept:", width=15, height=1, bg="white")
        label.grid(column=1,row=4)

        teacherdept=tk.StringVar(teachersWindow)
        teachdept=tk.Entry(teachersWindow, textvariable=teacherdept)
        teachdept.grid(column=2, row=4)
        #Student Course
        label = tk.Label(teachersWindow,text="Teacher Contact:", width=15, height=1, bg="white")
        label.grid(column=1,row=5)

        teachercontact=tk.StringVar(teachersWindow)
        teachcontact=tk.Entry(teachersWindow, textvariable=teachercontact)
        teachcontact.grid(column=2, row=5)

        creategrid(0)
        #Buttons
        # Save Button
        savebutton = tk.Button(master=teachersWindow,text = "Save", command=save)
        savebutton.grid(column=1, row=6)
        #Delete Button
        deletebutton = tk.Button(master=teachersWindow,text = "Delete", command=delete)
        deletebutton.grid(column=2, row=6)                
        #Update Button
        updatebutton = tk.Button(master=teachersWindow,text = "Update", command=update)
        updatebutton.grid(column=3, row=6)

        teachersWindow.mainloop()
