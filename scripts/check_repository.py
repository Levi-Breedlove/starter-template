#!/usr/bin/env python3
"""Offline checks for bootstrap structure and explicit Markdown link destinations.

Run this file from any working directory; its own location selects the default
repository root. --root selects a different tree, including a temporary fixture.

Supported links: inline links/images and reference definitions, with optional
titles, angle brackets, URL encoding, and fragments. Code fences, inline code,
HTML comments, external URLs, and obvious template placeholders are ignored.
This is deliberately not a complete Markdown parser: it does not validate
heading anchors, undefined reference labels, HTML links, or document semantics.
Symlink directories are not followed while scanning; link targets are resolved
before checking that they stay inside the selected repository.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import html
import os
from pathlib import Path
import re
from typing import Iterator
from urllib.parse import unquote, urlsplit

import bootstrap


REQUIRED_CORE_PATHS = (
    "README.md",
    "AGENTS.md",
    "project/brief.md",
    "project/adoption-report.md",
    "workflows/README.md",
    "workflows/consult.md",
    "workflows/feature.md",
    "workflows/bugfix.md",
    "workflows/brownfield.md",
    "workflows/reconcile.md",
    "workflows/review.md",
    "workflows/release.md",
    "workflows/incident.md",
    "templates/README.md",
    "delivery/current-handoff.md",
    "docs/implementation-plan.md",
    "guide/00-quickstart.md",
    "docs/reference/specification-operations.md",
    "docs/reference/task-execution.md",
    "scripts/bootstrap.py",
    "scripts/workflow.py",
    "scripts/codex_hooks.py",
    "workflow_engine/__init__.py",
    "workflow_engine/engine.py",
    "workflow_engine/context.py",
    "workflow_engine/doctor.py",
    "workflow_engine/native_preflight.py",
    "workflow_engine/specifications.py",
    "workflow_engine/runner.py",
    "specs/0001-workflow-foundation/requirements.md",
    "specs/0001-workflow-foundation/design.md",
    "specs/0001-workflow-foundation/tasks.md",
)

IGNORED_DIRECTORIES = {".git", ".venv", "venv", "node_modules", "__pycache__", ".workflow-state"}
PLACEHOLDER = re.compile(r"<[^<>]+>|\{\{[^{}]+\}\}|\$\{[^{}]+\}|\{[\w-]+\}")
BARE_PLACEHOLDERS = {"URL", "PATH", "LINK", "TARGET", "TODO", "TBD"}
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
REFERENCE = re.compile(r"^ {0,3}\[[^\]\n]+\]:[ \t]*", re.MULTILINE)
ESCAPED_PUNCTUATION = re.compile(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])")
TITLE_AND_CLOSE = re.compile(
    r'''\s*(?:(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\((?:\\.|[^)\\])*\))\s*)?\)'''
)


@dataclass(frozen=True)
class Issue:
    code: str
    source: str
    line: int
    target: str
    message: str


@dataclass
class Report:
    required_files: int = 0
    markdown_files: int = 0
    local_links: int = 0
    skipped_links: int = 0
    issues: list[Issue] = field(default_factory=list)


def _blank(text: str) -> str:
    """Hide non-content without changing line numbers or character offsets."""
    return "".join("\n" if char == "\n" else " " for char in text)


def _escaped(text: str, position: int) -> bool:
    backslashes = 0
    while position > 0 and text[position - 1] == "\\":
        backslashes += 1
        position -= 1
    return backslashes % 2 == 1


def _visible_markdown(text: str) -> str:
    visible = list(text)
    fence_char = ""
    fence_length = 0
    cursor = 0
    while cursor < len(text):
        if cursor == 0 or text[cursor - 1] == "\n":
            line_end = text.find("\n", cursor)
            line_end = len(text) if line_end < 0 else line_end + 1
            line = text[cursor:line_end]
            match = FENCE.match(line.rstrip("\r\n"))
            if fence_char:
                visible[cursor:line_end] = _blank(line)
                if match and match[1][0] == fence_char and len(match[1]) >= fence_length and not match[2].strip():
                    fence_char = ""
                cursor = line_end
                continue
            if match and not (match[1][0] == "`" and "`" in match[2]):
                fence_char, fence_length = match[1][0], len(match[1])
                visible[cursor:line_end] = _blank(line)
                cursor = line_end
                continue

        # Consume comments and code spans in source order. Fences inside a
        # comment cannot change fence state; comment markers in real code are
        # literal and cannot hide later document content.
        if text.startswith("<!--", cursor) and not _escaped(text, cursor):
            end = text.find("-->", cursor + 4)
            end = len(text) if end < 0 else end + 3
            visible[cursor:end] = _blank(text[cursor:end])
            cursor = end
            continue
        if text[cursor] == "`" and not _escaped(text, cursor):
            end = cursor + 1
            while end < len(text) and text[end] == "`":
                end += 1
            delimiter = re.compile(r"(?<!`)`{" + str(end - cursor) + r"}(?!`)")
            close = delimiter.search(text, end)
            if close:
                visible[cursor:close.end()] = _blank(text[cursor:close.end()])
                cursor = close.end()
            else:
                cursor = end
            continue
        cursor += 1
    return "".join(visible)


def _destination(text: str, start: int) -> tuple[str, int, bool] | None:
    """Read one destination; leave the outer inline-link ')' unconsumed."""
    cursor = start
    while cursor < len(text) and text[cursor].isspace():
        cursor += 1
    if cursor >= len(text):
        return None
    angled = text[cursor] == "<"
    if angled:
        cursor += 1
    beginning = cursor
    depth = 0
    while cursor < len(text):
        char = text[cursor]
        if char == "\\" and cursor + 1 < len(text):
            cursor += 2
            continue
        if angled:
            if char == ">":
                return text[beginning:cursor], cursor + 1, True
            if char in "\r\n":
                return None
        elif char.isspace() or (char == ")" and depth == 0):
            return text[beginning:cursor], cursor, False
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        cursor += 1
    if not angled and depth == 0:
        return text[beginning:cursor], cursor, False
    return None


def markdown_destinations(text: str) -> Iterator[tuple[int, str, bool]]:
    """Yield line, destination, angle-wrapper for explicit Markdown targets."""
    visible = _visible_markdown(text)
    for match in REFERENCE.finditer(visible):
        parsed = _destination(visible, match.end())
        if parsed:
            target, _, angled = parsed
            yield visible.count("\n", 0, match.start()) + 1, target, angled

    # Require an actual unescaped opening label bracket. Bracket balance keeps
    # simple nested labels working without treating escaped examples as links.
    brackets: list[int] = []
    cursor = 0
    while cursor < len(visible):
        if not _escaped(visible, cursor):
            if visible[cursor] == "[":
                brackets.append(cursor)
            elif visible[cursor] == "]" and brackets:
                brackets.pop()
                if visible[cursor + 1:cursor + 2] == "(":
                    parsed = _destination(visible, cursor + 2)
                    if parsed:
                        target, end, angled = parsed
                        close = TITLE_AND_CLOSE.match(visible, end)
                        if close:
                            yield visible.count("\n", 0, cursor) + 1, target, angled
                            cursor = close.end()
                            continue
        cursor += 1


def _local_path(target: str, angled: bool) -> str | None:
    target = html.unescape(ESCAPED_PUNCTUATION.sub(r"\1", target)).strip()
    if not target or target.startswith("#") or target.startswith("//"):
        return None
    if PLACEHOLDER.search(target) or target in BARE_PLACEHOLDERS:
        return None
    if angled and (target.lower() in {"url", "path", "link", "target", "name"} or re.fullmatch(r"[\w-]+-id", target)):
        return None
    if re.match(r"^[A-Za-z]:[/\\]", target) or target.startswith("\\"):
        raise ValueError("absolute Windows/UNC paths are not portable repository links")
    parts = urlsplit(target)
    if parts.scheme and parts.scheme.lower() != "file":
        return None
    if parts.scheme.lower() == "file" and parts.netloc not in {"", "localhost"}:
        raise ValueError("remote file URI is not a repository-local target")
    path = unquote(parts.path)
    return path.replace("\\", "/") or None


def _resolved_inside(root: Path, candidate: Path) -> Path:
    resolved = candidate.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("target resolves outside the repository")
    return resolved


def check_repository(root: Path) -> Report:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"repository root is not a directory: {root}")
    report = Report()
    required_paths = REQUIRED_CORE_PATHS
    manifest = root / ".aws-workflow/manifest.json"
    if manifest.exists() or (root / ".aws-workflow/scripts/workflow.py").exists():
        required_paths = ("AGENTS.md", ".aws-workflow/manifest.json", ".aws-workflow/scripts/workflow.py",
                          ".aws-workflow/workflows/consult.md")
        try:
            data = bootstrap.read_manifest(bootstrap.contained(root, bootstrap.MANIFEST))
            mapped = data["editable_project_records"]
            if len(set(mapped)) != len(mapped):
                raise ValueError("Each editable project record needs a distinct path")
            for relative in mapped:
                bootstrap.contained(root, relative)
            required_paths += tuple(mapped)
        except (OSError, ValueError, RuntimeError, bootstrap.BootstrapError) as error:
            report.issues.append(Issue("invalid-manifest", ".aws-workflow/manifest.json", 0, "", str(error)))
    report.required_files = len(required_paths)
    for relative in required_paths:
        try:
            required = _resolved_inside(root, root / relative)
            if not required.is_file():
                report.issues.append(Issue("missing-core", relative, 0, relative, "required core file is missing or not a file"))
        except (OSError, ValueError, RuntimeError) as error:
            report.issues.append(Issue("invalid-core", relative, 0, relative, str(error)))

    def walk_error(error: OSError) -> None:
        source = Path(error.filename) if error.filename else root
        try:
            relative = source.relative_to(root).as_posix()
        except ValueError:
            relative = str(source)
        report.issues.append(Issue("unreadable-directory", relative, 0, "", f"directory scan failed: {error}"))

    for directory, folders, files in os.walk(root, followlinks=False, onerror=walk_error):
        folders[:] = sorted(name for name in folders if name not in IGNORED_DIRECTORIES and not (Path(directory) / name).is_symlink())
        for name in sorted(files):
            if Path(name).suffix.lower() != ".md":
                continue
            source = Path(directory) / name
            relative = source.relative_to(root).as_posix()
            report.markdown_files += 1
            try:
                _resolved_inside(root, source)
                content = source.read_text(encoding="utf-8")
            except (OSError, UnicodeError, ValueError, RuntimeError) as error:
                report.issues.append(Issue("unreadable-source", relative, 0, "", str(error)))
                continue
            for line, target, angled in markdown_destinations(content):
                try:
                    local = _local_path(target, angled)
                    if local is None:
                        report.skipped_links += 1
                        continue
                    report.local_links += 1
                    # Absolute filesystem paths are checked as absolute, never
                    # reinterpreted as repository-root-relative web paths.
                    resolved = _resolved_inside(root, source.parent / local)
                    if not resolved.exists():
                        report.issues.append(Issue("missing-target", relative, line, target, "local target does not exist"))
                except (OSError, ValueError, RuntimeError) as error:
                    report.issues.append(Issue("invalid-target", relative, line, target, str(error)))
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline Markdown link and bootstrap structure checks only.")
    parser.add_argument("--root", type=Path, default=(Path(__file__).resolve().parents[2] if Path(__file__).resolve().parents[1].name == ".aws-workflow" else Path(__file__).resolve().parents[1]), help="repository root (defaults to this script's repository)")
    args = parser.parse_args(argv)
    print("Scope: link/structure checks only; no semantic, runtime, or AWS verification.")
    try:
        report = check_repository(args.root)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}")
        return 2
    for issue in report.issues:
        location = f"{issue.source}:{issue.line}" if issue.line else issue.source
        target = f" [{issue.target}]" if issue.target else ""
        print(f"ERROR {location}: {issue.code}{target}: {issue.message}")
    outcome = "FAIL" if report.issues else "PASS"
    print(f"{outcome}: {report.markdown_files} Markdown files; {report.local_links} local links; {report.required_files} required core files; {len(report.issues)} issues.")
    return 1 if report.issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
