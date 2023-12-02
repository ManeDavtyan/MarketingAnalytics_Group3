from setuptools import setup, find_packages

setup(
    author='Mane Davtyan',
    description='BookStore Recommendation System',
    name='bookstore',
    version='0.1.0',
    packages=find_packages(include=['bookstore','bookstore.*']),
    
)