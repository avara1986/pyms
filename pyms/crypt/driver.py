import logging
from abc import ABC, abstractmethod

from pyms.config.resource import ConfigResource
from pyms.constants import CRYPT_BASE, LOGGER_NAME
from pyms.utils import import_from

logger = logging.getLogger(LOGGER_NAME)


class CryptAbstract(ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def encrypt(self, message):
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, encrypted):
        raise NotImplementedError


class CryptNone(CryptAbstract):

    def encrypt(self, message):
        return message

    def decrypt(self, encrypted):
        return encrypted


class CryptResource(ConfigResource):
    """This class works between `pyms.flask.create_app.Microservice` and `pyms.flask.services.[THESERVICE]`. Search
    for a file with the name you want to load, set the configuration and return a instance of the class you want
    """
    config_resource = CRYPT_BASE

    def get_crypt(self, *args, **kwargs) -> CryptAbstract:
        if self.config.method == "fernet":
            crypt_object = import_from("pyms.crypt.fernet", "Crypt")
        elif self.config.method == "aws_kms":
            crypt_object = import_from("pyms.cloud.aws.kms", "Crypt")
        else:
            crypt_object = CryptNone
        logger.debug("Init crypt {}".format(crypt_object))
        return crypt_object(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.get_crypt(*args, **kwargs)