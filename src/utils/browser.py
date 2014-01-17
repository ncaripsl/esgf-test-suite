import nose
from splinter import Browser

from selenium import webdriver

     # Visit URL
#browser = Browser()

def browse(): #est_browse
	browser = Browser('firefox')

	url = "http://esgf-node.ipsl.fr/esgf-web-fe/login"
	browser.visit(url)

	browser.find_by_id('openid_identifier').fill('https://esgf-node.ipsl.fr/esgf-idp/openid/ncarenton')
	button = browser.find_by_value('Login')
	button.click()
	browser.find_by_id('password').fill('Tummy285')
	button = browser.find_by_value('SUBMIT')
	button.click()
     # Find and click the 'search' button
     #button = browser.find_by_name('btnG')
     # Interact with elements
     #button.click()
     #if browser.is_text_present('splinter.cobrateam.info'):
     #    print "Yes, the official website was found!"
     #else:
     #    print "No, it wasn't found... We need to improve our SEO techniques" 



def test_selenium():
        browser = webdriver.Firefox()
        browser.get('http://www.google.com')
        assert 'Google' == browser.title
	browser.quit()


#test_browse()

