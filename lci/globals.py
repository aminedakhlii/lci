from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lciDatabase.db'
