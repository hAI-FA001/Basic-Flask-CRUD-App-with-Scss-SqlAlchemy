from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, UTC


app = Flask(__name__)
Scss(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"  # triple / means relative path
db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now(UTC))

    def __repr__(self):
        return f"Task {self.id}"


@app.route("/", methods=["GET", "POST"])
def index():
    # Add Task
    if request.method == "POST":
        cur_task = request.form['content']
        new_task = MyTask(content=cur_task)
        # send new MyTask to DB
        try:
            db.session.add(new_task)
            db.session.commit()
            # return the homepage
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    # See Tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id: int):
    # won't get 404 cuz this route is only reached if Task is present
    del_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(del_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Error {e}")
        return f"Error {e}"

@app.route("/edit/<int:id>")
def edit(id: int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error {e}")
            return f"Error {e}"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)