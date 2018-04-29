# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Web Crawler',
    version='0.1.0',
    description='Web Crawler to analyze sentiment of webpages',
    long_description=readme,
    author='Thomas de Lange',
    author_email='delange.thomas@gmail.com',
    url='https://github.com/kennethreitz/samplemod',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
