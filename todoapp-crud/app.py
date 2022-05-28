from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/todoapp'
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description} {self.completed}>'


db.create_all()


@app.route("/todos/create", methods=['POST'])
def create_todo():
    description = request.form['description']

    todo = Todo(description=description)

    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))


@app.route("/")
def index():
    # Fetch all the todos
    data = Todo.query.all()

    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
