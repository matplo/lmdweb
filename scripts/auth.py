# from scripts import userdb
import userdb
import page_utils

class Authentication(object):
	def __init__(self, app):
		self.app = app
		app.auth = self

	def get_users_authorized(self, page):
		# users_authorized = page.meta.get('users', 'all')
		users_authorized = page_utils.safe_meta_get(page, 'users', None)
		if users_authorized is None:
			users_authorized = 'all'
		reta = []
		reta.append(self.app.config['MASTER_USER'])
		if type(users_authorized) == str:
			for u in users_authorized.split(','):
				reta.append(u)
		else:
			for u in users_authorized:
				reta.append(u)
		return reta

	def user_authorized(self, user, page):
		users_authorized = self.get_users_authorized(page)
		if 'all' in users_authorized:
			return True
		else:
			try:
				user.valid
			except:
				return False
			if user.name in users_authorized:
				return True
		return False

	# authentication
	def check_auth(self, username, password):
		return userdb.gUsers.check_passwd(username, password)
