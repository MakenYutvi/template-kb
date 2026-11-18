r"""Windows CLI regression checks; stdlib only, no accounts or network needed.

Run from the repository root:
    scripts\kb_python.cmd -m unittest discover -s tests
On other operating systems these Windows-specific checks are explicitly skipped.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = "Проверка ё № — путь с пробелом"


@unittest.skipUnless(os.name == "nt", "Requires Windows PowerShell and cmd.exe")
class WindowsLauncherTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="kb-cli-")
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name) / "База с пробелом ё"
        self.folder.mkdir()
        self.env = os.environ.copy()
        self.env.pop("PYTHONIOENCODING", None)
        self.env.pop("PYTHONUTF8", None)
        self.env["KB_PYTHON"] = sys.executable
        self.probe = self.folder / "probe.py"

    def run_command(self, args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess:
        return subprocess.run(
            args, cwd=cwd, env=self.env, stdin=subprocess.DEVNULL,
            capture_output=True, timeout=30,
        )

    def test_redirected_stdout_stderr_arguments_and_exit_code(self) -> None:
        self.probe.write_text(
            "import sys\nprint(sys.argv[1])\nprint(sys.argv[1], file=sys.stderr)\nsys.exit(7)\n",
            encoding="utf-8",
        )
        result = self.run_command([
            "cmd.exe", "/d", "/c", "scripts\\kb_python.cmd",
            str(self.probe), SAMPLE,
        ])
        self.assertEqual(result.returncode, 7)
        self.assertEqual(result.stdout.decode("utf-8").strip(), SAMPLE)
        self.assertEqual(result.stderr.decode("utf-8").strip(), SAMPLE)

    def capture_in_powershell(self, code_page: int, options: tuple[str, ...] = (), direct: bool = False) -> dict:
        # A BOM lets Windows PowerShell 5.1 read non-ASCII checkout paths too.
        wrapper = str(sys.executable if direct else ROOT / "scripts/kb_python.ps1").replace("'", "''")
        flags = " ".join("'" + flag.replace("'", "''") + "'" for flag in options)
        script = Path(self.temp.name) / "capture.ps1"
        script.write_text(
            "param([string] $Probe)\n"
            "$ErrorActionPreference = 'Stop'\n"
            f"[Console]::OutputEncoding = [Text.Encoding]::GetEncoding({code_page})\n"
            f"$Captured = & '{wrapper}' {flags} $Probe\n"
            "$Code = $LASTEXITCODE\n"
            "$Restored = [Console]::OutputEncoding.CodePage\n"
            "[Console]::OutputEncoding = New-Object Text.UTF8Encoding($false)\n"
            "@{text=$Captured; code=$Code; restored=$Restored; "
            "ioencoding=$env:PYTHONIOENCODING} | ConvertTo-Json -Compress\n",
            encoding="utf-8-sig",
        )
        result = self.run_command([
            "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), str(self.probe),
        ])
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout.decode("utf-8-sig"))

    def test_powershell_pipeline_and_console_encoding_restored(self) -> None:
        self.probe.write_text(f"print({ascii(SAMPLE)})\nraise SystemExit(7)\n", encoding="ascii")
        self.assertEqual(self.capture_in_powershell(866), {
            "text": SAMPLE, "code": 7, "restored": 866, "ioencoding": None,
        })

    def test_inherited_ioencoding_and_matching_console(self) -> None:
        for setting, code_page, codec, sample in (
            ("cp1251", 1251, "cp1251", SAMPLE),
            ("cp866", 866, "cp866", "Проверка ё"),
            ("utf-8", 65001, "utf-8", SAMPLE),
            ("cp1251:replace", 1251, "cp1251", SAMPLE + " 🙂"),
        ):
            with self.subTest(ioencoding=setting):
                self.env["PYTHONIOENCODING"] = setting
                expected = sample.encode(codec, errors="replace").decode(codec)
                self.probe.write_text(
                    f"print({ascii(sample)})\nraise SystemExit(7)\n", encoding="ascii",
                )
                self.assertEqual(self.capture_in_powershell(code_page), {
                    "text": expected, "code": 7, "restored": code_page, "ioencoding": setting,
                })
                self.probe.write_text(
                    "import sys\nprint(sys.argv[1])\nprint(sys.argv[1], file=sys.stderr)\nsys.exit(7)\n",
                    encoding="ascii",
                )
                result = self.run_command([
                    "cmd.exe", "/d", "/c", "scripts\\kb_python.cmd", str(self.probe), sample,
                ])
                self.assertEqual(result.returncode, 7, result.stderr)
                self.assertEqual(result.stdout.decode(codec).strip(), expected)
                # Python always uses backslashreplace for stderr.
                stderr_expected = sample.encode(codec, errors="backslashreplace").decode(codec)
                self.assertEqual(result.stderr.decode(codec).strip(), stderr_expected)

    def test_ioencoding_error_handler_without_codec_uses_utf8(self) -> None:
        self.env["PYTHONIOENCODING"] = ":replace"
        self.probe.write_text(f"print({ascii(SAMPLE)})\nraise SystemExit(7)\n", encoding="ascii")
        self.assertEqual(self.capture_in_powershell(866), {
            "text": SAMPLE, "code": 7, "restored": 866, "ioencoding": ":replace",
        })

    def test_explicit_codec_preserves_ignore_environment_options(self) -> None:
        self.env["PYTHONIOENCODING"] = "cp1251"
        self.probe.write_text(
            "import json, sys\n"
            "print(json.dumps({'utf8': sys.flags.utf8_mode, 'ignore': sys.flags.ignore_environment, "
            "'isolated': sys.flags.isolated, 'encoding': sys.stdout.encoding}), flush=True)\n"
            f"sys.stdout.buffer.write({ascii(SAMPLE)}.encode(sys.stdout.encoding, errors='backslashreplace'))\n"
            "raise SystemExit(7)\n",
            encoding="ascii",
        )
        for flag in ("-E", "-I", "-Es"):
            with self.subTest(flag=flag):
                # The local ANSI code page varies across Windows installations.
                # Match direct Python, including its flags, codec and captured text.
                expected = self.capture_in_powershell(1251, (flag,), direct=True)
                self.assertEqual(expected["code"], 7)
                self.assertEqual(expected["restored"], 1251)
                self.assertEqual(expected["ioencoding"], "cp1251")
                self.assertEqual(json.loads(expected["text"][0])["ignore"], 1)
                self.assertEqual(self.capture_in_powershell(1251, (flag,)), expected)

    def test_installer_and_hook_in_unicode_directory(self) -> None:
        result = self.run_command(["git", "init", "--quiet"], cwd=self.folder)
        self.assertEqual(result.returncode, 0, result.stderr)
        scripts = self.folder / "scripts"
        scripts.mkdir()
        for name in ("kb_python.ps1", "wiki_lint.ps1"):
            shutil.copyfile(ROOT / "scripts" / name, scripts / name)
        lint = scripts / "wiki_lint.py"
        lint.write_text(f"print({ascii(SAMPLE)})\n", encoding="ascii")
        result = self.run_command([
            "cmd.exe", "/d", "/c", "scripts\\install_pre_commit.cmd", "-Root", str(self.folder),
        ])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(self.folder / ".git/hooks/pre-commit"), result.stdout.decode("utf-8"))
        for exit_code in (0, 7):
            lint.write_text(f"print({ascii(SAMPLE)})\nraise SystemExit({exit_code})\n", encoding="ascii")
            result = self.run_command(["git", "hook", "run", "pre-commit"], cwd=self.folder)
            self.assertEqual(result.returncode == 0, exit_code == 0, result.stderr)
            self.assertIn(SAMPLE, (result.stdout + result.stderr).decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
