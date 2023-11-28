import boto3
import copy
from datetime import datetime
import logging
import psycopg2
import psycopg2.extras
import time

from arcimoto.exceptions import *
import arcimoto.db
import arcimoto.runtime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Replicate:

    def __init__(self, env, rds_client=True):
        self.env = env
        if rds_client:
            self.rds_client = self.rds_client_init()

    def db_cluster_clone(self):
        '''
        This should be run on the child classes `ReplicateMain` or `ReplicateAuthkey`
        to have `self.db_config` set correctly.
        '''

        global logger

        db_cluster_identifier_source = self.prod_cluster_source

        logger.debug(f'db_cluster_identifier_source: {db_cluster_identifier_source}')

        # use env to choose config
        env_db_config = self.db_config
        logger.debug(f'env_db_config: {env_db_config}')
        db_cluster_identifier = env_db_config.get('db_cluster_identifier', None)
        parameter_group_name = env_db_config.get('parameter_group_name_cluster', None)
        security_group_identifiers = env_db_config.get('security_group_identifiers', None)
        subnet_group_name = env_db_config.get('subnet_group_name', None)

        try:
            clone_cluster_response = self.rds_client.restore_db_cluster_to_point_in_time(
                DBClusterIdentifier=db_cluster_identifier,
                SourceDBClusterIdentifier=db_cluster_identifier_source,
                VpcSecurityGroupIds=security_group_identifiers,
                UseLatestRestorableTime=True,
                RestoreType='copy-on-write',
                DBClusterParameterGroupName=parameter_group_name,
                DBSubnetGroupName=subnet_group_name,
                DeletionProtection=True,
                EnableIAMDatabaseAuthentication=True,
                CopyTagsToSnapshot=True,
                EnableCloudwatchLogsExports=[
                    'postgresql',
                ],
                Tags=[
                    {
                        'Key': 'Cost Center',
                        'Value': 'Telematics'
                    }
                ]
            )
        except Exception as e:
            raise ArcimotoReplicateAlertException(f'Could not clone DB cluster {db_cluster_identifier_source} as {db_cluster_identifier}: {e}')

        # check returned successfully
        if clone_cluster_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            logger.info(f'Successfully cloned DB cluster {db_cluster_identifier_source} as {db_cluster_identifier}')
        else:
            raise ArcimotoReplicateAlertException(f'Could not clone DB cluster for {db_cluster_identifier_source}')

        return {
            'db_cluster_identifier_source': db_cluster_identifier_source,
            'db_cluster_identifier': db_cluster_identifier
        }

    def db_cluster_delete(self, db_cluster_identifier):
        return self.rds_client.delete_db_cluster(
            DBClusterIdentifier=db_cluster_identifier,
            SkipFinalSnapshot=True
        )

    def db_cluster_exists(self, db_cluster_identifier):
        global logger

        try:
            db_status = self.rds_client.describe_db_clusters(
                DBClusterIdentifier=db_cluster_identifier
            )['DBClusters'][0]['Status']
        except self.rds_client.exceptions.DBClusterNotFoundFault as e:
            logger.info(f'DB {db_cluster_identifier} does not exist: {e}')
            return False

        logger.info(f'DB {db_cluster_identifier} exists, it is {db_status}')
        return True

    def db_cluster_instance_create(self):

        global logger

        # use env to choose config
        env_db_config = self.db_config
        db_instance_identifier = env_db_config.get('db_instance_identifier', None)
        db_cluster_identifier = env_db_config.get('db_cluster_identifier', None)
        parameter_group_name = env_db_config.get('parameter_group_name_instance', None)
        subnet_group_name = env_db_config.get('subnet_group_name', None)

        create_db_instance_response = self.rds_client.create_db_instance(
            DBInstanceIdentifier=db_instance_identifier,
            DBInstanceClass='db.t4g.medium',
            DBClusterIdentifier=db_cluster_identifier,
            Engine='aurora-postgresql',
            DBParameterGroupName=parameter_group_name,
            DBSubnetGroupName=subnet_group_name,
            PubliclyAccessible=False,
            AutoMinorVersionUpgrade=True,
            CopyTagsToSnapshot=True,
            Tags=[
                {
                    'Key': 'Cost Center',
                    'Value': 'Telematics'
                }
            ]
        )

        # check returned successfully
        if create_db_instance_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            logger.info(f'response:\n{create_db_instance_response}')
            logger.info(f'Successfully created DB instance {db_cluster_identifier} for cluster {db_instance_identifier}')
        else:
            raise ArcimotoReplicateAlertException(f'Could not create DB instance {db_instance_identifier} for cluster {db_cluster_identifier}')

        return {
            'db_cluster_identifier': db_cluster_identifier,
            'db_instance_identifier': db_instance_identifier
        }

    def db_cluster_remove_protection(self, db_cluster_identifier):
        try:
            modify_db_cluster_response = self.rds_client.modify_db_cluster(
                DBClusterIdentifier=db_cluster_identifier,
                ApplyImmediately=True,
                DeletionProtection=False
            )

            # check rename DB instance returned successfully
            if modify_db_cluster_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                logger.info(f'response:\n{modify_db_cluster_response}')
                logger.info(f'Successfully removed DB {db_cluster_identifier} deletion protection')
            else:
                raise ArcimotoReplicateAlertException(f'Could not remove DB {db_cluster_identifier} deletion protection')
        except self.rds_client.exceptions.DBClusterNotFoundFault as e:
            # if the db is not available to be renamed then that is fine, move on
            logger.warning(f'DB {db_cluster_identifier} not available to remove deletion protection: {e}')

    def db_cluster_rename(self, db_cluster_identifier, db_cluster_new_identifier=None):
        global logger

        # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime('%Y%m%d-%H%M%S')
        postfix = f'-retired-{dt_string}'

        db_cluster_new_identifier_input = None

        if db_cluster_new_identifier is None:
            db_cluster_new_identifier = f'{db_cluster_identifier}{postfix}'
        else:
            db_cluster_new_identifier_input = db_cluster_new_identifier

        # handle 63 max character length
        if len(db_cluster_new_identifier) > 63:
            postfix_length = len(postfix)
            db_cluster_new_identifier = db_cluster_identifier[:63 - postfix_length]
            if db_cluster_new_identifier_input is None:
                db_cluster_new_identifier += postfix

        # remove disallowed double hyphen
        db_cluster_new_identifier = db_cluster_new_identifier.replace('--', '-')

        try:
            rename_db_cluster_response = self.rds_client.modify_db_cluster(
                DBClusterIdentifier=db_cluster_identifier,
                ApplyImmediately=True,
                NewDBClusterIdentifier=db_cluster_new_identifier
            )

            # check rename DB instance returned successfully
            if rename_db_cluster_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                logger.info(f'response:\n{rename_db_cluster_response}')
                logger.info(f'Successfully renamed DB {db_cluster_identifier} to {db_cluster_new_identifier}')
            else:
                raise ArcimotoReplicateAlertException(f'Could not rename DB {db_cluster_identifier} to {db_cluster_new_identifier}')
        except self.rds_client.exceptions.DBClusterNotFoundFault as e:
            # if the db is not available to be renamed then that is fine, move on
            logger.warning(f'DB {db_cluster_identifier} not available to rename: {e}')

        return db_cluster_new_identifier

    def db_cluster_status_check(self, db_cluster_identifier):
        global logger

        try:
            db_status = self.rds_client.describe_db_clusters(
                DBClusterIdentifier=db_cluster_identifier
            )['DBClusters'][0]['Status']
        except self.rds_client.exceptions.DBClusterNotFoundFault as e:
            logger.info(f'DB {db_cluster_identifier} does not exist: {e}')
            return False

        if db_status != 'available':
            logger.warning(f'DB {db_cluster_identifier} is not available, it is {db_status}')
            return False
        logger.info(f'DB {db_cluster_identifier} is available')
        return True

    def db_instance_delete(self, db_instance_identifier):
        return self.rds_client.delete_db_instance(
            DBInstanceIdentifier=db_instance_identifier,
            SkipFinalSnapshot=True,
            DeleteAutomatedBackups=True
        )

    def db_instance_exists(self, db_instance_identifier):
        global logger

        try:
            db_status = self.rds_client.describe_db_instances(
                DBInstanceIdentifier=db_instance_identifier
            )['DBInstances'][0]['DBInstanceStatus']
        except self.rds_client.exceptions.DBInstanceNotFoundFault as e:
            logger.info(f'DB {db_instance_identifier} does not exist: {e}')
            return False

        logger.info(f'DB {db_instance_identifier} exists, it is {db_status}')
        return True

    def db_instance_rename(self, db_instance_identifier, db_instance_new_identifier=None):
        global logger

        # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime('%Y%m%d-%H%M%S')
        postfix = f'-retired-{dt_string}'

        db_instance_new_identifier_input = None

        if db_instance_new_identifier is None:
            db_instance_new_identifier = f'{db_instance_identifier}{postfix}'
        else:
            db_instance_new_identifier_input = db_instance_new_identifier

        # handle 63 max character length
        if len(db_instance_new_identifier) > 63:
            postfix_length = len(postfix)
            db_instance_new_identifier = db_instance_identifier[:63 - postfix_length]
            if db_instance_new_identifier_input is None:
                db_instance_new_identifier += postfix

        # remove disallowed double hyphen
        db_instance_new_identifier = db_instance_new_identifier.replace('--', '-')

        try:
            rename_db_instance_response = self.rds_client.modify_db_instance(
                DBInstanceIdentifier=db_instance_identifier,
                ApplyImmediately=True,
                NewDBInstanceIdentifier=db_instance_new_identifier
            )

            # check rename DB instance returned successfully
            if rename_db_instance_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                logger.info(f'response:\n{rename_db_instance_response}')
                logger.info(f'Successfully renamed DB {db_instance_identifier} to {db_instance_new_identifier}')
            else:
                raise ArcimotoReplicateAlertException(f'Could not rename DB {db_instance_identifier} to {db_instance_new_identifier}')
        except self.rds_client.exceptions.DBInstanceNotFoundFault as e:
            # if the db is not available to be renamed then that is fine, move on
            logger.warning(f'DB {db_instance_identifier} not available to rename')

        return db_instance_new_identifier

    def db_instance_status_check(self, db_instance_identifier):
        global logger

        try:
            db_status = self.rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)['DBInstances'][0]['DBInstanceStatus']
        except self.rds_client.exceptions.DBInstanceNotFoundFault as e:
            logger.info(f'DB {db_instance_identifier} does not exist')
            return False

        if db_status != 'available':
            logger.warning(f'DB {db_instance_identifier} is not available, it is {db_status}')
            return False
        logger.info(f'DB {db_instance_identifier} is available')
        return True

    def db_instance_users_restore(self):
        global logger

        db_connection_info = self.get_db_connection_info()

        # use the existing prod sysadmin user to connect to the restored db
        db_restored_sysadmin_conn_info = copy.deepcopy(db_connection_info['prod']['sysadmin'])

        # will work in reality and for using unittest db
        host_parts = db_connection_info[self.env]['sysadmin']['host'].split('.')
        host_parts[0] = self.db_config.get('db_cluster_identifier', '')
        db_restored_sysadmin_conn_info['host'] = '.'.join(host_parts)

        conn = self.get_conn(db_restored_sysadmin_conn_info)
        cursor = conn.cursor()

        # change users passwords
        for db_connection_type in db_connection_info[self.env]:
            # this will cause the username to match the prod env
            # we want this going forward but will have repurcusions requiring updates
            # to the secret data for dev and staging once they are replicated
            username = db_connection_info['prod'][db_connection_type]['username']
            password = db_connection_info[self.env][db_connection_type]['password']
            self.user_set_password(cursor, username, password)

        conn.commit()
        conn.close()

        return {}

    def get_conn(self, db_connection_info):
        try:
            conn_string = 'dbname={} user={} host={} password={}'.format(
                db_connection_info['dbname'],
                db_connection_info['username'],
                db_connection_info['host'],
                db_connection_info['password']
            )
            conn = psycopg2.connect(conn_string, cursor_factory=psycopg2.extras.DictCursor)
            return conn

        except Exception as e:
            raise ArcimotoReplicateAlertException('Unable to open DB connection: {}'.format(e)) from e

    def get_db_connection_info(self):
        db_connection_info = {
            self.env: {},
            'prod': {}
        }
        db_connection_info['prod'] = self.get_secrets('prod')
        # get env being restored secret names
        db_connection_info[self.env] = self.get_secrets(self.env)
        return db_connection_info

    def get_secrets(self, env):
        secrets_data = {}
        db_connection_types = self.secret_names[env]
        for db_connection_type in db_connection_types:
            secret_name = db_connection_types[db_connection_type]
            secrets_data[db_connection_type] = arcimoto.runtime.get_secret(secret_name)
        return secrets_data

    def rds_client_init(self):
        return boto3.client(
            service_name='rds',
            region_name='us-west-2'
        )

    def user_set_password(self, cursor, username, password):
        global logger

        query = (
            f'ALTER ROLE {username} '
            f"WITH PASSWORD '{password}'"
        )
        cursor.execute(query)


class ReplicateAuthkey(Replicate):
    def __init__(self, env, rds_client=True):
        super().__init__(env, rds_client)

    @property
    def db_config(self):
        dev = {
            'db_cluster_identifier': 'tel-authkey-db-dev-auroradbcluster-1h1zls0pm3zn0',
            'db_instance_identifier': 'ta1h858bdayn0w3',
            'parameter_group_name_cluster': 'tel-authkey-db-dev-rdsdbclusterparametergroup-nsgaykyb0apz',
            'parameter_group_name_instance': 'tel-authkey-db-dev-dbparamgroup-1whri0jwwoop3',
            'security_group_identifiers': ['sg-0fee2eaac0db59d3d'],
            'subnet_group_name': 'tel-authkey-db-dev-dbsubnetgroup-cupjetntn7hq'
        }
        staging = {
            'db_cluster_identifier': 'tel-authkey-db-staging-auroradbcluster-1nzlavkvjvmb2',
            'db_instance_identifier': 'taz1h40irkeopr',
            'parameter_group_name_cluster': 'tel-authkey-db-staging-rdsdbclusterparametergroup-cbkdsnmde6yn',
            'parameter_group_name_instance': 'tel-authkey-db-staging-dbparamgroup-16xhupw9hk4hs',
            'security_group_identifiers': ['sg-0eb01d7541f7fcdfd'],
            'subnet_group_name': 'tel-authkey-db-staging-dbsubnetgroup-150jgeb4lr4i8'
        }
        return staging if self.env == 'staging' else dev

    def prefix_vins(self):
        global logger

        db_connection_info = self.get_db_connection_info()

        # use the existing sysadmin user to connect to the restored db
        db_restored_sysadmin_conn_info = copy.deepcopy(db_connection_info['prod']['sysadmin'])
        # but use the password from the user for the env that was restored in last step
        db_restored_sysadmin_conn_info['password'] = db_connection_info[self.env]['sysadmin']['password']

        # will work in reality and for using unittest db
        host_parts = db_connection_info[self.env]['sysadmin']['host'].split('.')
        host_parts[0] = self.db_config.get('db_cluster_identifier', '')
        db_restored_sysadmin_conn_info['host'] = '.'.join(host_parts)

        conn = self.get_conn(db_restored_sysadmin_conn_info)
        cursor = conn.cursor()

        tables = [  # tables that have a foreign key reference to vehicle:vin are left out
            'vehicle_authority',
            'vehicle_meta'
        ]
        if self.env == 'dev':
            env_prefix = 'DEV-'
        elif self.env == 'staging':
            env_prefix = 'STAGE-'

        # loop over tables that just need the vin replaced in all cases
        for table in tables:
            query = (
                f'UPDATE {table} '
                f"SET vin = CONCAT('{env_prefix}', vin)"
            )
            cursor.execute(query)

        conn.commit()
        conn.close()

    @property
    def prod_cluster_source(self):
        return 'tel-authkey-db-prod-auroradbcluster-gp0nmqa9ii2t'

    @property
    def secret_names(self):
        secret_names = {
            'dev': {
                'read': 'dev-pgsql-authkey-read',
                'write': 'dev-pgsql-authkey-write',
                'sysadmin': 'dev-pgsql-authkey'
            },
            'staging': {
                'read': 'staging-pgsql-authkey-read',
                'write': 'staging-pgsql-authkey-write',
                'sysadmin': 'staging-pgsql-authkey'
            },
            'prod': {
                'read': 'pgsql-authkey-read',
                'write': 'pgsql-authkey-write',
                'sysadmin': 'pgsql-authkey'
            }
        }
        return secret_names


class ReplicateMain(Replicate):
    def __init__(self, env, rds_client=True):
        super().__init__(env, rds_client)

    @property
    def db_config(self):
        dev = {
            'db_cluster_identifier': 'tel-main-db-dev-auroradbcluster-1pg6l9kfl9qdb',
            'db_instance_identifier': 'ta15hrvemqo89ft',
            'parameter_group_name_cluster': 'tel-main-db-dev-rdsdbclusterparametergroup-ter8ryq93imi',
            'parameter_group_name_instance': 'tel-main-db-dev-dbparamgroup-gnkh3e5miujv',
            'security_group_identifiers': ['sg-014114218009c11fc'],
            'subnet_group_name': 'tel-main-db-dev-dbsubnetgroup-6ceeo3gtec7o'
        }
        staging = {
            'db_cluster_identifier': 'tel-main-db-staging-auroradbcluster-6ntob7x6ajn5',
            'db_instance_identifier': 'ta1rn3qhtdvcpg5',
            'parameter_group_name_cluster': 'tel-main-db-staging-rdsdbclusterparametergroup-1684j55aooqdp',
            'parameter_group_name_instance': 'tel-main-db-staging-dbparamgroup-1wmqhasixk2fv',
            'security_group_identifiers': ['sg-02a7a3c93dc9ac8a8'],
            'subnet_group_name': 'tel-main-db-staging-dbsubnetgroup-xxto31hqskl2'
        }
        return staging if self.env == 'staging' else dev

    def prefix_vins(self):
        global logger

        db_connection_info = self.get_db_connection_info()

        # use the existing sysadmin user to connect to the restored db
        db_restored_sysadmin_conn_info = copy.deepcopy(db_connection_info['prod']['sysadmin'])
        # but use the password from the user for the env that was restored in last step
        db_restored_sysadmin_conn_info['password'] = db_connection_info[self.env]['sysadmin']['password']

        # will work in reality and for using unittest db
        host_parts = db_connection_info[self.env]['sysadmin']['host'].split('.')
        host_parts[0] = self.db_config.get('db_cluster_identifier', '')
        db_restored_sysadmin_conn_info['host'] = '.'.join(host_parts)

        conn = self.get_conn(db_restored_sysadmin_conn_info)
        cursor = conn.cursor()

        tables = [  # tables that have a foreign key reference to vehicle:vin are left out
            'managed_sessions',
            'managed_sessions_reef',
            'managed_sessions_vehicles',
            'telemetry_points',
            'vehicle',
            'vehicle_join_vehicle_group',
            'vehicle_meta',
            'vehicle_recalls'
        ]
        if self.env == 'dev':
            env_prefix = 'DEV-'
        elif self.env == 'staging':
            env_prefix = 'STAGE-'

        # special case - notes (object_id where object type = 'Vehicle')
        query = (
            'UPDATE notes '
            f"SET object_id = CONCAT('{env_prefix}', object_id) "
            "WHERE object_type = 'Vehicle'"
        )
        cursor.execute(query)

        # loop over tables that just need the vin replaced in all cases
        for table in tables:
            query = (
                f'UPDATE {table} '
                f"SET vin = CONCAT('{env_prefix}', vin)"
            )
            cursor.execute(query)

        conn.commit()
        conn.close()

    @property
    def prod_cluster_source(self):
        return 'tel-main-db-prod-auroradbcluster-1kkvd236ktt8q'

    @property
    def secret_names(self):
        secret_names = {
            'dev': {
                'read': 'dev-telemetryam-read',
                'write': 'dev-telemetryam-write',
                'sysadmin': 'dev-telemetryam-sysadmin'
            },
            'staging': {
                'read': 'staging-telemetryam-read',
                'write': 'staging-telemetryam-write',
                'sysadmin': 'staging-telemetryam-sysadmin'
            },
            'prod': {
                'read': 'telemetryam-read',
                'write': 'telemetryam-write',
                'sysadmin': 'telemetryam-sysadmin'
            }
        }
        return secret_names
