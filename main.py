from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    marks = {
        "John": 45,
        "Vishnu": 60,
        "Rahul": 70,
        "Mayur": 72,
        "Roshan": 70,
        "Neha": 65,
        "Deep": 85
    }

    def get_grade(mark):
        if mark >= 75:
            return "A"
        elif mark >= 60:
            return "B"
        elif mark >= 50:
            return "C"
        else:
            return "Fail"

    total = sum(marks.values())
    average = total / len(marks)

    return render_template(
        "index.html",
        marks=marks,
        get_grade=get_grade,
        total=total,
        average=average
    )

if __name__ == "__main__":
    app.run(debug=True)