import boto.ec2

from awstools.exceptions import ConfigurationError
from awstools.logger import get_logger

log = get_logger(__name__)


class Config(object):
    """
    Contains config info relevant to most of the API
    """
    def __init__(self, access_key_id, secret_access_key, region):
        if not access_key_id or not secret_access_key or not region:
            raise ConfigurationError("You must provide access_key_id, "
                                     "secret_access_key and region")

        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region_name = region
        self.__endpoint = None

    @property
    def region_endpoint(self):
        """
        Return the endpoint associated with the current region
        :return:
        """
        if self.__endpoint:
            return self.__endpoint

        log.debug("Finding endpoint for region '%s'" % self.region_name)

        region = boto.ec2.get_region(self.region_name)

        if not region:
            msg = "Unable to retrieve region info for the region '%s'" % \
                  self.region_name
            log.fatal(msg)
            raise ConfigurationError(msg)

        self.__endpoint = region.endpoint

        log.debug("Region endpoint is '%s'" % self.__endpoint)
        return self.__endpoint
