import os
import shutil
import subprocess

import utils.authentication as auth
import utils.configuration as config



def setup_module():
	global _mu

	_mu = auth.MyProxyUtils()
	_mu.get_trustroots()
	_mu.get_credentials()

def teardown_module():
	_mu.delete_credentials()
	_mu.delete_trustroots()


class TestGridFtp(object):
	@classmethod
	def setup_class(self):
		self.config = config.read_config()
		os.environ['X509_USER_PROXY'] = os.path.expanduser("~/.esg/credentials.pem")
		os.environ['X509_CERT_DIR'] = os.path.expanduser("~/.esg/certificates")

	def test_globus_url_copy(self):
		self.file = self.config['files']['gridftp_url']
		subprocess.check_call(["globus-url-copy", "-b", self.file, "/tmp/dest_file.nc" ])		

	@classmethod
	def teardown_class(self):
                # Delete downloaded file
                if os.path.exists("/tmp/dest_file.nc"):
                        os.remove("/tmp/dest_file.nc")	
