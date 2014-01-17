import requests

import utils.configuration as config



_services = {'idp_server'	: ['esgf-idp'],
	     'index_server'	: ['esgf-web-fe'],
	     'compute_server'	: ['las'],
	     'data_server'	: ['esgf-node-manager', 'esg-orp',
                         	   'esgf-desktop', 'esgf-dashboard',
                         	   'thredds']}

def setup_module():
	global _conf
	_conf = config.read_config()

def teardown_module():
	pass


class TestWebFrontEnds(object):
	def test_frontends_availability(self):
		for server_type in _services:
			server_name = _conf['servers'][server_type]
			for service in _services[server_type]:
				URL = "https://" + server_name + "/" + service
				r = requests.get(URL, verify=False)
				assert r.status_code == 200

