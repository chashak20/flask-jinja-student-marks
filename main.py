from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            marks INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_grade(mark):
    if mark >= 75:
        return "A"
    elif mark >= 60:
        return "B"
    elif mark >= 50:
        return "C"
    else:
        return "Fail"

@app.route("/")
def home():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, marks FROM students")
    data = cursor.fetchall()
    conn.close()

    total = sum([row[1] for row in data]) if data else 0
    average = total / len(data) if data else 0

    return render_template(
        "index.html",
        students=data,
        get_grade=get_grade,
        total=total,
        average=average
    )

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        marks = int(request.form["marks"])

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, marks) VALUES (?, ?)", (name, marks))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)