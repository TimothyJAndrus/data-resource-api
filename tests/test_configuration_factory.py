"""Configuration Factory Unit Test.

"""

from expects import expect, be_an, raise_error, have_property
from data_resource_api import ConfigurationFactory, InvalidConfigurationError


class TestConfigurationFactory(object):
    """Application Configuration Unit Tests."""

    def test_load_configuration(self):
        """Load a configuration from the configuration factory.

        Ensure that a configuration object can be pulled from the environment.

        """

        configuration = ConfigurationFactory.from_env()
        expect(configuration).to(be_an(object))
        expect(configuration).to(have_property('POSTGRES_PORT'))
        expect(configuration).to(have_property('POSTGRES_HOSTNAME'))

    def test_manually_request_configuration(self):
        """Manually specify a configuration.

        Ensure that bad or unknown configurations will throw an
        InvalidConfigurationError.

        """

        # bad configuration
        expect(lambda: ConfigurationFactory.get_config(
            config_type='UNDEFINED')).to(raise_error(InvalidConfigurationError))

        # good configuration
        configuration = ConfigurationFactory.get_config(
            config_type='TEST')
        expect(configuration).to(be_an(object))
        expect(configuration).to(have_property('POSTGRES_PORT'))
        expect(configuration).to(have_property('POSTGRES_HOSTNAME'))
