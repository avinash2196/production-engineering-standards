import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class ProductionFoundationSemanticsTest(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_python_starter_does_not_preload_enterprise_capabilities(self) -> None:
        pyproject = self.read("stacks/python-fastapi/project-template/pyproject.toml").lower()
        forbidden = (
            "sqlalchemy",
            "asyncpg",
            "aiokafka",
            "redis",
            "boto",
            "google-cloud-storage",
            "opentelemetry",
            "prometheus",
            "testcontainers",
        )
        for dependency in forbidden:
            self.assertNotIn(dependency, pyproject)

    def test_python_local_adapters_are_documented_as_reference_not_default(self) -> None:
        stack_readme = self.read("stacks/python-fastapi/README.md")
        self.assertIn("reference-implementations/local-adapters", stack_readme)
        self.assertIn("does **not** preload", stack_readme)

    def test_observability_separates_required_outcome_from_mechanism(self) -> None:
        standard = self.read("standards/observability.md")
        self.assertIn("Observability is a production requirement", standard)
        self.assertIn("OpenTelemetry", standard)
        self.assertIn("not an automatically installed dependency", standard)
        self.assertIn("Do not invent SLOs", standard)

    def test_configuration_does_not_require_config_provider_or_dynamic_config(self) -> None:
        standard = self.read("standards/configuration-management.md")
        self.assertIn("does **not** require a `ConfigProvider` interface in every service", standard)
        self.assertIn("Dynamic/runtime configuration is optional", standard)
        self.assertIn("There is no universal required precedence ordering", standard)

    def test_security_requires_invariants_without_preselecting_mechanisms(self) -> None:
        standard = self.read("standards/security/security-standards.md")
        self.assertIn("Security is mandatory", standard)
        self.assertIn("A specific security mechanism is not automatically mandatory", standard)
        self.assertIn("Do not infer RBAC/ABAC or PHI-specific authorization", standard)
        self.assertIn("Healthcare terminology does not by itself establish HIPAA applicability", standard)

    def test_production_readiness_uses_applicability_status_model(self) -> None:
        standard = self.read("standards/production-readiness.md")
        for status in ("PASS", "FAIL", "NOT APPLICABLE", "NEEDS VERIFICATION"):
            self.assertIn(status, standard)
        self.assertIn("Do not universally require OpenTelemetry", standard)
        self.assertIn("Production readiness does not bypass PDD gates", standard)


if __name__ == "__main__":
    unittest.main()
