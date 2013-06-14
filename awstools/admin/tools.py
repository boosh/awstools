"""
Admin commands and utilities
"""
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
        print current_instance.id
        print current_instance.id
        log.fatal("Not running on an EC2 instance. Aborting.")
        return False