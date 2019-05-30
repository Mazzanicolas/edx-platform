"""
Unit tests for the IdentityServer3 OAuth2 Backend
"""

from third_party_auth.identityserver3 import IdentityServer3
from third_party_auth.tests import testutil
from third_party_auth.tests.factories import OAuth2ProviderConfigFactory


class IdentityServer3Test(testutil.TestCase):
    """
    Unit tests for the IdentityServer3 OAuth2 Backend
    """

    def setUp(self):
        super(IdentityServer3Test, self).setUp()
        self.id3_instance = IdentityServer3()

    def test_proper_get_of_user_id(self):
        """
        make sure the "sub" claim works properly to grab user Id
        """
        response = {"sub": 1, "email": "example@example.com"}
        self.assertEqual(self.id3_instance.get_user_id({}, response), 1)

    def test_key_error_thrown_with_no_sub(self):
        """
        test that a KeyError is thrown if the "sub" claim does not exist
        """
        response = {"id": 1}
        self.assertRaises(KeyError, self.id3_instance.get_user_id({}, response))

    def test_proper_config_access(self):
        """
        test that the IdentityServer3 model properly grabs OAuth2Configs
        """
        provider_config = OAuth2ProviderConfigFactory.create(backend_name="identityServer3")
        self.assertEqual(self.id3_instance.get_config(), provider_config)

    def test_config_after_updating(self):
        """
        Make sure when the OAuth2Config for this backend is updated, the new config is properly grabbed
        """
        original_provider_config = OAuth2ProviderConfigFactory.create(slug="original", backend_name="identityServer3")
        updated_provider_config = OAuth2ProviderConfigFactory.create(slug="updated", backend_name="identityServer3")
        self.assertEqual(self.id3_instance.get_config(), updated_provider_config)
        self.assertNotEqual(self.id3_instance.get_config(), original_provider_config)
