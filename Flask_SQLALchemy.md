# INSTALL
```bash
pip install flask-sqlalchemy
```
```python
#import the SQLALchemy class from this module
from flask_sqlalchemy import SQLAlchemy
#Create a Flask application object and set the URI for the database to use
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'uri for the specific database system'
#This detrmines whether the database session is automatically committed when the application tears down.This means that any changes made to the database during the request will be committed to the database, even if an exception is raised.If set to false there will be no automatic commit when the application tears down.Any changes made won't be committed to the database unless the db.session.commit() is called explicitly.The dafualt value is true.there are some cases where you might want to set it to false for example if you are using the db.session.rollback() method to roll back changes made to the database during the request.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#then use the application object as a parameter to create an object of class SQLAlchemy.The object contains an auxiliary function for the ORM operation.It also provides a parent Model class that uses it to declare a user-defined model.

db = SQLAlchemy(app)

#create the models

```