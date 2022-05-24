from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost:5432/postgres"

db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    # For debug purpose
    def __repr__(self):
        return f'<Person ID: {self.id} name: {self.name}>'


# create the persons table if it does not exist
db.create_all()


@app.route("/")
def index():
    # Getting the first name from the database
    person = Person.query.first()
    return "Hi " + person.name


# Running the server
if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
