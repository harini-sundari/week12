
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("myform.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("username", "").strip()
    return render_template("greetings.html", name=name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
