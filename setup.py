from setuptools import setup

project = "flask-simple-alchemy"

setup(
    name=project,
    version='0.1.0',
    url='https://github.com/jlgoldb2/flask-simple-alchemy',
    description='A Simplification of SQLAlchemy\'s declarative using '\
        + ' Flask-SQLAlchemy',
    author='Jason Goldberger',
    license='MIT',
    author_email='jlgoldb2@asu.edu',
    packages=["simple_sqlalchemy"],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'pytest'
    ],
    test_suite='tests'
)