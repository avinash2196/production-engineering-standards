import os
import unittest
from unittest.mock import patch

from app.config.settings import Settings, get_settings
from app.main import create_app


class SettingsTest(unittest.TestCase):
    def tearDown(self) -> None:
        get_settings.cache_clear()

    def test_defaults_are_minimal_and_local(self) -> None:
        settings = Settings()
        self.assertEqual("service-name", settings.service_name)
        self.assertEqual("local", settings.environment)

    def test_environment_can_be_selected_explicitly(self) -> None:
        with patch.dict(os.environ, {"ENVIRONMENT": "production"}, clear=False):
            settings = Settings()
        self.assertEqual("production", settings.environment)


class AppFactoryTest(unittest.TestCase):
    def tearDown(self) -> None:
        get_settings.cache_clear()

    def test_create_app_uses_typed_service_name(self) -> None:
        with patch.dict(os.environ, {"SERVICE_NAME": "document-service"}, clear=False):
            get_settings.cache_clear()
            app = create_app()
        self.assertEqual("document-service", app.title)

    def test_production_disables_interactive_docs(self) -> None:
        with patch.dict(os.environ, {"ENVIRONMENT": "production"}, clear=False):
            get_settings.cache_clear()
            app = create_app()
        self.assertIsNone(app.docs_url)


if __name__ == "__main__":
    unittest.main()
