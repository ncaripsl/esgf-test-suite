import os
import sys
import site

from ConfigParser import SafeConfigParser

def read_config():
	#filePath = os.getcwd()+"/configuration.ini"
	#filePath = os.path.expanduser("~") + "/code//esgf-test-suite/esgf-test-suite/configuration.ini"
	filePath = site.getusersitepackages() + "/esgf_test_suite/esgf_test_suite/configuration.ini"

	parser = SafeConfigParser()

	parser.readfp(open(filePath))
	config = dict((section, dict((option, parser.get(section, option))
                             for option in parser.options(section)))
              for section in parser.sections())	
	return config
