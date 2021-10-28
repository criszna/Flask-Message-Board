from flask import Blueprint,render_template,url_for,request,redirect
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_required
from . import db
from .models import User
auth=Blueprint('auth',__name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup',methods=['POST'])
def post_signup():
    name = request.form.get('name')
    email = request.form.get('email')
    pwd = request.form.get('pwd')

    user = User.query.filter_by(email=email).first()
    if user is None == False:
        return redirect(url_for('auth.signup'))

    else:
        new_user = User(email=email,password=generate_password_hash(pwd,method='sha256'),username=name)
        db.session.add(new_user)
        db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def post_login():
    name = request.form.get('name')
    pwd = request.form.get('pwd')

    user = User.query.filter_by(username=name).first()
    if user and check_password_hash(user.password,pwd):
        login_user(user)
        return redirect(url_for('main.home',user=user))
    else:
        return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('welcome.html')