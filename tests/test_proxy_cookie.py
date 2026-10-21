import os
import tempfile
import unittest

from starlette.requests import Request


class ProxyCookieTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = tempfile.TemporaryDirectory()
        os.environ.setdefault("ADMIN_PASSWORD", "test-password-not-for-production")
        os.environ["DATA_DIR"] = cls.data_dir.name
        os.environ["SECURE_COOKIES"] = "true"
        import panel.main as main
        cls.main = main
        cls.main.TRUST_PROXY_HEADERS = True

    @classmethod
    def tearDownClass(cls):
        cls.data_dir.cleanup()

    def test_forwarded_https_is_detected(self):
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/",
            "raw_path": b"/",
            "query_string": b"",
            "headers": [(b"x-forwarded-proto", b"https")],
            "server": ("internal", 8000),
            "client": ("10.0.0.2", 1234),
            "scheme": "http",
        }
        request = Request(scope)
        self.assertTrue(self.main.request_is_secure(request))


if __name__ == "__main__":
    unittest.main()
