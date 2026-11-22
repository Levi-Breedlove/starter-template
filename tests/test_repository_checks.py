"""Behavioral fixtures for the offline link/structure check; no remote calls."""

import errno
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_repository.py"
sys.path.insert(0, str(SCRIPT.parent))
from check_repository import REQUIRED_CORE_PATHS, check_repository  # noqa: E402


class RepositoryChecksTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        for relative in REQUIRED_CORE_PATHS:
            self.write(relative, "# Fixture\n")

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_existing_paths_fragments_titles_and_reference_links_pass(self):
        self.write("docs/guide(v1).md", "# Guide\n")
        self.write("docs/file with spaces.md", "# Spaces\n")
        self.write("README.md", """# Valid links
[nested](docs/guide(v1).md#heading)
[escaped](docs/guide\\(v1\\).md "Guide")
[spaces](<docs/file with spaces.md> 'Title')
[encoded](docs/file%20with%20spaces.md?raw=1#intro)
[reference][manual]
[manual]: docs/guide(v1).md#heading "Guide"
[directory](docs/)
![image](docs/file%20with%20spaces.md)
""")
        report = check_repository(self.root)
        self.assertEqual(report.issues, [])
        self.assertEqual(report.local_links, 7)

    def test_fenced_inline_code_comments_external_and_placeholders_are_ignored(self):
        self.write("README.md", """# Examples
```md
[not a link to check](absent-fenced.md)
```
~~~~ markdown
[not a link to check](absent-tilde.md)
~~~
[still fenced](absent-short-close.md)
~~~~
`[inline](absent-inline.md)`
``[long ` span](absent-long-inline.md)``
<!-- [comment](absent-comment.md) -->
[web](https://example.invalid/no-network)
[mail](mailto:reader@example.invalid)
[protocol relative](//example.invalid/path)
[anchor](#unvalidated-heading)
[template](../specs/<work-id>/tasks.md)
[template]({{destination}})
[template](${DOC_PATH})
[template](<url>)
""")
        report = check_repository(self.root)
        self.assertEqual(report.issues, [])
        self.assertEqual(report.local_links, 0)

    def test_missing_inline_and_reference_destinations_report_source_lines(self):
        self.write("README.md", "# Missing\n[broken](absent.md)\n[ref]: docs/gone.md\n")
        issues = check_repository(self.root).issues
        failures = {(item.source, item.line, item.target) for item in issues if item.code == "missing-target"}
        self.assertEqual(failures, {("README.md", 2, "absent.md"), ("README.md", 3, "docs/gone.md")})

    def test_fence_inside_comment_does_not_hide_later_link(self):
        self.write("README.md", "<!--\n```md\n-->\n[broken](missing.md)\n")
        issues = check_repository(self.root).issues
        self.assertTrue(any(item.code == "missing-target" and item.line == 4 and item.target == "missing.md" for item in issues))

    def test_comment_markers_inside_real_code_do_not_hide_later_link(self):
        examples = (
            "```md\n<!--\n```\n[broken](missing.md)\n-->\n",
            "`<!--`\n[broken](missing.md)\n-->\n",
        )
        for text in examples:
            with self.subTest(text=text):
                self.write("README.md", text)
                issues = check_repository(self.root).issues
                self.assertTrue(any(item.code == "missing-target" and item.target == "missing.md" for item in issues))

    def test_escaped_opening_bracket_is_not_a_link(self):
        self.write("README.md", r"\[example](absent.md)" + "\n[real](AGENTS.md)\n")
        report = check_repository(self.root)
        self.assertEqual(report.issues, [])
        self.assertEqual(report.local_links, 1)

    def test_escaped_backticks_do_not_hide_a_real_link(self):
        self.write("README.md", r"\`[broken](missing.md)\`" + "\n")
        issues = check_repository(self.root).issues
        self.assertTrue(any(item.code == "missing-target" and item.target == "missing.md" for item in issues))

    def test_unreadable_noncore_subtree_reports_incomplete_scan(self):
        blocked = self.write("restricted/hidden.md", "[cannot inspect](missing.md)\n").parent
        actual_scandir = os.scandir

        def deny_restricted_directory(path):
            if Path(path) == blocked:
                raise PermissionError(errno.EACCES, "Permission denied", str(path))
            return actual_scandir(path)

        # Simulate the OS denial even when the test process runs as root; the
        # rest of os.walk traverses the actual on-disk fixture normally.
        with patch("check_repository.os.scandir", side_effect=deny_restricted_directory):
            issues = check_repository(self.root).issues
        self.assertTrue(any(item.code == "unreadable-directory" and item.source == "restricted" for item in issues))
        self.assertFalse(any(item.target == "missing.md" for item in issues))

    def test_missing_required_file_fails_structure_check(self):
        (self.root / "AGENTS.md").unlink()
        issues = check_repository(self.root).issues
        self.assertTrue(any(item.code == "missing-core" and item.target == "AGENTS.md" for item in issues))

    def test_existing_outside_targets_are_rejected_including_encoded_traversal(self):
        outside = self.base / "outside.md"
        outside.write_text("# Exists outside the selected repository\n", encoding="utf-8")
        self.write("README.md", f"[parent](../outside.md)\n[encoded](%2e%2e/outside.md)\n[absolute]({outside})\n[file URI]({outside.as_uri()})\n")
        issues = check_repository(self.root).issues
        self.assertEqual(len(issues), 4)
        self.assertTrue(all("outside the repository" in item.message for item in issues))

    def test_symlink_target_cannot_escape_repository(self):
        outside = self.base / "external"
        outside.mkdir()
        (outside / "guide.md").write_text("# Outside\n", encoding="utf-8")
        try:
            (self.root / "jump").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"symlinks unavailable: {error}")
        self.write("README.md", "[escape](jump/guide.md)\n")
        issues = check_repository(self.root).issues
        self.assertTrue(any(item.target == "jump/guide.md" and "outside" in item.message for item in issues))

    def test_markdown_symlink_outside_is_not_read(self):
        outside = self.base / "outside.md"
        outside.write_text("[must not inspect](never-read.md)\n", encoding="utf-8")
        try:
            (self.root / "foreign.md").symlink_to(outside)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"symlinks unavailable: {error}")
        issues = check_repository(self.root).issues
        self.assertTrue(any(item.source == "foreign.md" and item.code == "unreadable-source" for item in issues))
        self.assertFalse(any(item.target == "never-read.md" for item in issues))

    def test_cli_root_option_and_failure_exit_code_from_another_cwd(self):
        self.write("README.md", "[broken](absent.md)\n")
        completed = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root)], cwd=self.base, capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 1)
        self.assertIn("link/structure checks only", completed.stdout)
        self.assertIn("no semantic, runtime, or AWS verification", completed.stdout)
        self.assertIn("absent.md", completed.stdout)

    def test_default_root_comes_from_script_location_not_working_directory(self):
        copied = self.root / "scripts" / "check_repository.py"
        copied.parent.mkdir()
        shutil.copyfile(SCRIPT, copied)
        completed = subprocess.run([sys.executable, str(copied)], cwd=self.base, capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS:", completed.stdout)


if __name__ == "__main__":
    unittest.main()
