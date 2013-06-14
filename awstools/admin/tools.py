"""
Admin commands and utilities
"""
from time import strftime
import boto.ec2

from awstools.exceptions import ConfigurationError
from awstools.aws import Config
from awstools.ec2.instance import CurrentInstance, get_instances_tagged_with
from awstools.logger import get_logger

log = get_logger(__name__)


def backup_instances(access_key_id, secret_access_key, region, keep,
                     identifier, backup_tag, backup_tag_value,
                     backup_master_tag, backup_master_tag_value):
    """
    Backup instances, removing old snapshots.

    If a tag of Role exists on the instance, backups will be named
    'Role + timestamp + identifier'. Otherwise the value of the Name tag
    will be used (+ timestamp + identifier)

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
    if not identifier:
        msg = "Please pass a short identifier string"
        log.fatal(msg)
        raise ConfigurationError(msg)

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

    backup_masters = get_instances_tagged_with(conn, {
        backup_master_tag: backup_master_tag_value})

    current_instance_is_backup_master = False

    for backup_master in backup_masters:
        if current_instance.id == backup_master.__dict__['id']:
            current_instance_is_backup_master = True

    if not current_instance_is_backup_master:
        log.info("This instance is not the backup master. Aborting.")
        return False

    log.info("Running on the backup master. Searching for instances to "
             "backup...")

    instances_to_backup = get_instances_tagged_with(conn, {
        backup_tag: backup_tag_value})

    if not instances_to_backup or len(instances_to_backup) == 0:
        log.info("No instances tagged for backup.")
        return False

    log.info("%d instances need backing up" % len(instances_to_backup))

    for instance in instances_to_backup:
        log.info("Creating AMI of instance %s" % instance.__dict__['id'])
        now = strftime("%Y-%m-%d %H:%M:%S")
        try:
            instance_name = "%s__%s" % (instance.__dict__['tags']['Role'], now)
        except KeyError:
            try:
                instance_name = "%s__%s" % (instance.__dict__['tags']['Name'],
                                            now)
            except KeyError:
                instance_name = "Untitled-%s" % now

        instance_name += '__' + str(identifier)

        instance_name = instance_name.replace(' ', '-')[:128]
        instance_name = instance_name.replace(':', '-')

        log.debug("Image name will be '%s'" % instance_name)

        conn.create_image(instance_id=instance.__dict__['id'],
            name=instance_name,
            description="Automatic backup at %s" % (now),
            no_reboot=True)

        log.info("Instance %s snapshotted as %s" % (instance.__dict__['id'],
                instance_name))

    # delete old snapshots
    log.fatal("Implement deletion of old snapshots")
    # do this by searching for snapshots that match the identifier, and
    # delete [keep:] snapshots (those more than 'keep' when sorted)

