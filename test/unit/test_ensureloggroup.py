import pytest
import botocore

import ensureloggroup

LOG_GROUP_NAME = 'myLogGroup'
PHYSICAL_RESOURCE_ID = 'someUUID'


@pytest.fixture
def mock_cw_logs(mocker):
    mocker.patch.object(ensureloggroup, 'CW_LOGS')
    return ensureloggroup.CW_LOGS


def test_create_log_group_no_exist(mock_cw_logs, mocker):
    mocker.patch.object(ensureloggroup, 'uuid')
    ensureloggroup.uuid.uuid4.return_value = PHYSICAL_RESOURCE_ID

    response = ensureloggroup.create(_mock_event(), None)

    assert response == {
        'Status': 'SUCCESS',
        'PhysicalResourceId': PHYSICAL_RESOURCE_ID,
        'Data': {
            'LogGroupName': LOG_GROUP_NAME
        }
    }

    ensureloggroup.uuid.uuid4.assert_called()
    ensureloggroup.CW_LOGS.create_log_group.assert_called_with(
        logGroupName=LOG_GROUP_NAME
    )


def test_create_log_group_already_exists(mock_cw_logs, mocker):
    mocker.patch.object(ensureloggroup, 'uuid')
    ensureloggroup.uuid.uuid4.return_value = PHYSICAL_RESOURCE_ID
    ensureloggroup.CW_LOGS.create_log_group.side_effect = botocore.exceptions.ClientError(
        {
            'Error': {
                'Code': 'ResourceAlreadyExistsException'
            }
        },
        None
    )

    response = ensureloggroup.create(_mock_event(), None)

    assert response == {
        'Status': 'SUCCESS',
        'PhysicalResourceId': PHYSICAL_RESOURCE_ID,
        'Data': {
            'LogGroupName': LOG_GROUP_NAME
        }
    }

    ensureloggroup.uuid.uuid4.assert_called()
    ensureloggroup.CW_LOGS.create_log_group.assert_called_with(
        logGroupName=LOG_GROUP_NAME
    )


def test_create_log_group_other_error(mock_cw_logs, mocker):
    mocker.patch.object(ensureloggroup, 'uuid')
    ensureloggroup.uuid.uuid4.return_value = PHYSICAL_RESOURCE_ID
    ensureloggroup.CW_LOGS.create_log_group.side_effect = botocore.exceptions.ClientError(
        {
            'Error': {
                'Code': 'SomethingElse'
            }
        },
        None
    )

    with pytest.raises(botocore.exceptions.ClientError):
        ensureloggroup.create(_mock_event(), None)


def test_update_log_group_no_exist(mock_cw_logs, mocker):
    response = ensureloggroup.update(_mock_event(), None)

    assert response == {
        'Status': 'SUCCESS',
        'PhysicalResourceId': PHYSICAL_RESOURCE_ID,
        'Data': {
            'LogGroupName': LOG_GROUP_NAME
        }
    }

    ensureloggroup.CW_LOGS.create_log_group.assert_called_with(
        logGroupName=LOG_GROUP_NAME
    )


def test_update_log_group_already_exists(mock_cw_logs, mocker):
    ensureloggroup.CW_LOGS.create_log_group.side_effect = botocore.exceptions.ClientError(
        {
            'Error': {
                'Code': 'ResourceAlreadyExistsException'
            }
        },
        None
    )

    response = ensureloggroup.update(_mock_event(), None)

    assert response == {
        'Status': 'SUCCESS',
        'PhysicalResourceId': PHYSICAL_RESOURCE_ID,
        'Data': {
            'LogGroupName': LOG_GROUP_NAME
        }
    }

    ensureloggroup.CW_LOGS.create_log_group.assert_called_with(
        logGroupName=LOG_GROUP_NAME
    )


def test_update_log_group_other_error(mock_cw_logs, mocker):
    ensureloggroup.CW_LOGS.create_log_group.side_effect = botocore.exceptions.ClientError(
        {
            'Error': {
                'Code': 'SomethingElse'
            }
        },
        None
    )

    with pytest.raises(botocore.exceptions.ClientError):
        ensureloggroup.update(_mock_event(), None)


def test_delete(mock_cw_logs, mocker):
    response = ensureloggroup.delete(_mock_event(), None)

    assert response == {
        'Status': 'SUCCESS',
        'PhysicalResourceId': PHYSICAL_RESOURCE_ID,
        'Data': {
            'LogGroupName': None
        }
    }

    ensureloggroup.CW_LOGS.create_log_group.assert_not_called()


def _mock_event():
    return {
        'PhysicalResourceId': PHYSICAL_RESOURCE_ID,
        'ResourceProperties': {
            'LogGroupName': LOG_GROUP_NAME
        }
    }
