[![build](https://github.com/davidkaggulire/designpatterns/actions/workflows/integrations.yml/badge.svg)](https://github.com/davidkaggulire/designpatterns/actions/workflows/integrations.yml)
[![codecov](https://codecov.io/gh/davidkaggulire/designpatterns/branch/main/graph/badge.svg?token=2O2F4RR1LD)](https://codecov.io/gh/davidkaggulire/designpatterns)

# designpatterns
Project to explore various design patterns i.e Singleton, Factory design pattern, Dependency injection and Interfaces using a file system provider

# Installation
$ git clone https://github.com/davidkaggulire/designpatterns.git

$ cd your-dir

$ pip install -r requirements.txt

# Tests
Enables you to run tests on the different parts of the application to ensure that they are running as intended.

**Running tests**

Open the terminal and type in the command below to run tests on the program.

`python3 -m unittest discover tests`

**Gather test coverage data**

Determine the percentage of code tested.

`coverage run -m unittest discover -s tests`

# Print / Output test coverage report

**Command-line report**

Use the commands below to print out a simple command-line report.

`coverage report -m`
