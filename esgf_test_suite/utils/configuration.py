import os
import sys
import site
import subprocess

from ConfigParser import SafeConfigParser

def read_config():
	#filePath = os.getcwd()+"/configuration.ini"
	#filePath = os.path.expanduser("~") + "/code//esgf-test-suite/esgf-test-suite/configuration.ini"
	usersitepackages = subprocess.Popen(['python', '-m', 'site', '--user-site'], stdout=subprocess.PIPE).communicate()[0]#check_output(["python", "-m", "site", "--user-site"])
	usersitepackages = usersitepackages[:-2]
	filePath = "/usr/lib/python2.6/site-packages/esgf_test_suite-0.1-py2.6.egg/esgf_test_suite/configuration.ini"

	parser = SafeConfigParser()

	parser.readfp(open(filePath))
	config = dict((section, dict((option, parser.get(section, option))
                             for option in parser.options(section)))
              for section in parser.sections())	
	return config
