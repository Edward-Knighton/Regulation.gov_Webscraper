"""Reg.gov  webscraper python package configuration."""
import os
from setuptools import setup

setup(
    name='Reg_Gov_Scraper',
    author="Edward Knighton",
    author_email="edknight@umich.edu",
    description= ("A regulations.gov webscraper in order to mass download submitted comments on government regulations"),
    version='0.1.0',
    packages=['Reg_Gov_Scraper'],
    include_package_data=True,
    install_requires=[
        'tqdm==4.26.0',
        'pdfminer==20140328',
        'openpyxl==2.5.8',
    ],
    entry_points={
          'console_scripts': [
              'Reg_Gov_Scraper = my_project.__main__:main'
          ]
          },
)
