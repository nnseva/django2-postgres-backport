AUTHOR = 'Vsevolod Novikov'
AUTHOR_EMAIL = 'nnseva@gmail.com'
URL = 'https://github.com/nnseva/django2-postgres-backports'

import django2_postgres

from setuptools import setup, find_packages

description = 'Django 2.x PostgreSQL backports collection'

with open('README.rst') as f:
    long_description = f.read()

setup(
    name = 'django2-postgres-backports',
    version = django2_postgres.__version__,
    description = description,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    long_description = long_description,
    packages = [
        'django2_postgres',
    ],
    include_package_data = True,
    zip_safe = False,
    install_requires=['packaging']
)
