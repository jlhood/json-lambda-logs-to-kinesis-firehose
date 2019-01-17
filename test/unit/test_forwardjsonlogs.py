import pytest
import forwardjsonlogs


def test_handler(mocker):
    forwardjsonlogs.handler({}, None)
