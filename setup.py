from setuptools import setup

setup(name='esgf_test_suite',
      version='0.6',
      description='Nose scripts for ESGF integration test and validation',
      url='http://github.com/ncaripsl/esgf_test_suite',
      author='Nicolas Carenton',
      author_email='nicolas.carenton@ipsl.jussieu.fr',
      license='IPSL',
      packages=['esgf_test_suite'],
      install_requires=[
          'nose',
          'pyOpenSSL==0.13.1',
	  'MyProxyClient',
	  'requests',
	  'lxml',
	  'splinter',
      ],
      zip_safe=False,
      include_package_data=True)
