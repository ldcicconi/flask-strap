from app import app, db, lm
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask import render_template, flash, redirect, session, url_for, request, g
from forms import LoginForm, RegisterForm
from models import User, ROLE_USER, ROLE_ADMIN
from wtforms.validators import ValidationError


@app.route('/')
@app.route('/index')
def index():
	user = g.user
	return render_template('index.html', user=user)


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	loginform = LoginForm(prefix='loginform')
	registerform = RegisterForm(prefix='registerform')
	if loginform.validate_on_submit():
		try:
			loginform.check_user(loginform.username.data, loginform.password.data)
		except ValidationError:
			return render_template('login.html', loginform = loginform, registerform = registerform)
		else:
			if User.query.filter_by(username=loginform.username.data).first() is not None:
				user = User.query.filter_by(username=loginform.username.data).first()
			else:
				user = User.query.filter_by(email=loginform.username.data).first()
			login_user(user)
			session['remember_me'] = loginform.remember_me.data
			flash('Successful login')
			return redirect('/index')
	elif registerform.validate_on_submit():
		username = registerform.username.data
		email = registerform.email.data
		password = registerform.password.data
		try:
			registerform.check(username, email)
		except ValidationError:
			return render_template('login.html', loginform = loginform, registerform = registerform, registererror=True)
		else:
			newuser = User(username=username, email=email)
			newuser.set_password(password)
			db.session.add(newuser)
			db.session.commit()
			usr=User.query.filter_by(username=username).first()
			login_user(usr)
			flash('Successful registration')
			return redirect('/index')
	return render_template('login.html', loginform = loginform, registerform = registerform)


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.before_request
def before_request():
	g.user = current_user


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
