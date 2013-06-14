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
        if self.__instance_id != False:
            return self.__instance_id

        instance_id = None
        try:
            r = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
            instance_id = r.text
        except requests.exceptions.ConnectionError:
            pass

        self.__instance_id = instance_id

        return instance_id