from flask import Flask

#import flask extensions
from flask.ext.sqlalchemy import SQLAlchemy

#config values
SQLALCHEMY_DATABASE_URI ='sqlite:///example.db'
DEBUG = True
SECRET_KEY = 'development key'

#create app
app = Flask(__name__)

#config app
app.config.from_object(__name__)

#init extensitions
db = SQLAlchemy(app)





if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run()

