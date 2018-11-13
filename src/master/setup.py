# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Simple Python Reverse Shell (Server)',
    version='1.0.0',
    description='A Python reverse shell for executing remote code in target system.',
    long_description=readme,
    author='Heiko Alexander Weber',
    author_email='heiko.a.weber@gmail.com',
    url='https://github.com/heikoalexanderweber',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

