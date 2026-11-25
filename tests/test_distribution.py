"""Exercise the files GitHub will copy for a new application."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def run(*args, cwd):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=True).stdout


class DistributionTest(unittest.TestCase):
    def test_direct_template_and_brownfield_adoption(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            tree = base / "generated"
            build = [sys.executable, "-B", "scripts/package_template.py", "--output", str(tree)]
            run(*build, cwd=ROOT)
            self.assertNotEqual(subprocess.run(build, cwd=ROOT, capture_output=True).returncode, 0)
            for args in (("init", "-q"), ("add", ".")):
                run("git", *args, cwd=tree)
            # A fresh GitHub template copies tracked files, starting a new history.
            app = base / "new project"
            app.mkdir()
            run("git", "checkout-index", "--all", f"--prefix={app}/", cwd=tree)
            run("git", "init", "-q", cwd=app)
            self.assertFalse((app / ".codex/workflow.json").exists())
            self.assertEqual((app / "README.md").read_bytes(),
                             (ROOT / "distribution/README.md.in").read_bytes())
            for name in ("specs", "evidence"):
                self.assertEqual([p.name for p in (app / name).iterdir()], [".gitkeep"])
            manifest = json.loads((app / ".aws-workflow/manifest.json").read_bytes())
            for key in ("brief", "requirements", "tech", "structure", "architecture"):
                self.assertEqual(manifest["paths"][key], f"project/{key}.md")
                self.assertTrue((app / manifest["paths"][key]).is_file())
            keys = re.compile(r"^\| `(start|resume|status|feature|bugfix|review|release)` \| (.+)$", re.M)
            instructions = (app / "AGENTS.md").read_text()
            self.assertEqual(keys.findall(instructions), keys.findall((ROOT / "AGENTS.md").read_text()))
            self.assertEqual(len(keys.findall(instructions)), 7)
            self.assertIn("case-insensitive", instructions)
            cli = [sys.executable, "-B", ".aws-workflow/scripts/workflow.py", "--root", "."]
            run(*cli, "doctor", cwd=app)
            run(sys.executable, "-B", ".aws-workflow/scripts/check_repository.py", "--root", ".", cwd=app)
            checker = [sys.executable, "-B", ".aws-workflow/scripts/check_repository.py", "--root", "."]
            manifest_path = app / ".aws-workflow/manifest.json"
            original_manifest = manifest_path.read_bytes()
            (app / "alias.md").symlink_to("project/tech.md")
            for invalid in (47, "project/brief.md", ".git/config", "alias.md"):
                with self.subTest(invalid=invalid):
                    bad = json.loads(original_manifest)
                    if isinstance(invalid, int):
                        bad["schema_version"] = invalid
                    else:
                        bad["paths"]["architecture"] = invalid
                        bad["editable_project_records"].remove("project/architecture.md")
                        bad["editable_project_records"] = sorted([*bad["editable_project_records"], invalid])
                    manifest_path.write_text(json.dumps(bad))
                    self.assertNotEqual(subprocess.run(checker, cwd=app, capture_output=True).returncode, 0)
            manifest_path.write_bytes(original_manifest)
            (app / "alias.md").unlink()
            pkg = app / ".aws-workflow"
            installer = [sys.executable, "-B", str(pkg / "scripts/bootstrap.py"), "--source", str(pkg)]
            repeated = run(*installer, "--target", str(app), "--mode", "greenfield", "--apply", "--json", cwd=app)
            self.assertEqual(json.loads(repeated)["status"], "unchanged")
            run(*cli, "new", "0001-bookings", "--title", "Workshop bookings", "--mode", "greenfield",
                "--route", "requirements-first", "--activate", cwd=app)
            self.assertEqual(json.loads(run(*cli, "context", "--compact", cwd=app))["work"]["id"], "0001-bookings")
            brown = base / "existing"
            brown.mkdir()
            known = {"service.py": "BOOKING_LIMIT = 8\n", "docs/platform.md": "# Existing stack\n",
                     "infra/main.tf": "# existing IaC authority\n", ".github/workflows/ci.yml": "name: Existing CI\n",
                     "backlog.md": "# Existing task authority\n", "notes.md": "committed\n"}
            for name, content in known.items():
                path = brown / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            original = b"# Existing project instructions\r\n"
            (brown / "AGENTS.md").write_bytes(original)
            run("git", "init", "-q", cwd=brown)
            run("git", "add", ".", cwd=brown)
            run("git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                "commit", "-qm", "Existing application", cwd=brown)
            (brown / "notes.md").write_text("unsaved user decision\n")
            known["notes.md"] = "unsaved user decision\n"
            args = [*installer, "--target", str(brown), "--mode", "brownfield", "--tech", "docs/platform.md",
                    "--authority", "backlog.md", "--json"]
            preview = json.loads(run(*args, cwd=brown))
            self.assertEqual(preview["status"], "preview")
            self.assertFalse((brown / ".aws-workflow").exists())
            run(*args, "--apply", cwd=brown)
            self.assertEqual(json.loads(run(*args, "--apply", cwd=brown))["status"], "unchanged")
            self.assertTrue((brown / "AGENTS.md").read_bytes().startswith(original))
            self.assertEqual(known, {name: (brown / name).read_text() for name in known})
            installed = json.loads((brown / ".aws-workflow/manifest.json").read_bytes())
            self.assertEqual(installed["paths"]["tech"], "docs/platform.md")
            self.assertFalse((brown / "project/tech.md").exists())
            run(*cli, "doctor", cwd=brown)
            self.assertEqual(run("git", "diff", "--cached", "--name-only", cwd=brown), "")


if __name__ == "__main__":
    unittest.main()
