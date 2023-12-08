from setuptools import setup, find_packages

setup(
    author='Mane Davtyan',
    description='BookStore Recommendation System',
    name='bookrec',
    version='0.1.0',
    packages=find_packages(include=['bookrec','bookrec.*']),
    
)