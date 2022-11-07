from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.secret_key ='sdfjosidjh4ojg$_%JOI)JOJ54469420@69'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ojmjqofiuiycas:fe00f8f10d18baf52d3aae65812ab0a195c1ce9281085f7379af0a64029181d7@ec2-99-81-16-126.eu-west-1.compute.amazonaws.com:5432/d2bej9tm2co5tq'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    return app

app = create_app()
# print(f"{__file__}_{id(app)=}")
