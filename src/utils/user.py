from selenium import webdriver

import configuration as config



class UserUtils(object):
        def __init__(self):
                self.driver = webdriver.Firefox();

                self.config = config.read_config();
		self.account = self.config['account']
                self.idp_server = self.config['servers']['idp_server']
		
                self.elements = {'firstName' : self.account['firstname'],
                                 'lastName'  : self.account['lastname'],
                                 'email'     : self.account['email'],
                                 'userName'  : self.account['username'],
                                 'password1' : self.account['password'],
                                 'password2' : self.account['password']}


        def create_user(self):
		self.driver.get("https://"+self.idp_server+"/esgf-web-fe/createAccount");
		
		for element_name in self.elements:
			self.driver.find_element_by_name(element_name).send_keys(self.elements[element_name]);

		self.driver.find_element_by_css_selector("input[type=submit]").click();
		self.driver.quit();


        def delete_user(self):
		pass

