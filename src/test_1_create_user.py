import nose

import utils.user as usr



def setup_module():
	global	_usr

	_usr = usr.UserUtils()

def teardown_module():
	pass

class TestCreateUser(object):
	def test_create_user(self):
		_usr.create_user()
