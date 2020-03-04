from data_resource_api.app.utils.descriptor import (
    Descriptor,
    DescriptorsGetter)
from data_resource_api.app.utils.db_handler import DBHandler
from data_resource_api.app.utils.config import ConfigFunctions
from data_resource_api.config import ConfigurationFactory
from data_resource_api.db import Base, Session, Checksum
from data_resource_api.factories import ORMFactory
from data_resource_api.logging import LogFactory
from data_resource_api.utils import exponential_backoff


class DataManager(object):
    def __init__(self, logger_name: str = "data-manager", **kwargs):
        base = kwargs.get('base', Base)
        use_local_dirs = kwargs.get('use_local_dirs', True)
        descriptors = kwargs.get('descriptors', [])

        self.app_config = ConfigurationFactory.from_env()
        self.config = ConfigFunctions(self.app_config)

        self.db = DBHandler(self.config)

        self.orm_factory = ORMFactory(base)
        self.logger = LogFactory.get_console_logger(logger_name)

        self.descriptor_directories = []
        if use_local_dirs:
            self.descriptor_directories.append(
                self.config.get_data_resource_schema_path())

        self.custom_descriptors = descriptors

        self.data_store = []

    # ?? fns
    def data_exists(self, data_name: str, attr_getter):
        for data_object in self.data_store:
            if attr_getter(data_object).lower() == data_name.lower():
                return True
        return False

    def data_changed(self, data_name, checksum, name_getter, checksum_getter):
        for data_object in self.data_store:
            same_name = name_getter(data_object).lower == data_name.lower
            same_checksum = checksum_getter(data_object) != checksum
            if same_name and same_checksum:
                return True
        return False

    def get_data_index(self, data_name, name_getter):
        """Retrieves the index of a specific data resource in the data resources dict.

        Args:
           data_resource_name (str): Name of the data resource file on disk.

        Returns:
            int: Index of the data resource stored in memory, or -1 if not found.
        """
        index = -1
        for idx, data_object in enumerate(self.data_store):
            if name_getter(data_object) == data_name.lower():
                return idx
        return index
