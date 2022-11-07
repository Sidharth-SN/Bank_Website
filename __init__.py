from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.secret_key ='sdfjosidjh4ojg$_%JOI)JOJ54469420@69'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wbslyaejyfjamr:cd7970d4b3cc3f721288af4c5cda5293054e0e092e0d7014c2086844b5f72c63@ec2-54-246-185-161.eu-west-1.compute.amazonaws.com:5432/d69rgo10i23arq'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    return app

app = create_app()
# print(f"{__file__}_{id(app)=}")
