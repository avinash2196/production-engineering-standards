import unittest

from app.config.settings import get_settings
from app.main import create_app


class AppSmokeTest(unittest.TestCase):
    def tearDown(self) -> None:
        get_settings.cache_clear()

    def test_reference_app_can_be_created_with_checked_in_defaults(self) -> None:
        app = create_app()

        self.assertEqual("service-name local-adapter reference", app.title)
        self.assertEqual("/docs", app.docs_url)


if __name__ == "__main__":
    unittest.main()
