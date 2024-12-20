import tkinter as tk
from tkinter import scrolledtext, messagebox, Listbox, Scrollbar, Frame, Button
from tkcalendar import Calendar
import sqlite3
from datetime import datetime
from tkinter import ttk
from configparser import ConfigParser

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

#dictionary as a container for all notes
global notes_dict
notes_dict={}

#loading notes from db
def load_notes(date):
    listbox.delete(0, tk.END)
    text_area.delete("1.0", tk.END)
    cursor.execute('SELECT * FROM notes WHERE date=? ORDER BY date ASC',(date,))
    global notes_dict
    notes_dict={}
    notes_num=1
    for note in cursor.fetchall():
         notes_dict.update({notes_num:[note[0],note[1],note[2]]})
         #listbox.insert(tk.END, (note[0],note[1]))
         listbox.insert(tk.END,"{0}...".format(notes_dict[notes_num][2][:20]))
         notes_num+=1
    if notes_dict:
        listbox.select_set(tk.END)
        load_selected_note()

def load_all_notes():
    listbox.delete(0, tk.END)
    text_area.delete("1.0", tk.END)
    cursor.execute('SELECT * FROM notes ORDER BY date ASC')
    global notes_dict
    notes_dict={}
    notes_num=1
    for note in cursor.fetchall():
         notes_dict.update({notes_num:[note[0],note[1],note[2]]})
         #listbox.insert(tk.END, (note[0],note[1]))
         listbox.insert(tk.END,"{0} {1}...".format(notes_dict[notes_num][1],notes_dict[notes_num][2][:15]))
         notes_num+=1
    if notes_dict:
        listbox.select_set(tk.END)
        load_selected_note()

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
        note_id=notes_dict[listbox.curselection()[0]+1][0]
        content = text_area.get("1.0", tk.END).strip()
        date = calendar.get_date()
        cursor.execute('UPDATE notes SET date=?, content=? WHERE id=?', (date, content, note_id))
        conn.commit()
        load_notes(date)

    except IndexError:
        messagebox.showwarning(error_name, error_name2)

def delete_note():
    try:
        date = calendar.get_date()
        note_id=notes_dict[listbox.curselection()[0]+1][0]
        cursor.execute('DELETE FROM notes WHERE id=?', (note_id,))      
        conn.commit()
        load_notes(date)
        text_area.delete("1.0", tk.END)
    except IndexError:
        messagebox.showwarning(error_name, error_name2)

def export_current():
    try:
        note_id=notes_dict[listbox.curselection()[0]+1][0]
        cursor.execute('SELECT * FROM notes WHERE id=?', (note_id,))
        note = cursor.fetchone()
        with open(f'note_{note[0]}.txt', 'w') as file:
            file.write(f"{export_date_name}: {note[1]}\nContent:\n{note[2]}")
    except IndexError:
        messagebox.showwarning(error_name, error_name2)
        
def export_all():
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    with open('all_notes.txt', 'w') as file:
        for note in notes:
            file.write(f"ID: {note[0]}, {export_date_name}: {note[1]}\n{note[2]}\n\n",)

def on_enter(e):
    myButton1['highlightbackground'] = text_background_color
    myButton1['highlightthickness'] = 2
    myButton1['bd']=0
    e['background'] = special_color

def on_leave(e):
    myButton1['highlightbackground'] = text_background_color
    myButton1['highlightthickness'] = 2
    myButton1['bd']=0
    e['background'] = main_background_color

def load_selected_note():
    try:
        note_id=notes_dict[listbox.curselection()[0]+1][0]
        cursor.execute('SELECT * FROM notes WHERE id=?', (note_id,))
        note = cursor.fetchone()
        if note:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, note[2])
            calendar.selection_set(note[1])
            text_area.focus_set()

    except IndexError:
        messagebox.showwarning(error_name, error_name2)
        pass

def set_today():
    calendar.selection_set(datetime.now().strftime('%y.%m.%d'))
    load_notes(calendar.get_date())

#reading config
config = ConfigParser()
config.read("config.ini")

#read locales
language = config.get("LOCALE", "language")
language_section = language.upper()
config.read("locales/{}.ini".format(language),encoding='utf-8')

#read locales for instruments
calendar_locale=config.get(language_section, "cal_locale")
error_name=config.get(language_section, "error_k")
error_name2=config.get(language_section, "error_k2")
button_save=config.get(language_section, "saveButton")
button_new_note=config.get(language_section, "newNoteButton")
button_show_all_notes=config.get(language_section,"showAllNotes")
button_delete=config.get(language_section,'deleteButton')
button_export_current_note=config.get(language_section,'exportCurrentNote')
button_export_all_notes=config.get(language_section,'exportAllNotes')
button_set_today=config.get(language_section,'setToday')
export_date_name=config.get(language_section,'exportDateName')
main_background_color=config.get("Settings","mainBackgroundColor")
second_background_color=config.get("Settings","secondBackgroundColor")
text_background_color=config.get("Settings","textBackgroundColor")
special_color=config.get("Settings","specialColor")

# GUI
root = tk.Tk()
root.geometry("1000x445")
root.title("My Simple Notes")
root.option_add('*Font', 'Calibri 10')
root.configure(bg=main_background_color)
root.attributes("-toolwindow", True)
root.resizable("true","true")
style=ttk.Style()
style.theme_use('clam')

frame = Frame(root,bg=text_background_color)
frame.pack(side=tk.LEFT,fill=tk.Y, anchor="w")


calendar = Calendar(frame, date_pattern="Y.mm.dd",locale=calendar_locale,
    background=main_background_color,
    foreground=text_background_color,
    disabledbackground =main_background_color,
    disabledforeground=text_background_color,
    bordercolor="#434343",
    headersbackground="#030303",
    headersforeground=text_background_color,
    selectbackground=special_color,
    selectforeground=text_background_color,
    disabledselectbackground=main_background_color,
    disabledselectforeground=text_background_color,
    normalbackground=second_background_color,
    normalforeground=text_background_color,
    weekendbackground=second_background_color,
    weekendforeground=text_background_color,
    othermonthbackground=main_background_color,
    othermonthforeground=text_background_color,
    othermonthwebackground=main_background_color,
    othermonthweforeground=text_background_color,
    disableddaybackground=main_background_color,
    disableddayforeground=text_background_color,    
                    )
calendar.bind("<<CalendarSelected>>",lambda event:load_notes(calendar.get_date()))
calendar.pack()

frame2 = Frame(frame,bg=text_background_color)
frame2.pack(fill=tk.X, expand="true",anchor="n")

myButton7=tk.Button(frame2, text=button_set_today, command=set_today,bg="#282828",fg=text_background_color,highlightbackground = "black",highlightthickness = 2, bd=0)
myButton7.bind("<Enter>",lambda event:on_enter(myButton7))
myButton7.bind("<Leave>",lambda event:on_leave(myButton7))
myButton7.pack(fill=tk.X, expand="true",anchor="n")

myButton1=tk.Button(frame2, text=button_new_note, command=save_note,bg="#282828",fg=text_background_color, highlightbackground ="black",highlightthickness = 2, bd=0)
myButton1.bind("<Enter>",lambda event:on_enter(myButton1))
myButton1.bind("<Leave>",lambda event:on_leave(myButton1))
myButton1.pack(fill=tk.X, expand="true",anchor="n")

myButton2=tk.Button(frame2, text=button_show_all_notes, command=load_all_notes,bg="#282828",fg=text_background_color, highlightbackground = "black",highlightthickness = 2, bd=0)
myButton2.bind("<Enter>",lambda event:on_enter(myButton2))
myButton2.bind("<Leave>",lambda event:on_leave(myButton2))
myButton2.pack(fill=tk.X, expand="true",anchor="n")

myButton3=tk.Button(frame2, text=button_delete, command=delete_note,bg="#282828",fg=text_background_color, highlightbackground = "black",highlightthickness = 2, bd=0)
myButton3.bind("<Enter>",lambda event:on_enter(myButton3))
myButton3.bind("<Leave>",lambda event:on_leave(myButton3))
myButton3.pack(fill=tk.X, expand="true",anchor="n")

myButton4=tk.Button(frame2, text=button_save, command=update_note,bg="#282828",fg=text_background_color,highlightbackground = "black",highlightthickness = 2, bd=0)
myButton4.bind("<Enter>",lambda event:on_enter(myButton4))
myButton4.bind("<Leave>",lambda event:on_leave(myButton4))
myButton4.pack(fill=tk.X, expand="true",anchor="n")

myButton5=tk.Button(frame2, text=button_export_current_note, command=export_current,bg="#282828",fg=text_background_color,highlightbackground = "black",highlightthickness = 2, bd=0)
myButton5.bind("<Enter>",lambda event:on_enter(myButton5))
myButton5.bind("<Leave>",lambda event:on_leave(myButton5))
myButton5.pack(fill=tk.X, expand="true",anchor="n")

myButton6=tk.Button(frame2, text=button_export_all_notes, command=export_all,bg="#282828",fg=text_background_color,highlightbackground = "black",highlightthickness = 2, bd=0)
myButton6.bind("<Enter>",lambda event:on_enter(myButton6))
myButton6.bind("<Leave>",lambda event:on_leave(myButton6))
myButton6.pack(fill=tk.X, expand="true",anchor="n")

listbox = Listbox(frame,bg=main_background_color,fg=text_background_color,relief="flat",borderwidth=0, highlightthickness=0,selectbackground=special_color)
listbox.pack(fill=tk.BOTH,anchor="n",expand="true")

text_area = tk.Text(root,bg="#333333",fg=text_background_color,relief="flat",font = ("Calibri", 11),wrap="word",insertbackground=text_background_color)
text_area.pack(fill=tk.BOTH, expand="true",anchor="e",padx=5, pady=5,ipadx=10)
text_area.focus_set()

listbox.bind("<<ListboxSelect>>", lambda event: load_selected_note())
load_notes(calendar.get_date())

root.mainloop()
conn.close()

