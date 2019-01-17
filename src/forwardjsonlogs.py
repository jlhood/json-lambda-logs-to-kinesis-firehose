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

    log_message = _get_log_message(event)
    LOG.debug('Attempting to deserialize log message as JSON: %s', log_message)
    try:
        json.loads(log_message)
    except json.decoder.JSONDecodeError:
        LOG.debug('Log message is not valid JSON. Ignore.')
        return

    if not log_message.endswith(b'\n'):
        log_message += b'\n'

    FIREHOSE.put_record(
        DeliveryStreamName=config.DELIVERY_STREAM_NAME,
        Record={
            'Data': log_message
        }
    )


def _get_log_message(event):
    data = event['awslogs']['data']
    return gzip.decompress(base64.b64decode(data))
