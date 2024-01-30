from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# Candidate Concept 1: Routes for adding, updating, and deleting todos
# Here we have a route that when called, will add a new todo to the database.
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

# Here we have a route that when called, will update the complete status of a todo in the database.
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

# Here we have a route that when called, will delete a todo from the database.
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route("/")
def home():
    todo_list = Todo.query.all()
    # Candidate Concept 2: Templates
    # Here we are using the render_template function to render the base.html template as a file, passing the todo_list as a variable to the template.
    return render_template("base.html", todo_list=todo_list)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)