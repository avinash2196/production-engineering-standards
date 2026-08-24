from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "stacks/python-fastapi/reference-implementations/local-adapters"


class LocalAdapterReferenceSemanticsTest(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REFERENCE / relative).read_text(encoding="utf-8")

    def test_reference_declares_its_runtime_dependencies(self) -> None:
        pyproject = self.read("pyproject.toml").lower()
        self.assertIn('fastapi =', pyproject)
        self.assertIn('uvicorn =', pyproject)
        self.assertIn('packages = [{ include = "app" }]', pyproject)
        self.assertNotIn('your-team <team@myorg.com>', pyproject)

    def test_reference_main_does_not_import_nonexistent_api_router(self) -> None:
        main = self.read("app/main.py")
        self.assertNotIn("app.api.router", main)
        self.assertIn("app = create_app()", main)

    def test_reference_defaults_are_local_and_start_without_managed_adapters(self) -> None:
        settings = self.read("app/config/settings.py")
        self.assertIn("MessagingAdapter.IN_MEMORY", settings)
        self.assertIn("CacheAdapter.IN_MEMORY", settings)
        self.assertIn("StorageAdapter.LOCAL", settings)
        self.assertIn("SecretAdapter.ENV", settings)
        readme = self.read("README.md")
        self.assertIn("zero-infrastructure local adapters", readme)
        self.assertIn("uvicorn app.main:app --reload", readme)


if __name__ == "__main__":
    unittest.main()
