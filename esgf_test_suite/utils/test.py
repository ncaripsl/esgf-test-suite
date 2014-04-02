import os
import inspect
import sys


a = os.path.abspath(inspect.getsourcefile(lambda _: None))
print a.rsplit('/', 2)[0]+'/configuration.ini'
