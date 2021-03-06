import requests

import utils.configuration as config



_services = {'idp_node'		: ['esgf-idp'],
	     'index_node'	: ['esgf-web-fe'],
	     'compute_node'	: ['las'],
	     'data_node'	: ['esgf-node-manager', 'esg-orp',
                         	   'esgf-desktop', 'esgf-dashboard',
                         	   'thredds']}

def setup_module():
	global _conf
	_conf = config.read_config()

def teardown_module():
	pass


class TestWebFrontEnds(object):
	def check_frontend_availability(self, URL):
		r = requests.get(URL, verify=False, timeout=5)
		assert r.status_code == 200

	def test_frontends_availability(self):
		for node_type in _services:
			node_name = _conf['nodes'][node_type]
			for service in _services[node_type]:
				URL = "https://" + node_name + "/" + service
				yield self.check_frontend_availability, URL
