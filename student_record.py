import streamlit as st
import sqlite3
import pandas as pd


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Record System",
    page_icon="🎓",
    layout="wide"
)


# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 18px;
    margin-bottom: 30px;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- DATABASE ----------------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

conn.commit()


# ---------------- FUNCTIONS ----------------

def get_students():
    return pd.read_sql_query(
        "SELECT * FROM students ORDER BY id DESC",
        conn
    )


def add_student(name, age, course, email):

    cursor.execute(
        """
        INSERT INTO students (name, age, course, email)
        VALUES (?, ?, ?, ?)
        """,
        (name, age, course, email)
    )

    conn.commit()


def update_student(student_id, name, age, course, email):

    cursor.execute(
        """
        UPDATE students
        SET name = ?, age = ?, course = ?, email = ?
        WHERE id = ?
        """,
        (name, age, course, email, student_id)
    )

    conn.commit()


def delete_student(student_id):

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()


# ---------------- TITLE ----------------

st.markdown(
    '<p class="main-title">🎓 Student Record System</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Manage student records easily and efficiently</p>',
    unsafe_allow_html=True
)


# ---------------- SIDEBAR ----------------

st.sidebar.title("🎓 Navigation")

menu = st.sidebar.radio(
    "Select an option",
    [
        "📊 Dashboard",
        "➕ Add Student",
        "✏️ Update Student",
        "🗑️ Delete Student"
    ]
)


# ================= DASHBOARD =================

if menu == "📊 Dashboard":

    students = get_students()

    # Statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            len(students)
        )

    with col2:
        if len(students) > 0:
            st.metric(
                "📚 Total Courses",
                students["course"].nunique()
            )
        else:
            st.metric("📚 Total Courses", 0)

    with col3:
        if len(students) > 0:
            st.metric(
                "🎂 Average Age",
                round(students["age"].mean(), 1)
            )
        else:
            st.metric("🎂 Average Age", 0)

    st.divider()

    st.subheader("📋 Student Records")

    # Search
    search = st.text_input(
        "🔍 Search by Name or Course"
    )

    if len(students) > 0:

        if search:
            students = students[
                students["name"].str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                students["course"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            students,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No student records found. Add your first student! 🎓")


# ================= ADD STUDENT =================

elif menu == "➕ Add Student":

    st.header("➕ Add New Student")

    with st.form("add_student_form"):

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("👤 Student Name")
            age = st.number_input(
                "🎂 Age",
                min_value=1,
                max_value=100,
                value=18
            )

        with col2:
            course = st.text_input("📚 Course")
            email = st.text_input("📧 Email")

        submitted = st.form_submit_button(
            "➕ Add Student",
            use_container_width=True
        )

        if submitted:

            if name and course and email:

                add_student(
                    name,
                    age,
                    course,
                    email
                )

                st.success(
                    f"🎉 {name} has been added successfully!"
                )

            else:
                st.error(
                    "⚠️ Please fill in all fields!"
                )


# ================= UPDATE STUDENT =================

elif menu == "✏️ Update Student":

    st.header("✏️ Update Student Record")

    students = get_students()

    if len(students) > 0:

        student_id = st.selectbox(
            "Select Student ID",
            students["id"].tolist()
        )

        selected_student = students[
            students["id"] == student_id
        ].iloc[0]

        with st.form("update_student_form"):

            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input(
                    "👤 Student Name",
                    value=selected_student["name"]
                )

                age = st.number_input(
                    "🎂 Age",
                    min_value=1,
                    max_value=100,
                    value=int(selected_student["age"])
                )

            with col2:
                course = st.text_input(
                    "📚 Course",
                    value=selected_student["course"]
                )

                email = st.text_input(
                    "📧 Email",
                    value=selected_student["email"]
                )

            submitted = st.form_submit_button(
                "💾 Update Student",
                use_container_width=True
            )

            if submitted:

                update_student(
                    student_id,
                    name,
                    age,
                    course,
                    email
                )

                st.success(
                    "✅ Student record updated successfully!"
                )

                st.rerun()

    else:
        st.warning(
            "⚠️ No students available to update."
        )


# ================= DELETE STUDENT =================

elif menu == "🗑️ Delete Student":

    st.header("🗑️ Delete Student")

    students = get_students()

    if len(students) > 0:

        student_id = st.selectbox(
            "Select Student to Delete",
            students["id"].tolist()
        )

        selected_student = students[
            students["id"] == student_id
        ].iloc[0]

        st.warning(
            f"""
            You are about to delete:

            **Name:** {selected_student['name']}

            **Course:** {selected_student['course']}
            """
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this student"
        )

        if st.button(
            "🗑️ Delete Student",
            use_container_width=True
        ):

            if confirm:

                delete_student(student_id)

                st.success(
                    "🗑️ Student deleted successfully!"
                )

                st.rerun()

            else:
                st.error(
                    "⚠️ Please confirm before deleting!"
                )

    else:
        st.info(
            "No students available to delete."
        )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "🎓 Student Record Management System | Built with Python, Streamlit & SQLite"
)
