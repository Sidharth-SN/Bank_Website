from __init__ import db, app
from flask_migrate import Migrate
from datetime import datetime, date

migrate = Migrate(app, db, render_as_batch=True)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), nullable = False)
    passwd = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.now)

    banks = db.relationship('Accounts', backref = 'users')

    # def __repr__(self):
    #     return f'{self.sno} : {self.username} - {self.email}'

class Accounts(db.Model):
    acc_no = db.Column(db.BIGINT, primary_key = True)
    ifsc = db.Column(db.String(20), nullable = False)
    balance = db.Column(db.BIGINT, default = 0)
    acc_holder_name = db.Column(db.String(50), nullable = False)
    father_name =  db.Column(db.String(50), nullable = False)
    dob = db.Column(db.Date, nullable = False)
    address = db.Column(db.String(200), nullable = False)
    state = db.Column(db.String(20), nullable = False)
    pin_code = db.Column(db.Integer, nullable = False)
    country = db.Column(db.String(20), nullable = False)
    phoneNo = db.Column(db.BIGINT, nullable = False)
    occupation = db.Column(db.String(100))
    aadhar_no = db.Column(db.BIGINT, nullable = False)
    pan_no = db.Column(db.String(20), nullable = False)
    marital = db.Column(db.String(10))
    sex = db.Column(db.String(7), nullable = False)
    acc_type = db.Column(db.String(20), nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'CASCADE'))
    
    c_card = db.relationship('Credit_card', backref = 'cacc')
    d_card = db.relationship('Debit_card', backref = 'dacc')
    t_acc = db.relationship('Transactions', backref = 'trans')
    loan = db.relationship('Loans', backref = 'loans')
        

class Credit_card(db.Model):
    card_no = db.Column(db.BIGINT, primary_key = True)
    card_holder_name = db.Column(db.String(50), nullable = False)
    credit_limit = db.Column(db.Integer, nullable = False)
    outstanding = db.Column(db.Integer, default = 0)
    bill_date = db.Column(db.String(20), nullable = False)
    valid_from = db.Column(db.String(7), nullable = False)
    valid_to = db.Column(db.String(7), nullable = False)
    cvv = db.Column(db.Integer, nullable = False)

    credit_id = db.Column(db.BIGINT, db.ForeignKey('accounts.acc_no', ondelete = 'CASCADE'))


class Debit_card(db.Model):
    card_no = db.Column(db.BIGINT, primary_key = True)
    card_holder_name = db.Column(db.String(50), nullable = False)
    # balance = db.Column(db.Integer, default = 0)
    valid_from = db.Column(db.String(7), nullable = False)
    valid_to = db.Column(db.String(7), nullable = False)
    cvv = db.Column(db.Integer, nullable = False)

    debit_id = db.Column(db.BIGINT, db.ForeignKey('accounts.acc_no', ondelete = 'CASCADE'))


class Transactions(db.Model):
    sno = db.Column(db.Integer, primary_key = True, autoincrement = True)
    tid = db.Column(db.BIGINT, nullable = False)
    dot = db.Column(db.DateTime, nullable = False, default = datetime.now)
    tAmount = db.Column(db.BIGINT, default = 0)
    acc_to = db.Column(db.BIGINT, nullable = False)
    medium_tranc = db.Column(db.String(10), nullable = False, default = 'Online')
    type_tranc = db.Column(db.String(10), nullable = False)

    from_acc = db.Column(db.Integer, db.ForeignKey('accounts.acc_no', ondelete = 'CASCADE'))


class Loans(db.Model):
    lid = db.Column(db.BIGINT, primary_key = True, autoincrement = True)
    full_name  = db.Column(db.String(20), nullable = False)
    father_name = db.Column(db.String(20), nullable = False)
    phone = db.Column(db.BIGINT, nullable = False)
    address = db.Column(db.String(100), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    proprietor = db.Column(db.String(20), nullable = False)
    occupation = db.Column(db.String(30), nullable = False)
    nationality = db.Column(db.String(20), nullable = False)
    income = db.Column(db.BIGINT, nullable = False)
    loan_purpose = db.Column(db.String(40), nullable = False)
    loan_type = db.Column(db.String(20), nullable = False)
    loan_intrest = db.Column(db.String(20), nullable = False)
    loan_period = db.Column(db.String(10), nullable = False)
    loan_amt = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(10), nullable = False, default = 'Prefer not to say')
    pan_no = db.Column(db.String(10), nullable = False)

    acc = db.Column(db.Integer, db.ForeignKey('accounts.acc_no', ondelete = 'CASCADE'))
