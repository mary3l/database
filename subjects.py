import pymongo
import tkinter as tk
from tkinter import messagebox

class SubjectsForm:
    def sujectform():
        #for database connection
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient['enrollmentsystem']
        mycol = mydb["subjects"]

        #two-dimensional list
        lst=[["ID","Code","Description","Units","Schedule"]]

        #to assign to the 2 dimensional list to the grid
        def callback(event):
            li=[]
            li=event.widget._values
            subjectid.set(lst[li[1]][0])
            subjectcode.set(lst[li[1]][1])
            subjectdesc.set(lst[li[1]][2])
            subjectunits.set(lst[li[1]][3])
            subjectsched.set(lst[li[1]][4])

        def creategrid(n):
            lst.clear()
            lst.append(["ID","Code","Description","Units","Schedule"])
            cursor = mycol.find({})
            for text_fromDB in cursor:
                subjid = str(text_fromDB["subjid"])
                subjcode = str(text_fromDB["subjcode"].encode("utf-8").decode("utf-8"))
                subjdesc = str(text_fromDB["subjdesc"].encode("utf-8").decode("utf-8"))
                subjunits = str(text_fromDB["subjunits"])
                subjsched = str(text_fromDB["subjsched"].encode("utf-8").decode("utf-8"))
                lst.append([subjid,subjcode,subjdesc,subjunits,subjsched])
                print(f"{subjid} {subjcode} {subjdesc} {subjunits} {subjsched}")
        #to catch the 2 dimensional list and put it in a multiple entries or the grid
            #i is the row and j is the column
            for i in range(len(lst)):
                    for j in range(len(lst[0])):
                            mgrid = tk.Entry(subjectsWindow, width=25)
                            mgrid.insert(tk.END,lst[i][j])
                            mgrid._values = mgrid.get(), i
                            mgrid.grid(row=i+8, column=j+7)
                            mgrid.bind("<Button-1>", callback)
        #to clear all of the text entries for rows that is greater than 6
            if n==1:
                    for label in subjectsWindow.grid_slaves():
                        if int(label.grid_info()["row"]) > 7:
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
                    newid= mycol.find_one(sort=[("subjid",-1)])["subjid"]
                id=newid+1
                subjectid.set(id)
                mydict = {"subjid":id, "subjcode": subjcode.get(),"subjdesc":subjdesc.get(), "subjunits": int(float(subjunits.get())), "subjsched": subjsched.get()} 
        #to insert one document in the collection "insert_one"
                x = mycol.insert_one(mydict)
                creategrid(1)
                creategrid(0)

        def delete():
            r=msgbox("delete record?","record")
            if r==True:
                #deletes the certain variable in the collection using the ID
                myquery = {"subjid":int(float(subjid.get()))}
                mycol.delete_one(myquery)
                creategrid(1)
                creategrid(0)

        def update():
            option = messagebox.askokcancel("Update", "Update record?")
            if option:
                idQuery = {"subjid": int(float(subjid.get()))}
                updateValues = {
                    "$set": {
                        "subjcode": subjcode.get(),
                        "subjdesc": subjdesc.get(),
                        "subjunits": subjunits.get(),
                        "subjsched": subjsched.get(),
                    }
                }
                mycol.update_one(idQuery, updateValues)
                creategrid(1)
                creategrid(0)

        #Subjects GUI Form
        subjectsWindow = tk.Tk()
        subjectsWindow.title("Subjects Form")
        subjectsWindow.geometry("1050x500")
        subjectsWindow.configure(bg="orange")

        #Subjects Enlisment Form GUI
        label = tk.Label(subjectsWindow,text="Subjects Enlistment Form", width=30, height=1, bg="white", anchor="center")
        label.config(font=("Courier",10))
        label.grid(column=2,row=1)

        #Subject ID
        label = tk.Label(subjectsWindow,text="Subject ID:", width=10, height=1, bg="white")
        label.grid(column=1,row=2)

        subjectid=tk.StringVar(subjectsWindow)
        subjid=tk.Entry(subjectsWindow, textvariable=subjectid)
        subjid.grid(column=2, row=2)
        subjid.configure(state=tk.DISABLED)

        #Subject Code
        label = tk.Label(subjectsWindow,text="Subject Code:", width=15, height=1, bg="white")
        label.grid(column=1,row=3)

        subjectcode=tk.StringVar(subjectsWindow)
        subjcode=tk.Entry(subjectsWindow, textvariable=subjectcode)
        subjcode.grid(column=2, row=3)

        #Subject Description
        label = tk.Label(subjectsWindow,text="Subject Description:", width=15, height=1, bg="white")
        label.grid(column=1,row=4)

        subjectdesc=tk.StringVar(subjectsWindow)
        subjdesc=tk.Entry(subjectsWindow, textvariable=subjectdesc)
        subjdesc.grid(column=2, row=4)

        #Subject Units
        label = tk.Label(subjectsWindow,text="Subject Units:", width=15, height=1, bg="white")
        label.grid(column=1,row=5)

        subjectunits=tk.StringVar(subjectsWindow)
        subjunits=tk.Entry(subjectsWindow, textvariable=subjectunits)
        subjunits.grid(column=2, row=5)

        #Subject Schedule
        label = tk.Label(subjectsWindow,text="Subject Schedule:", width=15, height=1, bg="white")
        label.grid(column=1,row=6)

        subjectsched=tk.StringVar(subjectsWindow)
        subjsched=tk.Entry(subjectsWindow, textvariable=subjectsched)
        subjsched.grid(column=2, row=6)

        creategrid(0)
        #Buttons
        # Save Button
        savebutton = tk.Button(master=subjectsWindow,text = "Save", command=save)
        savebutton.grid(column=1, row=7)
        #Delete Button
        deletebutton = tk.Button(master=subjectsWindow,text = "Delete", command=delete)
        deletebutton.grid(column=2, row=7)                
        #Update Button
        updatebutton = tk.Button(master=subjectsWindow,text = "Update", command=update)
        updatebutton.grid(column=3, row=7)

        subjectsWindow.mainloop()

    
