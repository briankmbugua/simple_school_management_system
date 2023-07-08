import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
# helper function to help in accessing SQL functions
from sqlalchemy.sql import func

app = Flask(__name__)
# configuring database connection
# the database URI
databaseURI = 'mysql+pymysql://root:password@localhost:3306/student_management_system'
app.config['SQLALCHEMY_DATABASE_URI'] = databaseURI
# disabling tracking of changes in objects in order to save memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Declaring the table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    create_at = db.Column(db.DateTime(timezone=True),
                          server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'

# After initialiazing the database using flask shell and adding some data to it
# Create route and template to display all the students in the database on the index page


# create an index view function which renders a template while passing the student object from the query to render template to be used in populating the frontend
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


# Displaying a single record
# Route that renders a page for each individual student.Use get_or_404() method Flask-SQLAlchemy provides, which is a variant of the get() method.The difference is that get() returns the value None when no result matches the given ID, and get_or_404() returns a 404 Not Found HTTP response


# '<int:student_id>/' here int is a convertor that convers the default string in the URL into an integer.And student_id is the URL variable that determines the student being displayed on the page.
@app.route('/<int:student_id>/')
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student=student)


# Creating a new record using a route for adding new students to the database using web forms.Render a page with a web form where users enter the students data.Then handle form submission, create an object for the new student using the Student model, add it to the session, then commit the transaction

@app.route('/create/', methods=('GET', 'POST'))
def create():
    # handle post from the form in create.html
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        student = Student(firstname=firstname,
                          lastname=lastname,
                          email=email,
                          age=age,
                          bio=bio)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')


# route for editing a record, an /ID/edit/ route to edit the data of the students based on their ID.It fetches the student entry you want to edit using its ID.It extracts the new student via a web form.it then edits the student data, and redirects the user to the index page.

@app.route('/<int:student_id>/edit/', methods=('GET', 'POST'))
def edit(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']

        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.age = age
        student.bio = bio

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('edit.html', student=student)\



# Deleting a Record
# in this step i will add a new route and Delete button for deleting existing students.First i will add a new /id/delete/ route that accepts POST requests.The new delete() view function will receive the ID of the student you want to delete, pass the ID to the get_or_404() query method on the Student model to get it if it exists, or 404 Not found page if no student with the given ID was found on the database.

@app.post('/<int:student_id>/delete/')
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))


"""Here instead of using the usual app.route decorator, you use the app.post decorator introduced in Flask version 2.0.0, which added shortcuts for common HTTP methods.For example, @app.post("/login") is a shortcut for @app.route("/login", methods=["POST"])"""
