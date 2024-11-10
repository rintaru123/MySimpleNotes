import tkinter as tk
from tkinter import scrolledtext, messagebox, Listbox, Scrollbar, Frame, Button
from tkcalendar import Calendar
import sqlite3
from datetime import datetime
from tkinter import ttk

# Creating the DataBase
conn = sqlite3.connect('notes.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY,
    date TEXT,
    content TEXT
)
''')
conn.commit()


def load_notes(date):
    listbox.delete(0, tk.END)
    text_area.delete("1.0", tk.END)
    cursor.execute('SELECT * FROM notes WHERE date=?',(date,))
    for note in cursor.fetchall():
         listbox.insert(tk.END, (note[0],note[1]))

def load_all_notes():
    listbox.delete(0, tk.END)
    text_area.delete("1.0", tk.END)
    cursor.execute('SELECT * FROM notes')
    for note in cursor.fetchall():
         listbox.insert(tk.END, (note[0],note[1]))

def save_note():
    content = text_area.get("1.0", tk.END).strip()
    if content:
        date = calendar.get_date()
        cursor.execute('INSERT INTO notes (date, content) VALUES (?, ?)', (date, content))
        conn.commit()
        load_notes(date)
        text_area.delete("1.0", tk.END)

def update_note():
    try:
        note_id=listbox.get(listbox.curselection()[0])[0]
        content = text_area.get("1.0", tk.END).strip()
        date = calendar.get_date()
        cursor.execute('UPDATE notes SET date=?, content=? WHERE id=?', (date, content, note_id))
        conn.commit()
        load_notes(date)

    except IndexError:
        messagebox.showwarning("Error", "Choose a note.")

def delete_note():
    try:
        date = calendar.get_date()
        note_id=listbox.get(listbox.curselection()[0])[0]
        cursor.execute('DELETE FROM notes WHERE id=?', (note_id,))      
        conn.commit()
        load_notes(date)
        text_area.delete("1.0", tk.END)
    except IndexError:
        messagebox.showwarning("Error", "Choose a note.")

def export_current():
    try:
        note_id=listbox.get(listbox.curselection()[0])[0]
        cursor.execute('SELECT * FROM notes WHERE id=?', (note_id,))
        note = cursor.fetchone()
        with open(f'note_{note[0]}.txt', 'w') as file:
            file.write(f"Date: {note[1]}\nContent:\n{note[2]}")
    except IndexError:
        messagebox.showwarning("Error", "Choose a note.")
        
def export_all():
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    with open('all_notes.txt', 'w') as file:
        for note in notes:
            file.write(f"ID: {note[0]}, Date: {note[1]}\n{note[2]}\n\n")

def on_enter(e):
    myButton1['highlightbackground'] = "white"
    myButton1['highlightthickness'] = 2
    myButton1['bd']=0
    e['background'] = 'green'

def on_leave(e):
    myButton1['highlightbackground'] = "white"
    myButton1['highlightthickness'] = 2
    myButton1['bd']=0
    e['background'] = '#282828'

# GUI

root = tk.Tk()
root.geometry("1000x345")

root.title("Notes App")
root.option_add('*Font', 'Calibri 10')
root.configure(bg="#292929")
root.attributes("-toolwindow", True)
root.resizable("true","false")
style=ttk.Style()
style.theme_use('clam')


frame = Frame(root,bg="white")
frame.pack(side=tk.LEFT,anchor="sw")

listbox = Listbox(root,bg="#292929",fg="white",relief="flat",borderwidth=0, highlightthickness=0,selectbackground="green")
listbox.pack(side=tk.LEFT,fill=tk.Y,ipadx=20,anchor="nw",padx=10)

calendar = Calendar(frame, date_pattern="dd.mm.Y",locale='en_US',
    background="#292929",
    foreground="#E6E6E6",
    disabledbackground ="#292929",
    disabledforeground="#E6E6E6",
    bordercolor="#434343",
    headersbackground="#030303",
    headersforeground="#E6E6E6",
    selectbackground="green",
    selectforeground="white",
    disabledselectbackground="#292929",
    disabledselectforeground="#E6E6E6",
    normalbackground="#494949",
    normalforeground="#E6E6E6",
    weekendbackground="#494949",
    weekendforeground="#E6E6E6",
    othermonthbackground="#292929",
    othermonthforeground="#E6E6E6",
    othermonthwebackground="#292929",
    othermonthweforeground="#E6E6E6",
    disableddaybackground="#292929",
    disableddayforeground="#E6E6E6",    
                    )
calendar.bind("<<CalendarSelected>>",lambda event:load_notes(calendar.get_date()))
calendar.pack()


myButton1=tk.Button(frame, text="Make a new note", command=save_note,bg="#282828",fg="#E6E6E6",highlightbackground = "black",highlightthickness = 2, bd=0)
myButton1.bind("<Enter>",lambda event:on_enter(myButton1))
myButton1.bind("<Leave>",lambda event:on_leave(myButton1))
myButton1.pack(fill=tk.X, expand="true",anchor="sw")

myButton2=tk.Button(frame, text="Show all notes", command=load_all_notes,bg="#282828",fg="#E6E6E6",highlightbackground = "black",highlightthickness = 2, bd=0)
myButton2.bind("<Enter>",lambda event:on_enter(myButton2))
myButton2.bind("<Leave>",lambda event:on_leave(myButton2))
myButton2.pack(fill=tk.X, expand="true",anchor="sw")

myButton3=tk.Button(frame, text="Delete", command=delete_note,bg="#282828",fg="#E6E6E6",highlightbackground = "black",highlightthickness = 2, bd=0)
myButton3.bind("<Enter>",lambda event:on_enter(myButton3))
myButton3.bind("<Leave>",lambda event:on_leave(myButton3))
myButton3.pack(fill=tk.X, expand="true")

myButton4=tk.Button(frame, text="Save", command=update_note,bg="#282828",fg="#E6E6E6",highlightbackground = "black",highlightthickness = 2, bd=0)
myButton4.bind("<Enter>",lambda event:on_enter(myButton4))
myButton4.bind("<Leave>",lambda event:on_leave(myButton4))
myButton4.pack(fill=tk.X, expand="true")

myButton5=tk.Button(frame, text="Export current note", command=export_current,bg="#282828",fg="#E6E6E6",highlightbackground = "black",highlightthickness = 2, bd=0)
myButton5.bind("<Enter>",lambda event:on_enter(myButton5))
myButton5.bind("<Leave>",lambda event:on_leave(myButton5))
myButton5.pack(fill=tk.X, expand="true")

myButton6=tk.Button(frame, text="Export all notes", command=export_all,bg="#282828",fg="#E6E6E6",highlightbackground = "black",highlightthickness = 2, bd=0)
myButton6.bind("<Enter>",lambda event:on_enter(myButton6))
myButton6.bind("<Leave>",lambda event:on_leave(myButton6))
myButton6.pack(fill=tk.X, expand="true")


    


text_area = tk.Text(root,bg="#333333",fg="#E6E6E6",relief="flat",font = ("Calibri", 11),wrap="word",insertbackground="white")
text_area.pack(fill=tk.BOTH, expand="true",anchor="e",padx=5, pady=5,ipadx=10)
listbox.bind("<<ListboxSelect>>", lambda event: load_selected_note())
load_notes(calendar.get_date())

def load_selected_note():
    try:
        note_id=listbox.get(listbox.curselection()[0])[0]
        cursor.execute('SELECT * FROM notes WHERE id=?', (note_id,))
        note = cursor.fetchone()
        if note:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, note[2])
            calendar.selection_set(note[1])

    except IndexError:
        messagebox.showwarning("Error", "Please Choose a note.")
        pass

root.mainloop()

conn.close()

