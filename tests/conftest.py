# conftest.py

def pytest_addoption(parser):
    parser.addoption("--service", action="store", default="local")
    parser.addoption("--db", action="store", default="inmemory")