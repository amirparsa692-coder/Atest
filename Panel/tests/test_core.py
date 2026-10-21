import asyncio
import os
import tempfile
import unittest
from urllib.parse import urlparse


class CoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = tempfile.TemporaryDirectory()
        os.environ.setdefault("ADMIN_PASSWORD", "test-password-not-for-production")
        os.environ["DATA_DIR"] = cls.data_dir.name
        os.environ["SECURE_COOKIES"] = "true"
        import panel.main as main
        cls.main = main

    @classmethod
    def tearDownClass(cls):
        cls.data_dir.cleanup()

    def test_password_hash_round_trip(self):
        hashed = self.main.hash_password("correct horse battery staple")
        self.assertTrue(self.main.verify_password("correct horse battery staple", hashed))
        self.assertFalse(self.main.verify_password("wrong", hashed))

    def test_config_uri_has_expected_uuid_and_scheme(self):
        uid = self.main.generate_uuid()
        uri = self.main.generate_config_link(uid, "example.test", protocol="vless-ws")
        parsed = urlparse(uri)
        self.assertEqual(parsed.scheme, "vless")
        self.assertTrue(uri.startswith(f"vless://{uid}@"))
        self.assertIn("path=/ws/", uri)

    def test_input_normalization(self):
        self.assertEqual(self.main.parse_size_to_bytes(1, "GB"), 1024 ** 3)
        self.assertEqual(self.main.parse_speed_to_bytes(8, "Mbps"), 1024 ** 2)
        self.assertEqual(self.main.normalize_port("443"), 443)
        self.assertEqual(self.main.normalize_port("99999"), 443)

    def test_health_contract(self):
        payload = asyncio.run(self.main.health())
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["app"], self.main.APP_NAME)
        self.assertIn("version", payload)


if __name__ == "__main__":
    unittest.main()
