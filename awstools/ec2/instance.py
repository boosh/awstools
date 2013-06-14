import os
import requests

from awstools.logger import get_logger

log = get_logger(__name__)


class CurrentInstance(object):
    """
    Methods on the instance currently executing this code
    """
    def __init__(self):
        self.__instance_id = False

    @property
    def id(self):
        """
        Returns the Instance ID of the instance executing this script

        :return:
        """
        log.debug("Cached instance ID is %s" % self.__instance_id)
        if self.__instance_id is not False:
            return self.__instance_id

        instance_id = None
        try:
            r = requests.get(
                'http://169.254.169.254/latest/meta-data/instance-id')
            instance_id = r.text
        except requests.exceptions.ConnectionError:
            if 'MOCK_AWSTOOLS_INSTANCE' in os.environ:
                instance_id = os.environ['MOCK_AWSTOOLS_INSTANCE']

        self.__instance_id = instance_id

        return instance_id


def get_instances_tagged_with(conn, tags):
    """
    Returns instances tagged with the given tags

    :param conn:
    :param tags: dict of tags to check. All must be present
    :return: list of instances with the tags
    """
    log.debug("Searching for instances tagged with: '%s'" % tags)

    # get all instances
    reservations = conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]

    filtered_instances = []

    # iterate through all instances
    for instance in instances:
        # iterate through all of our filter tags
        all_tags_found = True
        for tag in tags:
            if tag[0] not in instance.__dict__['tags'] or \
                    instance.__dict__['tags'][tag[0]] != tag[1]:
                log.debug("Instance '%s' filtered out" % instance.id)
                all_tags_found = False

        if all_tags_found:
            log.debug("Instance '%s' is tagged with all tags" % instance.id)
            filtered_instances.append(instance)

    log.debug("Returning filtered instances: %s" % filtered_instances)

    return filtered_instances
