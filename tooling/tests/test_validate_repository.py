"""Tests for the dependency-free repository standards validator."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "validate_repository.py"
)
spec = importlib.util.spec_from_file_location("validate_repository", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load validator module from {MODULE_PATH}")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class RepositoryValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, relative_path: str, content: str = "") -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_required_paths_reports_only_missing_paths(self) -> None:
        self.write("standards/architecture.md", "# Architecture\n")
        errors = validator.validate_required_paths(
            self.root,
            required_paths=("standards", "contracts", "README.md"),
        )

        self.assertEqual(
            [
                "Missing required path: README.md",
                "Missing required path: contracts",
            ],
            errors,
        )

    def test_markdown_links_accept_existing_relative_targets(self) -> None:
        self.write("docs/target.md", "# Target\n")
        self.write("README.md", "See [target](docs/target.md).\n")

        errors = validator.validate_markdown_links(self.root)

        self.assertEqual([], errors)

    def test_markdown_links_report_broken_active_document_links(self) -> None:
        self.write("README.md", "See [missing](docs/missing.md).\n")

        errors = validator.validate_markdown_links(self.root)

        self.assertEqual(
            ["README.md:1: broken link 'docs/missing.md'"],
            errors,
        )

    def test_markdown_links_skip_template_placeholders(self) -> None:
        self.write(
            "templates/docs/project-template.md",
            "See [future generated file](docs/generated.md).\n",
        )

        errors = validator.validate_markdown_links(self.root)

        self.assertEqual([], errors)

    def test_placeholder_scan_does_not_flag_validator_pattern_declarations(self) -> None:
        placeholder = "Add validation " + "steps"
        self.write(
            "tooling/scripts/validate_repository.py",
            f'PLACEHOLDER_PATTERNS = ("{placeholder}",)\n',
        )
        self.write("README.md", "Complete documentation.\n")

        errors = validator.validate_no_placeholders(self.root)

        self.assertEqual([], errors)

    def test_placeholder_scan_reports_placeholder_in_active_file(self) -> None:
        placeholder = "Add validation " + "steps"
        self.write("README.md", placeholder + "\n")

        errors = validator.validate_no_placeholders(self.root)

        self.assertEqual(
            [f"README.md contains placeholder: '{placeholder}'"],
            errors,
        )

    def test_prompt_validation_rejects_deprecated_mode_and_duplicate_body_metadata(self) -> None:
        self.write(
            ".github/prompts/example.prompt.md",
            """---
mode: agent
description: Example
agent: agent
---
mode: agent

Do work.
""",
        )

        errors = validator.validate_prompt_files(self.root)

        self.assertEqual(
            [
                ".github/prompts/example.prompt.md: deprecated frontmatter field 'mode'",
                ".github/prompts/example.prompt.md: duplicate body metadata 'mode: agent'",
            ],
            errors,
        )

    def test_prompt_validation_accepts_supported_multiline_frontmatter(self) -> None:
        self.write(
            ".github/prompts/example.prompt.md",
            """---
description: Example
agent: agent
tools:
  - codebase
  - readFile
---
Do work.
""",
        )

        errors = validator.validate_prompt_files(self.root)

        self.assertEqual([], errors)

    def test_prompt_validation_accepts_supported_inline_tools_list(self) -> None:
        self.write(
            ".github/prompts/example.prompt.md",
            """---
description: Example
agent: agent
tools: ['search/codebase', 'vscode/askQuestions']
---
Do work.
""",
        )

        errors = validator.validate_prompt_files(self.root)

        self.assertEqual([], errors)

    def test_prompt_validation_rejects_malformed_list_marker(self) -> None:
        self.write(
            ".github/prompts/example.prompt.md",
            """---
description: Example
agent: agent
tools:
  * codebase
---
Do work.
""",
        )

        errors = validator.validate_prompt_files(self.root)

        self.assertEqual(
            [
                ".github/prompts/example.prompt.md:5: invalid list item; use '- value'"
            ],
            errors,
        )

    def test_prompt_validation_rejects_scalar_tools_value(self) -> None:
        self.write(
            ".github/prompts/example.prompt.md",
            """---
description: Example
tools: codebase
---
Do work.
""",
        )

        errors = validator.validate_prompt_files(self.root)

        self.assertEqual(
            [
                ".github/prompts/example.prompt.md: frontmatter field 'tools' must be a YAML list"
            ],
            errors,
        )

    def test_prompt_validation_rejects_duplicate_frontmatter_key(self) -> None:
        self.write(
            ".github/prompts/example.prompt.md",
            """---
description: Example
description: Duplicate
---
Do work.
""",
        )

        errors = validator.validate_prompt_files(self.root)

        self.assertEqual(
            [
                ".github/prompts/example.prompt.md:3: duplicate frontmatter field 'description'"
            ],
            errors,
        )

    def test_prompt_validation_rejects_unexpected_indentation(self) -> None:
        self.write(
            ".github/prompts/example.prompt.md",
            """---
description: Example
  agent: agent
---
Do work.
""",
        )

        errors = validator.validate_prompt_files(self.root)

        self.assertEqual(
            [
                ".github/prompts/example.prompt.md:3: unexpected indentation in prompt frontmatter"
            ],
            errors,
        )

    def test_prohibited_reference_scan_reports_stale_active_document_terms(self) -> None:
        stale_prefix = "FALL" + "BACK_"
        self.write(
            "README.md",
            "Run tooling/scripts/generate-template.py and set "
            + stale_prefix
            + "KAFKA=db.\n",
        )

        errors = validator.validate_prohibited_references(self.root)

        self.assertEqual(
            [
                f"README.md contains stale reference '{stale_prefix}'",
                "README.md contains stale reference 'generate-template.py'",
            ],
            errors,
        )



    def test_skill_validation_accepts_valid_skill(self) -> None:
        self.write(
            ".github/skills/requirements-analysis/SKILL.md",
            """---
name: requirements-analysis
description: Review requirements before planning.
---
# Requirements Analysis
""",
        )

        errors = validator.validate_skill_files(self.root)

        self.assertEqual([], errors)

    def test_skill_validation_requires_skill_md_for_each_skill_directory(self) -> None:
        (self.root / ".github/skills/code-review").mkdir(parents=True)

        errors = validator.validate_skill_files(self.root)

        self.assertEqual(
            [".github/skills/code-review: missing SKILL.md"],
            errors,
        )

    def test_skill_validation_requires_name_and_description(self) -> None:
        self.write(
            ".github/skills/code-review/SKILL.md",
            """---
name: code-review
---
# Code Review
""",
        )

        errors = validator.validate_skill_files(self.root)

        self.assertEqual(
            [".github/skills/code-review/SKILL.md: missing frontmatter field 'description'"],
            errors,
        )

    def test_skill_validation_requires_name_to_match_directory(self) -> None:
        self.write(
            ".github/skills/code-review/SKILL.md",
            """---
name: pull-request-review
description: Review code.
---
# Code Review
""",
        )

        errors = validator.validate_skill_files(self.root)

        self.assertEqual(
            [
                ".github/skills/code-review/SKILL.md: skill name 'pull-request-review' must match directory 'code-review'"
            ],
            errors,
        )

    def test_skill_validation_rejects_invalid_skill_name_format(self) -> None:
        self.write(
            ".github/skills/Code_Review/SKILL.md",
            """---
name: Code_Review
description: Review code.
---
# Code Review
""",
        )

        errors = validator.validate_skill_files(self.root)

        self.assertEqual(
            [
                ".github/skills/Code_Review/SKILL.md: skill name 'Code_Review' must use lowercase letters, numbers, and hyphens"
            ],
            errors,
        )

    def test_skill_validation_rejects_malformed_frontmatter(self) -> None:
        self.write(
            ".github/skills/code-review/SKILL.md",
            """---
name: code-review
description: Review code.
allowed-tools:
  * shell
---
# Code Review
""",
        )

        errors = validator.validate_skill_files(self.root)

        self.assertEqual(
            [
                ".github/skills/code-review/SKILL.md:5: invalid list item; use '- value'"
            ],
            errors,
        )

if __name__ == "__main__":
    unittest.main()
