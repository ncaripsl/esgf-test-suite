import requests
from selenium import webdriver

import configuration as config



class UserUtils(object):
        def __init__(self):
                self.config = config.read_config()
		self.account = self.config['account']
                self.idp_server = self.config['nodes']['idp_node']
		
                self.elements = {'firstName' : self.account['firstname'],
                                 'lastName'  : self.account['lastname'],
                                 'email'     : self.account['email'],
                                 'userName'  : self.account['username'],
                                 'password1' : self.account['password'],
                                 'password2' : self.account['password']}


        def create_user(self):
		URL = "https://{0}/esgf-web-fe/createAccount".format(self.idp_server)

		if (requests.get(URL, verify=False).status_code == 200):
			self.driver = webdriver.Firefox()
			self.driver.get(URL)
		
			for element_name in self.elements:
				self.driver.find_element_by_name(element_name).send_keys(self.elements[element_name])

			self.driver.find_element_by_css_selector("input[type=submit]").click()
			
			self.driver.quit()

        def delete_user(self):
		pass
