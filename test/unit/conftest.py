"""Setup unit test environment."""

import sys
import os

import test_constants

# make sure tests can import the app code
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../../src/')

# set expected config environment variables to test constants
os.environ['LOG_LEVEL'] = test_constants.LOG_LEVEL
os.environ['DELIVERY_STREAM_NAME'] = test_constants.DELIVERY_STREAM_NAME
