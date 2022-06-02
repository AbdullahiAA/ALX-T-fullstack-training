from ast import Or
from os import abort
import sys
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import null

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/todoappcrud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    # This is a foreign key that references the todoList id
    todolists_id = db.Column(
        db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description} {self.completed}, list {self.todolists_id}>'


class TodoList(db.Model):
    __tablename__ = 'todolists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    # This is what defines the relationship between this table and the todos table
    todos = db.relationship('Todo', backref="list", lazy=True)

    def __repr__(self):
        return f'<TodoList {self.id} {self.name}>'


@app.route("/todos/create", methods=['POST'])
def create_todo():
    # This is used to track when an error occurred
    error = False

    try:
        # Fetch the description from the request body
        description = request.get_json()['description']
        todolists_id = request.get_json()['todolists_id']

        # Instantiate a new Todo object
        todo = Todo(description=description, todolists_id=todolists_id)

        db.session.add(todo)
        db.session.commit()
    except:
        error = True

        # Roll back the changes
        db.session.rollback()

        # Print the system execution error
        print(sys.exc_info())
    finally:
        db.session.close()

        # Return the data if there is no error
        if error:
            abort(400)
        else:
            return jsonify({'description': description, 'todolists_id': todolists_id})


@app.route("/todos/updateStatus/<todo_id>", methods=['PUT'])
def update_status(todo_id):
    error = False
    try:
        status = request.get_json()['completed']

        todo = Todo.query.get(todo_id)
        todo.completed = status
        db.session.commit()

        print(todo)
    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()

    finally:
        db.session.close()

        if error:
            abort(400)
        else:
            return jsonify({'completed': status})


@app.route("/todos/delete/<todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    error = False

    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()

    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()

    finally:
        db.session.close()

        if error:
            abort(400)
        else:
            return jsonify({'success': True})


@app.route("/lists/create", methods=['POST'])
def create_list():
    # This is used to track when an error occurred
    error = False

    try:
        # Fetch the name from the request body
        name = request.get_json()['name']

        # Instantiate a new TodoList object
        todoList = TodoList(name=name)

        db.session.add(todoList)
        db.session.commit()
    except:
        error = True

        # Roll back the changes
        db.session.rollback()

        # Print the system execution error
        print(sys.exc_info())
    finally:
        db.session.close()

        # Return the data if there is no error
        if error:
            abort(400)
        else:
            return jsonify({'name': name})


@app.route("/lists/delete/<list_id>", methods=['DELETE'])
def delete_list(list_id):
    error = False

    try:
        todoList = TodoList.query.get(list_id)

        for todo in todoList.todos:
            db.session.delete(todo)

        db.session.delete(todoList)
        db.session.commit()

    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()

    finally:
        db.session.close()

        if error:
            abort(400)
        else:
            return jsonify({'name': 'Roll'})


@app.route("/lists/<list_id>")
def get_list_todos(list_id):
    # Fetch all the todos based on the list id
    todos = Todo.query.filter_by(todolists_id=list_id).order_by('id').all()

    lists = TodoList.query.all()
    active_list = TodoList.query.get(list_id)

    return render_template('index.html', todos=todos, lists=lists, active_list=active_list)


@app.route("/")
def index():
    first_list_id = TodoList.query.first()

    if first_list_id:
        print('Exist')
        return redirect(url_for('get_list_todos', list_id=first_list_id.id))
    else:
        print('Not exist')
        return redirect(url_for('get_list_todos', list_id=1))

    # if not first_list_id.id:

    #     # Redirect to the list route
    # else:


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
