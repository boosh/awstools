
class Config(object):
    """
    Contains config info relevant to most of the API
    """
    def __init__(self, access_key_id, secret_access_key, region):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region = region