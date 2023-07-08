# Student management system
A small student management system to demonstrate how to use the Flask-SQLAlchemy extension
# 1.Install Flask and Flask-SQLAlchemy
# 2.Setting up the Database and Model
In this step, i'll set up the database connection, and create an SQLAlchemy database model, which is a python class that represents the table that stores your data.I'll initiate the database, create a table for students based on the model declared, and add a few students into the students table
# Setting up the database connection
the database URI and other configurations which are put in app.config
# Creating the database
set the app.py file as your Flask application using the FLASK_APP enviromental variable.
Import the database and the Model in this case student, then use db.create_all() method to create the table in the database
# NOTE:
The db.create_all() function does not recreate or update a table if it already exists in the database.To modify the model you have to delete all existing database tables with db.drop_all() function and then recreate the with db.create all().This will apply the modifications you make to your models, but will also delete all the existing data in the database.To update the database and preserve existing data you'll need to use schema migration which allows you to modify your tables and preserve data.
```bash
export FLASK_APP=app
flask shell
>>> from app import db, Student
>>> db.create_all()
```
# Populating the Table
After creating the database and student table, use the flask shell to add some students to your database through the Student model.
To add a student to your database, you'll import the database object and the Student model, and create an instance of the Student model, passing it data as **kwargs
```bash
flask shell
from app import db, Student
student_john = Student(firstname='john', lastname='doe',
                       email='jd@example.com', age=23,
                       bio='Biology student')
```
The student_john represents the student that will be added to the database.
But this object has not been written in the database yet
```bash
>>> student_john
# output
<Student john>
# value of the columns
>>>student_john.firstname
>>>student_john.bio
#output
Output
'john'
'Biology student'
#Because this student has not been added to the database yet its ID will be None:
>>> print(student_john.id)
# output
None
# to add to the database you need to add to a database session, which manages database transaction.Flask-SQLAlchemy provides the db.session object through which you can manage your database changes.Add the student_john object to the session using the db.session.add() to be prepare it to be written to the database
>>>db.session.add(student_john)
# This will issue an INSERT statement, but you won't get an ID back since the database transaction is still not commited
# To commit the transaction apply changes to the database, use the db.session.commit()
>>> db.session.commit()
# you can also use the db.session.add() method to edit item in the database
>>> student_john.email = 'john_doe@example.com'
>>> db.session.add(student_john)
>>> db.session.commit()
# you can query all the records in the student table using the query attribute with the all() method
>>> Student.query.all()
# Querying one student
>>> Student.query.filter_by(firstname='Sammy').first()
# To get a student by its ID, you can use filter_by(id=ID)
>>> Student.query.filter_by(id=3).first()
# or you can use the shorter get() method which allows you to retrieve a specific item using its primary key
>>> Student.query.get(3)
```

