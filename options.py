import sys
import unittest
from flask_app import app


RUN_SERVER_COMMAND = 'runserver'
RUN_TESTS_COMMAND = 'runtests'


if len(sys.argv) == 2:
    command = sys.argv[1]
    if command == RUN_SERVER_COMMAND:
        print('running the server')
        app.run()
    if command == RUN_TESTS_COMMAND:
        print('running tests')
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)

