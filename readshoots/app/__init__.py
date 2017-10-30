from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:qwer@localhost/readshoots"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/uploads/")
app.config["FC_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/uploads/users/")
app.config["SECRET_KEY"] = '44a648cbdd9f48178a2e22bda53eb7b9'
app.debug = True
db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint,url_prefix="/admin")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")