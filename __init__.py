from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.secret_key ='sdfjosidjh4ojg$_%JOI)JOJ54469420@69'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    return app

app = create_app()
# print(f"{__file__}_{id(app)=}")
