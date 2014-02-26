from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, Email, ValidationError, StopValidation
from models import User

class LoginForm(Form):
	username = TextField('username', validators = [Required()])#Also checks email
	password = PasswordField('password', validators = [Required()])
	remember_me = BooleanField('remember_me', default = False)

	def check_user(self, username, password):
		if User.query.filter_by(username=username).first() is not None or User.query.filter_by(email=username).first() is not None:
			if User.query.filter_by(username=username).first() is not None:
				x = User.query.filter_by(username=username).first()
			else:
				x = User.query.filter_by(email=username).first()
			if not x.check_password(password):
				self.password.errors.append('Incorrect password')
				raise ValidationError('Incorrect password')
			else:
				return True
		else:
			self.username.errors.append('Incorrect username or email')
			raise ValidationError('Incorrect username or email')


class RegisterForm(Form):
	username = TextField('username', validators = [Required()])
	email = TextField('email', validators=[Required(), Email()])
	password = PasswordField('password', validators = [Required()])

	def check(self, username, email):
		if User.query.filter_by(username=username).first() is None:
			if User.query.filter_by(email=email).first() is None:
				return True
			else:
				self.email.errors.append('Email already associated with an account')
				raise ValidationError('Email already associated with an account')
		else:
			self.username.errors.append('Username is taken')
			raise ValidationError('Username is taken')
