from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/postgres'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    # Debug purpose
    def __repr__(self):
        return f'<User ID: {self.id} name: {self.name}>'


db.create_all()


@app.route("/")
def index():
    return 'Model.query excercise is on the gooo...'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
