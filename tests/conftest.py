"""Pytest Fixtures"""

import os
import pytest
import docker
from data_resource_api import ConfigurationFactory
# from data_resource_api.app.data_resource_manager import DataResourceManager
from data_resource_api.app.data_model_manager import DataModelManagerSync


from time import sleep
# from flask_migrate import upgrade
# from authserver import create_app
# from authserver.utilities import PostgreSQLContainer
# from authserver.config import ConfigurationFactory

class PostgreSQLContainer(object):
    """A PostgreSQL Container Object.

    This class provides a mechanism for managing PostgreSQL Docker containers
    so that it can be injected into unit tests.

    Class Attributes:
        config (object): A Configuration Factory object.
        container (object): The Docker container object.
        docker_client (object): Docker client.
        db_environment (list): Database environment configuration variables.
        db_ports (dict): Dictionary of database port mappings.

    """

    def __init__(self):
        self.config = ConfigurationFactory.get_config('TEST')
        self.container = None
        self.docker_client = docker.from_env()
        self.db_environment = [
            'POSTGRES_USER={}'.format(self.config.POSTGRES_USER),
            'POSTGRES_PASSWORD={}'.format(self.config.POSTGRES_PASSWORD),
            'POSTGRES_DB={}'.format(self.config.POSTGRES_DATABASE)
        ]
        self.db_ports = {'5432/tcp': self.config.POSTGRES_PORT}

    def get_postgresql_image(self):
        """Output the PostgreSQL image from the configuation.

        Returns:
            str: The PostgreSQL image name and version tag.
        """
        return '{}:{}'.format(self.config.IMAGE_NAME, self.config.IMAGE_VERSION)

    def start_container(self):
        """Start PostgreSQL Container."""
        try:
            self.docker_client.images.pull(self.get_postgresql_image())
        except Exception as e:
            print('Exception {}'.format(e))

        self.container = self.docker_client.containers.run(
            self.get_postgresql_image(),
            detach=True,
            auto_remove=True,
            name=self.config.CONTAINER_NAME,
            environment=self.db_environment,
            ports=self.db_ports)

    def stop_container(self):
        """Stop PostgreSQL Container."""
        if self.container is None:
            self.container = self.docker_client.containers.get(
                self.config.CONTAINER_NAME)

        if self.container is not None:
            self.container.stop()


@pytest.fixture(scope='session')
def client():
    # From authserver
    """Setup the Flask application and return an instance of its test client.

    Returns:
        client (object): The Flask test client for the application.

    """
    drm = DataResourceManager()
    app = drm.create_app()

    # From authserver
    # client = app.test_client()
    # return client

    return app

@pytest.fixture(scope='session', autouse=True)
def app():
    """Setup the PostgreSQL database instance and return the Flask application.

    Returns:
        app (object): The Flask application.

    """
    # drm = DataResourceManager()
    app = drm.create_app()
    postgres = PostgreSQLContainer()
    postgres.start_container()

    data_model_manager = DataModelManagerSync()

    upgraded = False
    while not upgraded:
        try:
            with app.app_context():
                data_model_manager.run_upgrade()
                upgraded = True
        except Exception as e:
            print("Not upgraded, sleeping...")
            sleep(1)


@pytest.fixture
def environments():
    return [
        'DEVELOPMENT',
        'TESTING',
        'STAGING',
        'SANDBOX',
        'PRODUCTION'
    ]
