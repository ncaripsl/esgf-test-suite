import os
import sys

from ConfigParser import SafeConfigParser

def read_config():
	filePath = os.getcwd()+"/configuration.ini"
	parser = SafeConfigParser()

	parser.readfp(open(filePath))
	config = dict((section, dict((option, parser.get(section, option))
                             for option in parser.options(section)))
              for section in parser.sections())	
	return config
