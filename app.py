from flask import Flask, render_template
import database

app = Flask(__name__)

@app.route("/")
def home():
    jobs = database.list_jobs()
    return render_template("index.html", jobs=jobs)


if __name__ == "__main__":
    app.run(debug=True)