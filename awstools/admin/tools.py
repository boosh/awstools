"""
Admin commands and utilities
"""
import boto.ec2

from awstools.aws import Config
from awstools.ec2.instance import CurrentInstance
from awstools.logger import get_logger

log = get_logger(__name__)


def backup_instances(access_key_id, secret_access_key, region, keep,
                     identifier, backup_tag, backup_tag_value,
                     backup_master_tag, backup_master_tag_value):
    """
    Backup instances, removing old snapshots

    :param access_key_id:
    :param secret_access_key:
    :param region:
    :param keep:
    :param identifier:
    :param backup_tag:
    :param backup_tag_value:
    :param backup_master_tag:
    :param backup_master_tag_value:
    :return:
    """
    log.debug("Creating config object")
    config = Config(access_key_id=access_key_id,
        secret_access_key=secret_access_key, region=region)

    # get the current instance
    current_instance = CurrentInstance()

    if not current_instance.id:
        log.fatal("Not running on an EC2 instance. Aborting.")
        return False

    log.info("Current instance ID is %s" % current_instance.id)

    conn = boto.ec2.connect_to_region(config.region_name,
        aws_access_key_id=config.access_key_id,
        aws_secret_access_key=config.secret_access_key)

    # get the current instance
    reservations = conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]

    # get the tags of the current instance and see if we're the
    # backup master
    current_instance_tags = None

    for instance in instances:
        if instance.__dict__['id'] == current_instance.id:
            current_instance_tags = instance.__dict__['tags']

    log.debug("Tags on the current instance are: %s" % current_instance_tags)

    if not current_instance_tags or backup_master_tag not in \
            current_instance_tags or \
            current_instance_tags[backup_master_tag] != backup_master_tag_value:
        log.info("This instance is not the backup master. Aborting.")
        return False

    log.info("Running on the backup master. Searching for instances to "
             "backup...")

