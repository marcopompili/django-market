"""
Created on 24/gen/2014

@author: Marco Pompili
"""

import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
      name=str('django-market'),
      version=str('0.2'),
      packages=['django_market', 'django_market.templatetags'],
      include_package_data=True,
      license=str('BSD-3 License'),
      description=str('Django Market is an application for basic management of categories and products.'),
      long_description=README,
      url=str('https://github.com/marcopompili/django-market'),
      author=str('Marco Pompili'),
      author_email=str('django@emarcs.org'),
      install_requires=['django', 'django-mptt', 'django-modeltranslation==0.7.3', 'django-galleries'],
      classifiers=[
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD-3 License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
      )