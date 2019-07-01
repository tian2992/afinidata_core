# Afinidata Core

## Overview


Afinidata Core is a Django app designed to hold info regarding users, instances (of children), sessions, chatbot integration data and other operative data from Afinidata.

Core is built using Python3, Django, and a small set of extra dependencies. The directory layout is quite standard for Django projects. The aim is to migrate significant services to Django REST on the future.


## Installation / Running

1. Install Python 3.6 or more as suggested by your OS.
2. Install dependencies, a suggested way is to use virtualenv: ```virtualenv -p python3 venv/; source venv/bin/activate; pip install -r requirements.txt```
3. Run ```manage.py``` and build and execute db migrations. MySQL is used in production, while a stub config exists for running using SQLite. 
4. Ready to go! Use the WSGI app exposed as content_manager

## Contributing

The Afinidata Content Manager is a Free Software Product created by Afinidata and available under the AGPL Licence. 

To contribute, read our [Code of Conduct](CODE_OF_CONDUCT.md), code away. Contact us via github issues or via email.
Create a pull request and contact us in order to merge your suggested changes. We suggest the use of git flow in order to provide a better contributing experience.

