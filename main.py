from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    marks={
        "John":45,
        "Vishnu":60,
        "Rahul":70,
        "Alexa":50,
        "Krish":55,
        "Roshan":70,
        "Neha":65,
        "Mayur":72,
        "Deep":85,
        "Ritesh":24,
        "Jesmine":25,
        "Rishi":23,
        "Raj":22,
        "Rina":20
    }
    return render_template("index.html", marks=marks)
app.run(debug=True)