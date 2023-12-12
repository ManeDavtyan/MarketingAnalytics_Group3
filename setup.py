from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()
setup(
    author='Mane Davtyan',
    description='BookStore Recommendation System',
    name='bookrecs',
    version='1.1.3',
    packages=find_packages(include=['bookrecs', 'bookrecs.*']),
    install_requires=[
    'Faker==20.1.0',
    'fastapi==0.105.0',
    'numpy==1.24.4',
    'pandas==2.0.3',
    'pydantic==2.5.2',
    'scikit_learn==1.3.2',
    'setuptools==49.2.1',
    'SQLAlchemy==2.0.23',

    ],
    dependency_links=['https://github.com/ManeDavtyan/MarketingAnalytics_Group3'],
    long_description=description,
    long_description_content_type = "text/markdown"
)
