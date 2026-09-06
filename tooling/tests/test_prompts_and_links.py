from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]

class PromptAndLinkTest(unittest.TestCase):
    def test_prompt_custom_agent_bindings_exist(self):
        agents = {
            p.name.removesuffix(".agent.md").removesuffix(".md")
            for p in (ROOT / ".github/agents").glob("*.md")
        }
        built_in = {"ask", "agent", "plan", "edit"}
        for prompt in (ROOT / ".github/prompts").glob("*.prompt.md"):
            text = prompt.read_text(encoding="utf-8")
            front = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
            self.assertIsNotNone(front, prompt.name)
            match = re.search(r'^agent:\s*"?([^"\n]+)"?$', front.group(1), re.MULTILINE)
            if match:
                name = match.group(1).strip()
                self.assertTrue(name in built_in or name in agents, (prompt.name, name))

    def test_relative_markdown_links_resolve(self):
        link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for path in ROOT.rglob("*.md"):
            for target in link_re.findall(path.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                rel = target.split("#", 1)[0]
                if rel:
                    self.assertTrue((path.parent / rel).resolve().exists(), (path, target))

if __name__ == "__main__":
    unittest.main()
