from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True

bcrypt = Bcrypt(app)

app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

toolbar = DebugToolbarExtension(app)
from app import views, models

if __name__ == "__main__":
    app.run()
