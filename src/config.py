"""Environment configuration values used by lambda functions."""

import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
DELIVERY_STREAM_NAME = os.getenv('DELIVERY_STREAM_NAME')
