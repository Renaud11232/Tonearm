import os
from injector import singleton, inject

from tonearm.configuration import Configuration

from .base import StorageBase


@singleton
class StorageService(StorageBase):

    @inject
    def __init__(self, configuration: Configuration):
        super().__init__(os.path.join(configuration.data_path, "global.json"))
