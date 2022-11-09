from flask import render_template, redirect, request, session, url_for, flash
from tables import *
import re, random
from __init__ import app

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['pass']

        global db_u, db_acc
        db_u = Users.query.filter_by(username = user).first()
        db_acc = Accounts.query.filter_by(user_id = db_u.id).first()

        if db_u != None:
            if passw == db_u.passwd:
                if not Accounts.query.filter_by(user_id = db_u.id).first():
                    return redirect(url_for('acc_register', user = user))

                session['user'] = user
                return redirect(url_for('index'))
            else:
                flash('Password Incorrect')
        else:
            flash('User not registered')

    return render_template('login.html')


@app.route("/", methods = ['POST', 'GET'])
def index():
    return render_template('index.html')
 
@app.route("/profile", methods = ['POST', 'GET'])
def profile():
    if not db_acc:
        return redirect(url_for('acc_register', user = session['user']))

    return render_template('profile.html', acc_details = db_acc)


@app.route("/balance", methods = ['POST', 'GET'])
def balance():
    if not db_acc:
        return redirect(url_for('acc_register', user = session['user']))

    if request.method == 'POST':
        passw = request.form['pass']
        if passw != db_u.passwd:
            flash('Wrong password')
            return redirect(url_for('balance'))
        else:
            return render_template('balance.html', accDetail = [db_acc.acc_no, db_acc.ifsc, db_acc.balance])

    return render_template('balance.html', accDetail = [db_acc.acc_no, db_acc.ifsc, '*****'])


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route("/aboutUs", methods = ['POST', 'GET'])
def about():
    return render_template('about.html')

@app.route("/terms", methods = ['POST', 'GET'])
def terms():
    return render_template('terms.html')

@app.route("/loans", methods = ['POST', 'GET'])
def loan():
    if not db_acc:
        return redirect(url_for('acc_register', user = session['user']))

    if request.method == 'POST':
        # acc = request.form['acc']
        name = request.form['name']
        fname = request.form['fname']
        phoneNo = request.form['phone']
        address = request.form['address']
        age = request.form['age']
        proprietor = request.form['proprietor']
        occupation = request.form['occupation']
        loanAmt = request.form['loanA']
        loanPurp = request.form['loanPurp']
        loanPeriod = request.form['loanPeriod']
        nation = request.form['nation']
        mIncome = request.form['income']
        pan = request.form['pan']
        loanType = request.form['loan_type']
        intrestRate = request.form['intrestR']
        sex = request.form['gender']

        if len(phoneNo) != 10 or phoneNo.isnumeric() != True:
            flash('Please enter a valid Phone Number')
            return redirect(url_for('loan'))
        elif age.isnumeric() != True:
            flash('Please enter a valid Age')
            return redirect(url_for('loan'))
        elif loanAmt.isnumeric() != True:
            flash('Please enter a valid Loan Amount')
            return redirect(url_for('loan'))
        elif loanPeriod.isnumeric() != True:
            flash('Please enter a valid Loan Period in number of months')
            return redirect(url_for('loan'))
        elif mIncome.isnumeric() != True:
            flash('Please enter a valid Income')
            return redirect(url_for('loan'))
        else:
            num = random.randrange(100000000, 1000000000)
            if Loans.query.filter_by(lid = num).first():
                num = random.randrange(100000000, 1000000000)

            loan = Loans(
                lid = num,
                full_name = name,
                father_name = fname,
                phone = phoneNo,
                address = address,
                age = age,
                proprietor = proprietor,
                occupation = occupation,
                nationality = nation,
                income = mIncome,
                loan_purpose = loanPurp,
                loan_type = loanType,
                loan_intrest = intrestRate,
                loan_period = loanPeriod,
                loan_amt = loanAmt,
                gender = sex,
                pan_no = pan,
                acc = db_acc.acc_no
            )

            db.session.add(loan)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('loan.html', detl = [db_acc.acc_no, db_acc.pan_no])


@app.route("/cards", methods = ['POST', 'GET'])
def card():
    if not db_acc:
        return redirect(url_for('acc_register', user = session['user']))

    Ccard = Credit_card.query.filter_by(credit_id = db_acc.acc_no)
    Dcard = Debit_card.query.filter_by(debit_id = db_acc.acc_no)

    cno = '-'.join([str(Ccard.card_no)[i:i+4] for i in range(0, 16, 4)])
    cc = [cno, Ccard.card_holder_name, Ccard.valid_to, Ccard.cvv]

    dno = '-'.join([str(Dcard.card_no)[i:i+4] for i in range(0, 16, 4)])
    dd = [dno, Dcard.card_holder_name, Dcard.valid_to, Dcard.cvv]

    cards = [cc, dd]
    return render_template('cards.html', cards = cards)

@app.route("/transfer", methods = ['POST', 'GET'])
def transfer():
    if not acc:
        return redirect(url_for('acc_register', user = session['user']))

    if request.method == 'POST':
        acc = request.form['acc_no']
        re_acc = request.form['re_acc']
        ifsc = request.form['ifsc']
        amt = request.form['amount']

        if acc != re_acc or len(acc) != 12:
            flash("Entered account numbers dosen't match")
            return redirect(url_for('transfer'))
        elif len(ifsc) != 11:
            flash("Please enter a valif IFSC Code")
            return redirect(url_for('transfer'))
        elif int(amt) > db_acc.balance:
            flash("Balance Insufficient")
            return redirect(url_for('transfer'))
        else:
            num = random.randrange(1000000000, 10000000000)
            if Transactions.query.filter_by(tid = num).first():
                num = random.randrange(1000000000, 10000000000)

            trans = Transactions(
                tid = num,
                tAmount = int(amt),
                acc_to = acc,
                type_tranc = 'Debit',
                from_acc = db_acc.acc_no
            )
            db.session.add(trans)
            db_acc.balance -= int(amt)

            db.session.commit()

            return redirect(url_for('index'))

    return render_template('transfer.html')


@app.route("/deposit", methods = ['POST', 'GET'])
def deposit():
    if not db_acc:
        return redirect(url_for('acc_register', user = session['user']))
        
    if request.method == 'POST':
        acc = request.form['acc_number']
        user = request.form['username']
        pas = request.form['passw']
        amt = request.form['amount']

        # if acc != db_acc.acc_no:
        #     flash("Please enter a valid Account Number")
        #     return redirect(url_for('deposit'))

        if user != db_u.username:
            flash("Incorrect Username")
            return redirect(url_for('deposit'))

        elif pas != db_u.passwd:
            flash("Incorrect Password")
            return redirect(url_for('deposit'))
        
        else:
            num = random.randrange(1000000000, 10000000000)
            if Transactions.query.filter_by(tid = num).first():
                num = random.randrange(1000000000, 10000000000)

            trans = Transactions(
                tid = num,
                tAmount = int(amt),
                acc_to = acc,
                type_tranc = 'Credit',
                from_acc = db_acc.acc_no
            )
            db.session.add(trans)
            db_acc.balance += int(amt)

            db.session.commit()

            return redirect(url_for('index'))

    return render_template('deposit.html', detl = [db_acc.acc_no, db_acc.acc_holder_name])


@app.route("/transaction", methods = ['POST', 'GET'])
def transaction():
    if db_acc != None:
        db_acc = db_acc.acc_no
    all_Trans = Transactions.query.filter_by(from_acc = db_acc).all()
    # finally:
    return render_template('transaction.html', all_Trans = all_Trans)


@app.route('/delete_acc')
def delete_account():
    try:
        session.pop('user', None)
        db.session.delete(db_u)
        db.session.commit()
        return redirect(url_for('login'))
    except:
        flash('There was a problem deleting your account. Please try again after sometime')
        return redirect(url_for('index'))


@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        Email = request.form['email']
        pass1 = request.form['password']
        pass2 = request.form['password2']

        if pass1 != pass2:
            flash("You Passwords dosen't match. Please enter same password in both")
            return redirect(url_for('register'))

        if db_u != None:
        # if username in USERS:
        #     if Email == USERS[username][0]:
            if Email == db_u.email:
                flash('User already registered with same Username and Email')
                return redirect(url_for('register'))
            else:
                flash('User already registered with same Username')
                return redirect(url_for('register'))
        else:
            # if Email == Users.query.filter_by(username = user).first().email:
            if Users.query.filter_by(email = Email).first() != None:
                flash('User already registered with same Email')
                return redirect(url_for('register'))
            else:
                if len(pass1) < 8:
                    flash('Password must be 8 characters or more')
                    return redirect(url_for('register'))
                elif not re.search('[a-z]', pass1):           
                    flash('Password must have lower case letters')
                    return redirect(url_for('register'))
                elif not re.search('[A-Z]', pass1):
                    flash('Password must have upper case letters')
                    return redirect(url_for('register'))
                elif not re.search('[!#$%&()*+,-./:;<=>?@[\]^_`{|}~]', pass1):
                    flash('Password must have special characters')
                    return redirect(url_for('register'))
                else:
                    users = Users(
                        username = user,
                        email = Email,
                        passwd = pass1
                    )
                    db.session.add(users)
                    db.session.commit()
        
                    # USERS[username] = [Email, pass1]
                    return redirect(url_for('acc_register', user = user))

    return render_template('register.html')


@app.route("/acc_register/<string:user>", methods = ['POST', 'GET'])
def acc_register(user):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        father = request.form['fathername']
        birth = request.form['dob']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        state = request.form['state']
        pinCode = request.form['pinCode']
        country = request.form['country']
        phone = request.form['phone']
        occupation = request.form['occupation']
        aadhar = request.form['aadhar']
        pan = request.form['pan']
        marital = request.form['marital']
        sex = request.form['gender']
        accType = request.form['acc_type']

        full_name = ' '.join([fname, lname])
        f_address = ' '.join([address1, address2, city])
        y, m, d = birth.split('-')

        # u = Users.query.filter_by(username = user).first()
        detail = [user, fname, lname, father, birth, address1, address2, city, state, pinCode, country, phone, occupation, aadhar, pan]
        if len(pinCode) != 6:
            flash('Please enter a valid Pin Code')
            return render_template('account_regi.html', user = detail)

        elif len(phone) != 10:
            flash('Please enter a valid Phone Number')
            return render_template('account_regi.html', user = detail)

        elif len(aadhar) != 12:
            flash('Please enter a valid Aadhar Number')
            return render_template('account_regi.html', user = detail)

        elif not re.search(r"[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}", pan) and len(pan) != 10:
            flash('Please enter a valid PAN Number')
            return render_template('account_regi.html', user = detail)

        else:
            acc_num = random.randrange(100000000000, 1000000000000)
            if Accounts.query.filter_by(acc_no = acc_num).first():
                acc_num = random.randrange(100000000000, 1000000000000)

            acc_det = Accounts(
                    acc_no = acc_num,
                    ifsc = 'FAKE0069420',
                    acc_holder_name = full_name,
                    father_name = father,
                    dob = date(int(y), int(m), int(d)),
                    address = f_address,
                    state = state,
                    pin_code = int(pinCode),
                    country = country,
                    phoneNo = int(phone),
                    occupation = occupation,
                    aadhar_no = int(aadhar),
                    pan_no = pan,
                    marital = marital,
                    sex = sex,
                    acc_type = accType,
                    user_id = Users.query.filter_by(username = user).first().id
            )

            c_num = random.randrange(1000000000000000, 10000000000000000)
            if Credit_card.query.filter_by(card_no = c_num).first() or Debit_card.query.filter_by(card_no = c_num).first():
                c_num = random.randrange(1000000000000000, 10000000000000000)

            # Only 1000 unique cvv can be generated
            ccvv = random.randrange(100, 1000)
            if Credit_card.query.filter_by(cvv = ccvv).first() or Debit_card.query.filter_by(cvv = ccvv).first():
                ccvv = random.randrange(100, 1000)

            cCard = Credit_card(
                    card_no = c_num,
                    card_holder_name = full_name,
                    credit_limit = 100000,
                    bill_date = '7th of Every month',
                    valid_from = str(datetime.today().month) + '/' + str(datetime.today().year)[-2:],
                    valid_to = str(datetime.today().month - 1) + '/' + str(datetime.today().year + 7)[-2:],
                    cvv = ccvv,
                    credit_id = acc_num
            )

            d_num = random.randrange(1000000000000000, 10000000000000000)
            if Credit_card.query.filter_by(card_no = d_num).first() or Debit_card.query.filter_by(card_no = d_num).first():
                d_num = random.randrange(1000000000000000, 10000000000000000)

            # Only 1000 unique cvv can be generated
            dcvv = random.randrange(100, 1000)
            if Credit_card.query.filter_by(cvv = dcvv).first() or Debit_card.query.filter_by(cvv = dcvv).first():
                dcvv = random.randrange(100, 1000)

            dCard = Debit_card(
                    card_no = d_num,
                    card_holder_name = full_name,
                    valid_from = str(datetime.today().month) + '/' + str(datetime.today().year)[-2:],
                    valid_to = str(datetime.today().month - 1) + '/' + str(datetime.today().year + 7)[-2:],
                    cvv = dcvv,
                    debit_id = acc_num
            )

            db.session.add(acc_det)
            db.session.add(cCard)
            db.session.add(dCard)

            db.session.commit()

            return redirect(url_for('login'))

    return render_template('account_regi.html', user = [user])

