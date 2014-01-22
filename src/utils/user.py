from selenium import webdriver

import configuration as config



_elements = {'firstName' : 'testfirstName',
             'lastName'  : 'testlastName',
             'email'	 : 'nicolas.carenton@ipsl.jussieu.fr',
	     'userName' : 'testuserName',
	     'password1' : 'testPassword1',
	     'password2' : 'testPassword1'}

class UserUtils(object):
        def __init__(self):
		self.driver = webdriver.Firefox();
                self.config = config.read_config();


        def create_user(self):
		self.driver.get("https://"+self.config['servers']['index_server']+"/esgf-web-fe/createAccount");

		for element_name in _elements:
			self.driver.find_element_by_name(element_name).send_keys(_elements[element_name]);

		self.driver.find_element_by_css_selector("input[type=submit]").click();
		#self.driver.quit();


        def delete_user(self):
		pass

