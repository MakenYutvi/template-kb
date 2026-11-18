"""Git-ignore regression checks on disposable repositories; no network needed."""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("git"), "Requires Git")
class GitIgnoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="kb-ignore-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "--quiet")
        # Isolate from the user's global excludes; keep fixture policy explicit.
        (self.root / "empty-excludes").write_text("", encoding="utf-8")
        self.git("config", "core.excludesFile", str(self.root / "empty-excludes"))

    def git(self, *args: str, expected: int = 0) -> subprocess.CompletedProcess:
        result = subprocess.run(
            ["git", *args], cwd=self.root, capture_output=True, timeout=15,
        )
        self.assertEqual(result.returncode, expected, result.stderr)
        return result

    def file(self, name: str, text: str = "synthetic fixture\n") -> Path:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def assert_ignored(self, name: str, ignored: bool) -> None:
        self.git("check-ignore", "-q", "--no-index", "--", name, expected=0 if ignored else 1)

    def test_template_keeps_reports_visible_and_local_data_ignored(self) -> None:
        shutil.copyfile(ROOT / ".gitignore", self.root / ".gitignore")
        for name, ignored in (
            ("wiki/outputs/index.md", False), ("wiki/outputs/report.md", False),
            ("outputs/local.md", True), ("project/outputs/report.md", False),
            (".env", True), (".env.example", False), ("private.key", True),
            (".kb-runtime/state.json", True), (".codex_runtime/probe.txt", True),
            (".ai/automation-preferences.local.json", True),
        ):
            with self.subTest(path=name):
                self.file(name)
                self.assert_ignored(name, ignored)

    def test_verbose_negation_is_not_an_ignored_result(self) -> None:
        self.file(".gitignore", "outputs/\n!/wiki/outputs/\n/wiki/outputs/private.md\n!/wiki/outputs/index.md\n")
        for name, ignored in (
            ("wiki/outputs/index.md", False), ("wiki/outputs/private.md", True),
            ("unmatched.md", False), ("outputs/local.md", True),
        ):
            self.file(name)
            self.assert_ignored(name, ignored)
        diagnostic = self.git("check-ignore", "-v", "--no-index", "--", "wiki/outputs/index.md")
        self.assertIn(b"!/wiki/outputs/index.md", diagnostic.stdout)
        self.git("add", "--", "wiki/outputs/index.md")
        # --no-index still tests rules even after the file is tracked.
        self.assert_ignored("wiki/outputs/index.md", False)
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout.strip(), b"wiki/outputs/index.md")

    def test_upgrade_exception_preserves_private_rules_and_file_bytes(self) -> None:
        original = "outputs/\n.env\n/wiki/outputs/private.md\n"
        rules = self.file(".gitignore", original)
        names = ("wiki/outputs/index.md", "wiki/outputs/private.md", "outputs/local.md", "project/outputs/local.md", ".env")
        before = {name: self.file(name).read_bytes() for name in names}
        self.assert_ignored("wiki/outputs/index.md", True)
        # The documented narrow directory exception leaves precise file rules in force.
        rules.write_text(original + "!/wiki/outputs/\n", encoding="utf-8")
        for name in names:
            self.assertEqual((self.root / name).read_bytes(), before[name])
            self.assert_ignored(name, name != "wiki/outputs/index.md")
        self.assertTrue(rules.read_text(encoding="utf-8").startswith(original))
        self.assertEqual(self.git("diff", "--cached", "--name-only").stdout, b"")


if __name__ == "__main__":
    unittest.main()
