import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import DateEntry   # for date picker (pip install tkcalendar)

# ---------------- Database Setup ----------------
conn = sqlite3.connect("work_summary.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS work_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    description TEXT,
    summary TEXT
)
""")
conn.commit()

# ---------------- CRUD Functions ----------------
def fetch_records():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM work_summary")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def add_record():
    date = date_entry.get()
    name = name_var.get()
    dept = dept_var.get()
    desc = desc_text.get("1.0", tk.END).strip()
    summary = summary_text.get("1.0", tk.END).strip()

    if not date or not name or not dept:
        messagebox.showwarning("Input Error", "Date, Name, and Department are required!")
        return

    cursor.execute("INSERT INTO work_summary (date, name, department, description, summary) VALUES (?, ?, ?, ?, ?)",
                   (date, name, dept, desc, summary))
    conn.commit()
    fetch_records()
    clear_fields()
    messagebox.showinfo("Success", "Record added successfully!")

def update_record():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select", "Select a record to update")
        return
    values = tree.item(selected, "values")
    record_id = values[0]
    cursor.execute("UPDATE work_summary SET date=?, name=?, department=?, description=?, summary=? WHERE id=?",
                   (date_entry.get(), name_var.get(), dept_var.get(),
                    desc_text.get("1.0", tk.END).strip(),
                    summary_text.get("1.0", tk.END).strip(),
                    record_id))
    conn.commit()
    fetch_records()
    clear_fields()
    messagebox.showinfo("Updated", "Record updated successfully!")

def delete_record():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select", "Select a record to delete")
        return
    values = tree.item(selected, "values")
    record_id = values[0]
    cursor.execute("DELETE FROM work_summary WHERE id=?", (record_id,))
    conn.commit()
    fetch_records()
    clear_fields()
    messagebox.showinfo("Deleted", "Record deleted successfully!")

def clear_fields():
    date_entry.set_date('')
    name_var.set('')
    dept_var.set('')
    desc_text.delete("1.0", tk.END)
    summary_text.delete("1.0", tk.END)

def on_row_select(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, "values")
        date_entry.set_date(values[1])
        name_var.set(values[2])
        dept_var.set(values[3])
        desc_text.delete("1.0", tk.END)
        desc_text.insert(tk.END, values[4])
        summary_text.delete("1.0", tk.END)
        summary_text.insert(tk.END, values[5])

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Daily Work Summary - CRUD Application")
root.geometry("900x600")
root.configure(bg="#020138")

# Variables
name_var = tk.StringVar()
dept_var = tk.StringVar()

# Frame for Form
form_frame = tk.LabelFrame(root, text="Enter Work Details", bg="#85f3ee", padx=10, pady=10, font=("Arial", 12, "bold"))
form_frame.pack(fill="x", padx=10, pady=5)

# Row 1: Date, Name, Department
tk.Label(form_frame, text="Date:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
date_entry = DateEntry(form_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Name:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5, sticky="w")
tk.Entry(form_frame, textvariable=name_var, width=25).grid(row=0, column=3, padx=5, pady=5)

tk.Label(form_frame, text="Department:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=4, padx=5, pady=5, sticky="w")
tk.Entry(form_frame, textvariable=dept_var, width=25).grid(row=0, column=5, padx=5, pady=5)

# Row 2: Description
tk.Label(form_frame, text="Description:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="nw")
desc_text = tk.Text(form_frame, width=40, height=3)
desc_text.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

# Row 3: Work Summary
tk.Label(form_frame, text="Today's Work Summary:", bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5, sticky="nw")
summary_text = tk.Text(form_frame, width=60, height=4)
summary_text.grid(row=2, column=1, columnspan=5, padx=5, pady=5)

# Buttons
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(fill="x", padx=10, pady=5)

tk.Button(btn_frame, text="Add", width=10, bg="#4CAF50", fg="white", command=add_record).pack(side="left", padx=5)
tk.Button(btn_frame, text="Update", width=10, bg="#2196F3", fg="white", command=update_record).pack(side="left", padx=5)
tk.Button(btn_frame, text="Delete", width=10, bg="#f44336", fg="white", command=delete_record).pack(side="left", padx=5)
tk.Button(btn_frame, text="Clear", width=10, bg="#9E9E9E", fg="white", command=clear_fields).pack(side="left", padx=5)

# Data Table
tree_frame = tk.Frame(root)
tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("ID", "Date", "Name", "Department", "Description", "Summary")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=130)
tree.pack(fill="both", expand=True)
tree.bind("<ButtonRelease-1>", on_row_select)

fetch_records()
root.mainloop()
