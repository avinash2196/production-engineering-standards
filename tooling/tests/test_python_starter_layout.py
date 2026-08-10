import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STARTER = ROOT / "stacks/python-fastapi/project-template"
REFERENCE = ROOT / "stacks/python-fastapi/reference-implementations/local-adapters"


class PythonStarterLayoutTest(unittest.TestCase):
    def test_canonical_starter_contains_only_foundation_packages(self) -> None:
        app = STARTER / "app"
        forbidden = ("api", "domain", "infrastructure", "repository", "service")
        for package in forbidden:
            self.assertFalse(
                (app / package).exists(),
                f"Canonical Python starter must not contain capability package: {package}",
            )

    def test_canonical_starter_has_only_minimal_tests(self) -> None:
        tests = STARTER / "tests"
        python_tests = {path.name for path in tests.glob("test_*.py")}
        self.assertEqual({"test_app.py"}, python_tests)

    def test_local_adapter_reference_contains_real_implementation(self) -> None:
        self.assertTrue(
            (REFERENCE / "app/infrastructure/local/providers.py").is_file(),
            "Move local-adapter implementation into the reference directory.",
        )
        self.assertTrue(
            (REFERENCE / "tests/test_provider_selection.py").is_file(),
            "Move local-adapter tests into the reference directory.",
        )
        self.assertTrue((REFERENCE / "app/config/settings.py").is_file())
        self.assertTrue((REFERENCE / "pyproject.toml").is_file())


if __name__ == "__main__":
    unittest.main()
