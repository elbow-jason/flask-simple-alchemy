from setuptools import setup

project = "flask-simple-alchemy"

setup(
    name=project,
    version='0.6.0a',,
    description='A Simplification of SQLAlchemy\'s declarative using '\
        + ' Flask-SQLAlchemy',
    author='Jason Goldberger',
    author_email='jlgoldb2@asu.edu',
    packages=["simple-sqlalchemy"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'pytest'
    ],
    test_suite='tests'
)