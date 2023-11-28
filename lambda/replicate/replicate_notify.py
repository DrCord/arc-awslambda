import logging
import json

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.note

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'event': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'message_addendum': {
        'type': 'string',
        'nullable': True,
        'default': None
    },
    'source': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'event_data': {
        'type': 'dict',
        'default': None,
        'nullable': True
    },
    'severity': {
        'type': 'string',
        'default': 'INFO',
        'allowed': [
            'INFO',
            'WARNING',
            'ERROR',
            'CRITICAL'
        ]
    }
})

# all available severity levels that work with arcimoto.note.Notification
SEVERITY_CRITICAL = 'CRITICAL'
SEVERITY_ERROR = 'ERROR'
SEVERITY_WARNING = 'WARNING'
SEVERITY_INFO = 'INFO'

_DEFAULT_SEVERITY = SEVERITY_INFO


@arcimoto.runtime.handler
def replicate_notify(event, message_addendum, source, event_data=None, severity=_DEFAULT_SEVERITY):
    try:
        msg_lines = [
            'Replicate DB',
            event
        ]
        msg = '\n'.join(msg_lines)
        if message_addendum is not None:
            msg += f'\n' + message_addendum
        if event_data is not None:
            msg += f'\n\n' + json.dumps(event_data)

        arcimoto.note.ReplicateNotification(
            message=msg,
            source=source,
            source_type='state_machine',
            severity=severity
        )
    except Exception as e:
        raise ArcimotoReplicateAlertException(f'Failed to send {event} {message_addendum} notification from {source} replication state machine: {e}')

    return {}


lambda_handler = replicate_notify
