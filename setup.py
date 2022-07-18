from setuptools import setup, find_packages

# function to read in requirements.txt to package setup function
def read_requirements():
  with open('requirements.txt') as req:
    content = req.read()
    requirements = content.split('\n')

  return requirements

# default setup.py function to define package and console script
setup(
  name='ribbitx',
  version='0.3',
  packages=find_packages(),
  include_package_data=True,
  install_requires=read_requirements(),
  entry_points='''
    [console_scripts]
    ribbitx=ribbitx.cli:cli
  '''
)