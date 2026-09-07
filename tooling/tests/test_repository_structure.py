from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class RepositoryStructureTest(unittest.TestCase):
    def test_copilot_native_directories_exist(self):
        for rel in [
            ".github/agents",
            ".github/skills",
            ".github/prompts",
            ".github/instructions",
            ".github/workflows",
        ]:
            self.assertTrue((ROOT / rel).is_dir(), rel)

    def test_legacy_root_taxonomies_are_absent(self):
        for rel in [
            "standards",
            "playbooks",
            "stacks",
            "contracts",
            "templates",
            "agents",
        ]:
            self.assertFalse((ROOT / rel).exists(), rel)

    def test_required_root_support_directories_exist(self):
        for rel in ["tooling", "docs"]:
            self.assertTrue((ROOT / rel).is_dir(), rel)

    def test_root_examples_are_optional(self):
        examples = ROOT / "examples"
        if examples.exists():
            self.assertTrue(examples.is_dir(), "examples")


if __name__ == "__main__":
    unittest.main()
