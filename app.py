from flask import Flask, render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
Scss(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://database.db"
db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now(datetime.UTC))

    def __repr__(self):
        return f"Task {self.id}"


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)