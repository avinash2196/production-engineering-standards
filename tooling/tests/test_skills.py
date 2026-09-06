from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".github/skills"

class SkillTest(unittest.TestCase):
    def test_every_skill_has_valid_skill_md(self):
        self.assertTrue(SKILLS.is_dir())
        for directory in [p for p in SKILLS.iterdir() if p.is_dir()]:
            with self.subTest(skill=directory.name):
                skill = directory / "SKILL.md"
                self.assertTrue(skill.is_file())
                text = skill.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                self.assertRegex(text, rf"(?m)^name:\s*{re.escape(directory.name)}\s*$")
                self.assertRegex(text, r"(?m)^description:\s*.+$")

    def test_oracle_postgres_is_a_skill(self):
        self.assertTrue((SKILLS / "oracle-to-postgres-modernization/SKILL.md").is_file())
        self.assertFalse((ROOT / ".github/agents/oracle-to-postgres-modernization.agent.md").exists())

    def test_oracle_postgres_has_required_references(self):
        base = SKILLS / "oracle-to-postgres-modernization/references"
        for name in [
            "assessment.md",
            "schema-and-sql-mapping.md",
            "spring-boot-migration.md",
            "verification-and-cutover.md",
        ]:
            self.assertTrue((base / name).is_file(), name)

if __name__ == "__main__":
    unittest.main()
