import os
import shutil
import subprocess
from operator import itemgetter

import utils.authentication as auth
import utils.configuration as config
import utils.catalog as cat



def setup_module():
	global _mu
	global _tu

	global endpoints

	_mu = auth.MyProxyUtils()
	_tu = cat.ThreddsUtils()
	endpoints = _tu.get_endpoints()	

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
		#self.file = self.config['files']['gridftp_url']
		gridftp_endpoints = [i for i in endpoints if 'GridFTP' in i[2]]
		path = min(gridftp_endpoints,key=itemgetter(1))[0]
		url = "gsiftp://{0}:2811//{1}".format(self.config['nodes']['data_node'], path)
		a = subprocess.check_call(["globus-url-copy", "-b", url, "/tmp/dest_file.nc" ])
		print a

	@classmethod
	def teardown_class(self):
                # Delete downloaded file
                if os.path.exists("/tmp/dest_file.nc"):
                        os.remove("/tmp/dest_file.nc")	

#class TestHttp(object):
#	def test_wget_download(self):
#		http_endpoint = [i for i in endpoints if 'HTTPServer' in i[2]]
#                print min(http_endpoint,key=itemgetter(1))

