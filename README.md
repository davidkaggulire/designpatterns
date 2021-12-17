[![build](https://github.com/davidkaggulire/designpatterns/actions/workflows/main.yml/badge.svg)](https://github.com/davidkaggulire/designpatterns/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/davidkaggulire/designpatterns/branch/main/graph/badge.svg?token=2O2F4RR1LD)](https://codecov.io/gh/davidkaggulire/designpatterns)

# designpatterns
Project to explore various design patterns i.e Singleton, Factory design pattern, Dependency injection and Interfaces using different sets of providers i.e. InMemory, FileSystem, SQL(postgreSQL) and NoSQL(using MongoDB Atlas).
The project also tests the design patterns with the disk file storage and Firebase Storage(using the firebase_admin sdk).

# Installation
$ git clone https://github.com/davidkaggulire/designpatterns.git

$ cd `your-dir`

Create virtual environment using command below

$ python3 -m venv `venv`

Activate virtual environment
`source venv/bin/activate`

$ pip install -r requirements.txt

# Run project
Navigate to the root folder and run 

`python phone_book.py` for the DB provider 

Run `python store_service.py` for the storage service provider

# Tests
Enables you to run tests on the different parts of the application to ensure that they are running as intended.

**Running tests**

Open the terminal and type in the command below to run tests on the program.

`pytest --cov=tests/`

## Print / Output test coverage report

**Command-line report**

Use the commands below to print out a simple command-line report.

`coverage report -m`


