from setuptools import setup

project = "flask-simple-alchemy"

setup(
    name=project,
    version='0.3.0',  # Alpha Release
    url='https://github.com/jlgoldb2/flask-simple-alchemy',
    description='A Simplification of SQLAlchemy\'s declarative using'
                ' Flask-SQLAlchemy',
    author='Jason Goldberger',
    license='MIT',
    author_email='jlgoldb2@asu.edu',
    packages=["flask_simple_alchemy"],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'pytest',
        'testfixtures'
    ],
    test_suite='tests'
)
