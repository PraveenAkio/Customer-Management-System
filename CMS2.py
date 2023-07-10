from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import mysql.connector
import csv
import os
import sys

mydata = []

def update(rows):
    global mydata
    mydata = rows
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert('', 'end', values=i)

def search():
    q2 = q.get()
    query = "SELECT id, name, email, age FROM customers WHERE name LIKE '%"+q2+"%' OR email LIKE '%"+q2+"%'"
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)

def clear():
    query = "SELECT id, name, email, age FROM customers"
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)

def getrow(event):
    rowid = trv.identify_row(event.y)
    item = trv.item(trv.focus())
    t1.set(item['values'][0])
    t2.set(item['values'][1])
    t3.set(item['values'][2])
    t4.set(item['values'][3])

def update_customer():
    name = t2.get()
    email = t3.get()
    age = t4.get()
    custid = t1.get()

    if messagebox.askyesno("Confirm Please", "Are you sure you want to UPDATE this customer?"):
        query = "UPDATE customers SET name = %s, email = %s, age = %s WHERE id = %s"
        cursor.execute(query, (name, email, age, custid))
        mydb.commit()
        clear()
    else:
        return True

def add_new():
    name = t2.get()
    email = t3.get()
    age = t4.get()
    if messagebox.askyesno("Confirm Please", "Are you sure you want to ADD this customer?"):
        query = "INSERT INTO customers(id, name, email, age) VALUES(NULL, %s, %s, %s)"
        cursor.execute(query, (name, email, age))
        mydb.commit()
        clear()
    else:
        return True

def delete_customer():
    customer_id = t1.get()
    if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this customer?"):
        query = "DELETE FROM customers WHERE id = "+customer_id
        cursor.execute(query)
        mydb.commit()
        clear()
    else:
        return True

def export():
    if len(mydata) < 1:
        messagebox.showerror("No Data", "No data available to export")
        return False

    fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
    with open(fln, mode='w') as myfile:
        exp_writer = csv.writer(myfile, delimiter=',', lineterminator = '\n')
        for i in mydata:
            exp_writer.writerow(i)
    messagebox.showinfo("Data Exported", "Your data has been exported to "+os.path.basename(fln)+ " successfully.")

def importcsv():
    mydata.clear()
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
    with open(fln) as myfile:
        csvread = csv.reader(myfile, delimiter=',')
        for i in csvread:
            mydata.append(i)
    update(mydata)
    messagebox.showinfo("Data Imported", "Your data has been imported successfully.")

def savedb():
    if messagebox.askyesno("Confirmation", "Are you sure you want to save data to Database"):
        for i in mydata:
            id = i[0]
            name = i[1]
            email = i[2]
            age = i[3]
            query = "INSERT INTO customers(id, name, email, age) VALUES(NULL, %s, %s, %s)"
            cursor.execute(query, (name, email, age))
        mydb.commit()
        clear()
        messagebox.showinfo("Data Saved", "Data has been saved to Database successfully.")
    else:
        return False

mydb = mysql.connector.connect(host="localhost", user="root", passwd="Uzumaki_706", database="test")
cursor = mydb.cursor()

root = tk.Tk()

#Login Program Section
top = Toplevel()

top.title("LogIn")
top.geometry('450x450')
top.configure(bg='#333333')

username_entry = Entry(top) #Username entry
password_entry = Entry(top) #Password entry

def login():
    username = "user"
    password = "123"
    if username_entry.get()==username and password_entry.get()==password:
        messagebox.showinfo(title="Login Success", message="You successfully logged in.")
        root.deiconify()
        top.destroy()
    else:
        messagebox.showerror(title="Error", message="Invalid login.")

def cancel():
    top.destroy() #Removes the toplevel window
    root.destroy() #Removes the hidden root window
    sys.exit() #Ends the script

# Creating widgets
login_label = tk.Label(top, text="Login", bg='#333333', fg="#FF7900", font=("Arial", 30))
username_label = tk.Label(top, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = tk.Entry(top, font=("Arial", 16))
password_entry = tk.Entry(top, show="*", font=("Arial", 16))
password_label = tk.Label(top, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_button = tk.Button(top, text="Login", bg="GREEN", fg="#FFFFFF", font=("Arial", 16), command=lambda:login())
cancel_button = tk.Button(top, text="Cancel", bg="RED", fg="#FFFFFF", font=("Arial", 16), command=lambda:cancel())

# Placing widgets on the screen
login_label.grid(row=0, column=1, columnspan=1, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=1, columnspan=1, pady=20)
cancel_button.grid(row=4, column=1, columnspan=1, pady=20)

login_img = PhotoImage(file='login.png')
top.iconphoto(False,login_img)
top.resizable(False,False)
root.withdraw()

#Main Program Section
q = StringVar()
t1 = StringVar()
t2 = StringVar()
t3 = StringVar()
t4 = StringVar()

root.configure(bg="#333333")
root.title("Customer Management System")
root.geometry("800x680")
root.resizable(False, False)
main_img = PhotoImage(file='user.png')
root.iconphoto(False,main_img)

wrapper1 = LabelFrame(root, text = "Customer List")
wrapper2 = LabelFrame(root, text = "Search and Modify Data")
wrapper3 = LabelFrame(root, text = "Customer Data")

wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

trv = ttk.Treeview(wrapper1, columns=(1,2,3,4), show="headings", height="7")
trv.pack(side=LEFT)
trv.place(x=0, y=0)

trv.heading(1, text="Customer ID")
trv.heading(2, text="Name")
trv.heading(3, text="Email")
trv.heading(4, text="Age")

trv.bind('<Double 1>', getrow)

#vertical scrollbar
yscrollbar = ttk.Scrollbar(wrapper1 , orient="vertical", command=trv.yview)
yscrollbar.pack(side=RIGHT, fill="y")

trv.configure(yscrollcommand=yscrollbar.set)

query = "SELECT id, name, email, age from customers"
cursor.execute(query)
rows = cursor.fetchall()
update(rows)

#Search Section
lbl = Label(wrapper2, text="Search")
lbl.pack(side=tk.LEFT, padx=10)
ent = Entry(wrapper2, textvariable=q)
ent.pack(side=tk.LEFT, padx=6)
btn = Button(wrapper2, text="Search", command=search)
btn.pack(side=tk.LEFT, padx=6)
cbtn = Button(wrapper2, text="Clear", command=clear)
cbtn.pack(side=tk.LEFT, padx=6)

extbtn = Button(wrapper2, text="Exit", command=lambda: exit())
extbtn.pack(side=tk.LEFT, padx=6)

savebtn = Button(wrapper2, text="Save Data", command=savedb)
savebtn.pack(side=tk.RIGHT, padx=10, pady=10)

expbtn = Button(wrapper2, text="Export CSV", command=export)
expbtn.pack(side=tk.RIGHT, padx=10, pady=10)
impbtn = Button(wrapper2, text="Import CSV", command=importcsv)
impbtn.pack(side=tk.RIGHT, padx=10, pady=10)

#User Data Section
lbl1 = Label(wrapper3, text="Customer ID")
lbl1.grid(row=0, column=0, padx=5, pady=3)
ent1 = Entry(wrapper3, textvariable=t1)
ent1.grid(row=0, column=1, padx=5, pady=3)

lbl2 = Label(wrapper3, text="Name")
lbl2.grid(row=1, column=0, padx=5, pady=3)
ent2 = Entry(wrapper3, textvariable=t2)
ent2.grid(row=1, column=1, padx=5, pady=3)

lbl3 = Label(wrapper3, text="Email")
lbl3.grid(row=2, column=0, padx=5, pady=3)
ent3 = Entry(wrapper3, textvariable=t3)
ent3.grid(row=2, column=1, padx=5, pady=3)

lbl4 = Label(wrapper3, text="Age")
lbl4.grid(row=3, column=0, padx=5, pady=3)
ent4 = Entry(wrapper3, textvariable=t4)
ent4.grid(row=3, column=1, padx=5, pady=3)

up_btn = Button(wrapper3, text="Update", command=update_customer)
add_btn = Button(wrapper3, text="Add New", command=add_new)
delete_btn = Button(wrapper3, text="Delete", command=delete_customer)

add_btn.grid(row=4, column=0, padx=5, pady=3)
up_btn.grid(row=4, column=1, padx=5, pady=3)
delete_btn.grid(row=4, column=2, padx=5, pady=3)

top.mainloop()
root.mainloop()