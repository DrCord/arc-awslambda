import logging
import psycopg2

from arcimoto.exceptions import *
import arcimoto.runtime
import arcimoto.args
import arcimoto.db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

arcimoto.args.register({
    'filename': {
        'type': 'string',
        'required': True,
        'empty': False
    }
})


@arcimoto.runtime.handler
def util_users_execute_sql(filename):
    global logger

    conn = get_new_conn()
    cursor = conn.cursor()

    try:
        cursor.execute(open('schema/' + filename, 'r').read())
        # remove this logging statement for queries that do not return to prevent error
        logger.debug(cursor.fetchall())

        conn.commit()

    except Exception as e:
        if conn is not None:
            conn.rollback()
        logger.exception(f'util_users_execute_sql failed, error: {e}')
        raise

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

    return {}


def get_new_conn():
    '''
    Used to prevent the execute_sql lambdas that are all run in LATEST mode
    from using a cached connection and therefore potentially reaching an unintended ENV
    '''
    role_name = arcimoto.runtime.get_role()
    secret_name = ".".join([role_name, 'db', arcimoto.runtime.get_env()])
    secret = arcimoto.runtime.get_secret(secret_name)
    conn_string = 'dbname={} user={} host={} password={}'.format(
        secret['dbname'],
        secret['username'],
        secret['host'],
        secret['password']
    )
    conn = psycopg2.connect(conn_string, cursor_factory=psycopg2.extras.DictCursor)
    return conn


lambda_handler = util_users_execute_sql
