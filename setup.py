from setuptools import setup, find_packages

setup(
    author='Mane Davtyan',
    description='BookStore Recommendation System',
    name='bookrec',
    version='0.1.3',
    packages=find_packages(include=['bookrec', 'bookrec.*']),
    install_requires=[
        'annotated-types==0.6.0',
        'anyio<4.0.0 and >=3.7.1',
        'click==8.1.7',
        'exceptiongroup==1.2.0',
        'Faker==20.1.0',
        'fastapi==0.104.1',
        'fuzzywuzzy==0.18.0',
        'greenlet==3.0.1',
        'h11==0.14.0',
        'idna==3.6',
        'joblib==1.3.2',
        'numpy==1.24.4',
        'pandas==2.0.3',
        'pydantic==2.5.2',
        'pydantic-core==2.14.5',
        'python-dateutil==2.8.2',
        'pytz==2023.3.post1',
        'scikit-learn==1.3.2',
        'scipy==1.10.1',
        'six==1.16.0',
        'sniffio==1.3.0',
        'SQLAlchemy==2.0.23',
        'starlette>=0.27.0,<=0.33.0',
        'threadpoolctl==3.2.0',
        'typing-extensions==4.8.0',
        'tzdata==2023.3',
        'uvicorn==0.24.0.post1',
    ],
)