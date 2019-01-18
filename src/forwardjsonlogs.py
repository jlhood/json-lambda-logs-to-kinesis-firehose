"""Lambda function handler."""

# must be the first import in files with lambda function handlers
import lambdainit  # noqa: F401

import base64
import gzip
import json

import boto3

import config
import lambdalogging

LOG = lambdalogging.getLogger(__name__)
FIREHOSE = boto3.client('firehose')


def handler(event, context):
    """Forward JSON-formatted CW Log events to Firehose Delivery Stream."""
    LOG.debug('Received event: %s', event)

    log_messages = _get_log_messages(event)
    for log_message in log_messages:
        if _is_json(log_message):
            if not log_message.endswith('\n'):
                log_message += '\n'

            FIREHOSE.put_record(
                DeliveryStreamName=config.DELIVERY_STREAM_NAME,
                Record={
                    'Data': log_message
                }
            )


def _get_log_messages(event):
    data = json.loads(gzip.decompress(base64.b64decode(event['awslogs']['data'])))
    return [log_event['message'] for log_event in data['logEvents']]


def _is_json(s):
    try:
        LOG.debug('Attempting to deserialize as JSON: %s', s)
        json.loads(s)
        return True
    except json.decoder.JSONDecodeError:
        LOG.debug('String is not JSON')
        return False
