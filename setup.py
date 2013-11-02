from setuptools import setup, find_packages
import os

version = '0.0'

long_description = (
    open('README.rst').read() + '\n' +
    open('CHANGES.rst').read() + '\n'
    )

setup(name='mtj.ppmx',
      version=version,
      description="Some package that tries to make sense of xmpp",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Tommy Yu',
      author_email='y@metatoaster.com',
      url='https://github.com/metatoaster/mtj.ppmx/',
      license='gpl',
      packages=find_packages(),
      namespace_packages=['mtj'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'mtj.jibber',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
