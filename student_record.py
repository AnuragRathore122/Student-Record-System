import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ---------------- DATABASE ----------------

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT,
    email TEXT
)
""")

conn.commit()


# ---------------- FUNCTIONS ----------------

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_course.delete(0, tk.END)
    entry_email.delete(0, tk.END)


def show_students():
    for item in student_table.get_children():
        student_table.delete(item)

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    for row in rows:
        student_table.insert("", tk.END, values=row)


def add_student():
    name = entry_name.get()
    age = entry_age.get()
    course = entry_course.get()
    email = entry_email.get()

    if name == "" or age == "" or course == "" or email == "":
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number!")
        return

    cursor.execute(
        "INSERT INTO students (name, age, course, email) VALUES (?, ?, ?, ?)",
        (name, age, course, email)
    )

    conn.commit()

    messagebox.showinfo("Success", "Student added successfully!")

    clear_fields()
    show_students()


def select_student(event):
    selected = student_table.focus()

    if not selected:
        return

    values = student_table.item(selected, "values")

    if values:
        clear_fields()

        entry_name.insert(0, values[1])
        entry_age.insert(0, values[2])
        entry_course.insert(0, values[3])
        entry_email.insert(0, values[4])


def update_student():
    selected = student_table.focus()

    if not selected:
        messagebox.showwarning("Warning", "Please select a student!")
        return

    values = student_table.item(selected, "values")
    student_id = values[0]

    name = entry_name.get()
    age = entry_age.get()
    course = entry_course.get()
    email = entry_email.get()

    if name == "" or age == "" or course == "" or email == "":
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    cursor.execute("""
        UPDATE students
        SET name=?, age=?, course=?, email=?
        WHERE id=?
    """, (name, age, course, email, student_id))

    conn.commit()

    messagebox.showinfo("Success", "Student updated successfully!")

    clear_fields()
    show_students()


def delete_student():
    selected = student_table.focus()

    if not selected:
        messagebox.showwarning("Warning", "Please select a student!")
        return

    values = student_table.item(selected, "values")
    student_id = values[0]

    answer = messagebox.askyesno(
        "Confirm Delete",
        "Do you want to delete this student?"
    )

    if answer:
        cursor.execute(
            "DELETE FROM students WHERE id=?",
            (student_id,)
        )

        conn.commit()

        messagebox.showinfo("Success", "Student deleted successfully!")

        clear_fields()
        show_students()


def search_student():
    search_text = entry_search.get()

    for item in student_table.get_children():
        student_table.delete(item)

    cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE ? OR course LIKE ?
    """, (
        "%" + search_text + "%",
        "%" + search_text + "%"
    ))

    rows = cursor.fetchall()

    for row in rows:
        student_table.insert("", tk.END, values=row)


# ---------------- GUI WINDOW ----------------

root = tk.Tk()
root.title("Student Record Management System")
root.geometry("850x600")
root.resizable(False, False)


# ---------------- TITLE ----------------

title = tk.Label(
    root,
    text="STUDENT RECORD MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold")
)

title.pack(pady=15)


# ---------------- INPUT FRAME ----------------

input_frame = tk.Frame(root)
input_frame.pack(pady=10)


tk.Label(input_frame, text="Name:", font=("Arial", 11)).grid(
    row=0, column=0, padx=10, pady=8
)

entry_name = tk.Entry(input_frame, width=25)
entry_name.grid(row=0, column=1)


tk.Label(input_frame, text="Age:", font=("Arial", 11)).grid(
    row=0, column=2, padx=10, pady=8
)

entry_age = tk.Entry(input_frame, width=15)
entry_age.grid(row=0, column=3)


tk.Label(input_frame, text="Course:", font=("Arial", 11)).grid(
    row=1, column=0, padx=10, pady=8
)

entry_course = tk.Entry(input_frame, width=25)
entry_course.grid(row=1, column=1)


tk.Label(input_frame, text="Email:", font=("Arial", 11)).grid(
    row=1, column=2, padx=10, pady=8
)

entry_email = tk.Entry(input_frame, width=25)
entry_email.grid(row=1, column=3)


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(root)
button_frame.pack(pady=10)


tk.Button(
    button_frame,
    text="Add Student",
    width=15,
    command=add_student
).grid(row=0, column=0, padx=5)


tk.Button(
    button_frame,
    text="Update Student",
    width=15,
    command=update_student
).grid(row=0, column=1, padx=5)


tk.Button(
    button_frame,
    text="Delete Student",
    width=15,
    command=delete_student
).grid(row=0, column=2, padx=5)


tk.Button(
    button_frame,
    text="Clear",
    width=15,
    command=clear_fields
).grid(row=0, column=3, padx=5)


# ---------------- SEARCH ----------------

search_frame = tk.Frame(root)
search_frame.pack(pady=10)


tk.Label(
    search_frame,
    text="Search:",
    font=("Arial", 11)
).pack(side=tk.LEFT)


entry_search = tk.Entry(search_frame, width=30)
entry_search.pack(side=tk.LEFT, padx=10)


tk.Button(
    search_frame,
    text="Search",
    command=search_student
).pack(side=tk.LEFT)


tk.Button(
    search_frame,
    text="Show All",
    command=show_students
).pack(side=tk.LEFT, padx=5)


# ---------------- TABLE ----------------

table_frame = tk.Frame(root)
table_frame.pack(pady=10)


columns = ("ID", "Name", "Age", "Course", "Email")

student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=12
)


for column in columns:
    student_table.heading(column, text=column)
    student_table.column(column, width=140)


student_table.pack()


student_table.bind(
    "<<TreeviewSelect>>",
    select_student
)


# ---------------- START ----------------

show_students()

root.mainloop()

conn.close()