from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------- Grade Function ----------
def get_grade(mark):
    if mark >= 75:
        return "A"
    elif mark >= 60:
        return "B"
    elif mark >= 50:
        return "C"
    else:
        return "Fail"

# ---------- Home ----------
@app.route("/")
def home():
    search = request.args.get("search")

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    if search:
        cursor.execute("SELECT rowid, name, marks FROM students WHERE name LIKE ?", ('%' + search + '%',))
    else:
        cursor.execute("SELECT rowid, name, marks FROM students")

    data = cursor.fetchall()
    conn.close()

    total = sum([row[2] for row in data]) if data else 0
    average = total / len(data) if data else 0

    return render_template(
        "index.html",
        students=data,
        get_grade=get_grade,
        total=total,
        average=average
    )

# ---------- Add ----------
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

# ---------- Delete ----------
@app.route("/delete/<int:id>")
def delete_student(id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE rowid = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

# ---------- Edit ----------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        marks = int(request.form["marks"])

        cursor.execute(
            "UPDATE students SET name=?, marks=? WHERE rowid=?",
            (name, marks, id)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT name, marks FROM students WHERE rowid=?", (id,))
    student = cursor.fetchone()
    conn.close()

    return render_template("edit.html", student=student, id=id)


if __name__ == "__main__":
    app.run(debug=True)