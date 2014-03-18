from setuptools import setup

setup(name='esgf_test_suite',
      version='0.1',
      description='Nose scripts for ESGF integration test and validation',
      url='http://github.com/ncaripsl/esgf-test-suite',
      author='Nicolas Carenton',
      author_email='nicolas.carenton@ipsl.jussieu.fr',
      license='IPSL',
      packages=['esgf_test_suite'],
      install_requires=[
          'nose',
          'pyOpenSSL',
	  'MyProxyClient',
	  'requests',
	  'lxml',
	  'splinter',
      ],
      zip_safe=False,
      include_package_data=True)
