#!/usr/bin/env python3
"""Build the exact preinitialized application tree in a new directory."""
import argparse
from pathlib import Path
import shutil
import tempfile

import bootstrap


def build_distribution(source: Path, output: Path) -> None:
    source = source.resolve(strict=True)
    output = output.absolute()
    if output.exists() or output.is_symlink():
        raise ValueError("Distribution destination already exists")
    if not output.parent.is_dir() or source in output.resolve().parents:
        raise ValueError("Select a new directory outside the maintenance checkout")
    # Build privately first. A partial package must never look like a release tree.
    with tempfile.TemporaryDirectory(dir=output.parent) as scratch:
        stage = Path(scratch) / "application"
        stage.mkdir()
        bootstrap.apply_plan(bootstrap.build_plan(source, stage, "greenfield", name="AWS project",
                                                  visible_records=True))
        for directory in ("docs/decisions", "docs/diagrams", "src", "tests", "specs", "evidence",
                          "infrastructure", "security", "costs", "runbooks"):
            path = stage / directory
            path.mkdir(parents=True, exist_ok=True)
            (path / ".gitkeep").touch()
        ignore = stage / ".gitignore"
        ignore.write_bytes((source / ".gitignore").read_bytes() + b"\n" + ignore.read_bytes())
        for name in ("CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md", ".github/pull_request_template.md"):
            target = stage / name
            target.parent.mkdir(exist_ok=True)
            shutil.copyfile(source / name, target)
        shutil.copyfile(source / "distribution/README.md.in", stage / "README.md")
        stage.rename(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        build_distribution(Path(__file__).resolve().parents[1], args.output)
    except (OSError, ValueError, bootstrap.BootstrapError) as exc:
        parser.exit(1, f"Cannot build distribution: {exc}\n")


if __name__ == "__main__":
    main()
