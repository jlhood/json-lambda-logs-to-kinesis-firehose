"""Custom Resource function handler ensuring log group exists."""

# must be the first import in files with lambda function handlers
import lambdainit  # noqa: F401

import uuid

import boto3
import botocore
import cfn_resource

import lambdalogging

LOG = lambdalogging.getLogger(__name__)
CW_LOGS = boto3.client('logs')
handler = cfn_resource.Resource()


@handler.create
def create(event, context):
    """Ensure given log group name exists."""
    LOG.debug('CustomResource create handler called with event: %s', event)
    physical_resource_id = str(uuid.uuid4())
    props = event['ResourceProperties']
    _ensure_log_group_exists(props['LogGroupName'])
    return _response(physical_resource_id, props['LogGroupName'])


@handler.update
def update(event, context):
    """Ensure given log group name exists."""
    LOG.debug('CustomResource update handler called with event: %s', event)
    physical_resource_id = event['PhysicalResourceId']
    props = event['ResourceProperties']
    _ensure_log_group_exists(props['LogGroupName'])
    return _response(physical_resource_id, props['LogGroupName'])


@handler.delete
def delete(event, context):
    """No-op on delete."""
    LOG.debug('CustomResource delete handler called with event: %s', event)
    physical_resource_id = event['PhysicalResourceId']
    return _response(physical_resource_id, None)


def _ensure_log_group_exists(log_group_name):
    try:
        LOG.debug("Attempting to create log group: %s", log_group_name)
        CW_LOGS.create_log_group(
            logGroupName=log_group_name
        )
        LOG.info("Log group created: %s", log_group_name)
    except botocore.errorfactory.ResourceAlreadyExistsException:
        LOG.debug("Log group already exists: %s", log_group_name)


def _response(physical_resource_id, log_group_name):
    response = {
        "Status": "SUCCESS",
        "PhysicalResourceId": physical_resource_id,
        "Data": {
            "LogGroupName": log_group_name
        }
    }
    LOG.debug('Returning response: %s', response)
    return response
