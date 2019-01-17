import pytest
import base64
import gzip

import test_constants
import forwardjsonlogs


@pytest.fixture
def mock_firehose(mocker):
    mocker.patch.object(forwardjsonlogs, 'FIREHOSE')
    return forwardjsonlogs.FIREHOSE


def test_handler_valid_json(mock_firehose):
    log_message = '{"a":1,"b":"foo"}'
    forwardjsonlogs.handler(_mock_log_event(log_message), None)
    mock_firehose.put_record.assert_called_with(
        DeliveryStreamName=test_constants.DELIVERY_STREAM_NAME,
        Record={
            'Data': bytes(log_message + '\n', 'utf-8')
        }
    )


def test_handler_valid_json_with_trailing_newline(mock_firehose):
    log_message = '{"a":1,"b":"foo"}\n'
    forwardjsonlogs.handler(_mock_log_event(log_message), None)
    mock_firehose.put_record.assert_called_with(
        DeliveryStreamName=test_constants.DELIVERY_STREAM_NAME,
        Record={
            'Data': bytes(log_message, 'utf-8')
        }
    )


def test_handler_invalid_json(mock_firehose):
    forwardjsonlogs.handler(_mock_log_event('not json'), None)
    mock_firehose.put_record.assert_not_called()


def _mock_log_event(log_message):
    data = base64.b64encode(gzip.compress(bytes(log_message, 'utf-8')))
    return {
        'awslogs': {
            'data': data
        }
    }
