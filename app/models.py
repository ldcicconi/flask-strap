from app import db, bcrypt

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String, index = True, unique = True)
	email = db.Column(db.String, index = True, unique = True)
	pwdhash = db.Column(db.String)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	
	def __repr__(self):
		return '<User %r>' % (self.username)

	def set_password(self, password):
		self.pwdhash = bcrypt.generate_password_hash(password)

	def check_password(self, password):
		return bcrypt.check_password_hash(self.pwdhash, password)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.username)
