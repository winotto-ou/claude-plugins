"""Tests for scripts/check.py. Run: python3 scripts/test_check.py (or pytest scripts -q)."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHECK = REPO / "scripts" / "check.py"

GOOD_SKILL = "---\nname: demo\ndescription: A demo skill.\n---\n\nBody text.\n"


def run_check(root):
    p = subprocess.run([sys.executable, str(CHECK)], cwd=root, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "repo"
        shutil.copytree(
            REPO, self.root,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", "dist"),
        )
        self.plugin = self.root / "plugins" / "winotto"
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def add_skill(self, text=GOOD_SKILL, name="demo"):
        d = self.plugin / "skills" / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(text, encoding="utf-8")
        return d / "SKILL.md"

    def expect_error(self, fragment):
        code, out = run_check(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn(fragment, out)

    def edit_json(self, path, fn):
        data = json.loads(path.read_text(encoding="utf-8"))
        fn(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_real_repo_ok(self):
        p = subprocess.run([sys.executable, str(CHECK)], cwd=REPO, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(p.stdout.strip(), "OK")

    def test_good_skill_ok(self):
        self.add_skill()
        code, out = run_check(self.root)
        self.assertEqual(code, 0, out)

    # Rule 1
    def test_rule1_broken_json(self):
        (self.root / ".claude-plugin" / "marketplace.json").write_text("{nope", encoding="utf-8")
        self.expect_error("marketplace.json")

    def test_rule1_marketplace_name(self):
        self.edit_json(self.root / ".claude-plugin" / "marketplace.json", lambda d: d.update(name="other"))
        self.expect_error("winotto-ou")

    def test_rule1_source_dotdot(self):
        self.edit_json(self.root / ".claude-plugin" / "marketplace.json",
                       lambda d: d["plugins"][0].update(source="./plugins/../plugins/winotto"))
        self.expect_error("..")

    def test_rule1_source_no_prefix(self):
        self.edit_json(self.root / ".claude-plugin" / "marketplace.json",
                       lambda d: d["plugins"][0].update(source="plugins/winotto"))
        self.expect_error("./")

    def test_rule1_missing_plugin_json(self):
        (self.plugin / ".claude-plugin" / "plugin.json").unlink()
        self.expect_error("plugin.json")

    # Rule 2
    def test_rule2_extra_key(self):
        self.edit_json(self.plugin / ".mcp.json",
                       lambda d: d["mcpServers"]["jw"].update(headers={"X": "y"}))
        self.expect_error("jw")

    def test_rule2_bad_url(self):
        self.edit_json(self.plugin / ".mcp.json",
                       lambda d: d["mcpServers"]["jw"].update(url="https://example.com/jw/mcp"))
        self.expect_error("url")

    def test_rule2_bad_type(self):
        self.edit_json(self.plugin / ".mcp.json",
                       lambda d: d["mcpServers"]["jw"].update(type="sse"))
        self.expect_error("type")

    def test_rule2_missing_mcp_json(self):
        (self.plugin / ".mcp.json").unlink()
        self.expect_error(".mcp.json")

    # Rule 3
    def test_rule3_no_frontmatter(self):
        self.add_skill("no frontmatter\n")
        self.expect_error("frontmatter")

    def test_rule3_name_mismatch(self):
        self.add_skill("---\nname: other\ndescription: x\n---\n")
        self.expect_error("name")

    def test_rule3_empty_description(self):
        self.add_skill("---\nname: demo\ndescription:\n---\n")
        self.expect_error("description")

    def test_rule3_long_description(self):
        self.add_skill("---\nname: demo\ndescription: " + "a" * 1025 + "\n---\n")
        self.expect_error("1024")

    def test_rule3_forbidden_key(self):
        self.add_skill("---\nname: demo\ndescription: x\nuser-invocable: true\n---\n")
        self.expect_error("user-invocable")

    # Rule 4
    def test_rule4_mcp_prefix(self):
        self.add_skill(GOOD_SKILL + "Use mcp" + "__jw__search.\n")
        self.expect_error("mcp" + "__")

    def test_rule4_plugin_root(self):
        self.add_skill(GOOD_SKILL + "Run $" + "{CLAUDE_PLUGIN_ROOT}/x.\n")
        self.expect_error("CLAUDE_PLUGIN_ROOT")

    # Rule 5
    def test_rule5_bin_dir(self):
        (self.plugin / "bin").mkdir()
        self.expect_error("bin")

    # Rule 6
    def test_rule6_forbidden_strings(self):
        for bad in ["/ho" + "me/x", "/mnt" + "/c/x", "a@gmail" + ".com"]:
            with self.subTest(bad=bad):
                f = self.root / "leak.txt"
                f.write_text(bad, encoding="utf-8")
                self.expect_error("leak.txt")
                f.unlink()

    def test_rule6_leak_in_check_script_itself(self):
        with open(self.root / "scripts" / "check.py", "a", encoding="utf-8") as f:
            f.write("\n# /ho" + "me/someone\n")
        self.expect_error("check.py")

    def test_rule6_secret(self):
        (self.root / "leak.txt").write_text("api_" + "key = abcdefgh12345", encoding="utf-8")
        self.expect_error("leak.txt")


if __name__ == "__main__":
    unittest.main()
