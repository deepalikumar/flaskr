from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask >= 1.0.2, < 1.1',
        'pytest >= 4.0.2, < 4.1',
        'flask-sqlalchemy >= 2.3.2, < 2.4',
        'gunicorn',
    ],
)