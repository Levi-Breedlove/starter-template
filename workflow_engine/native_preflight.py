"""Read-only native startup preflight; never initialize a client or read its data."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import stat
import sys


def _directory_status(path: Path) -> str:
    if not path.is_absolute():
        return "relative-path"
    try:
        if not stat.S_ISDIR(path.stat().st_mode):
            return "not-directory"
        if os.statvfs(path).f_flag & os.ST_RDONLY:
            return "read-only-mount"
        access_options = {"effective_ids": True} if os.access in os.supports_effective_ids else {}
        if not os.access(path, os.W_OK | os.X_OK, **access_options):
            return "not-writable"
        return "appears-writable"
    except FileNotFoundError:
        return "missing"
    except (OSError, ValueError, AttributeError, NotImplementedError):
        return "unknown"


def inspect_native(*, pilot: bool = False) -> dict:
    """Check the calling shell's observable prerequisites, not model readiness.

    Only directory metadata, access flags and executable presence are inspected.
    The configured sqlite_home/log_dir may override environment/default locations.
    No configuration, credentials, session data or database contents are read.
    """
    blockers = []
    platform_ready = sys.platform.startswith("linux") or sys.platform == "darwin"
    if not platform_ready:
        blockers.append("Native process control requires Linux, macOS or WSL.")
    if sys.version_info < (3, 10):
        blockers.append("Python 3.10 or newer is required.")
    names = ("codex", "git", "python3", "tar", "mktemp", "timeout") if pilot else ("codex", "git")
    executables = {name: bool(shutil.which(name)) for name in names}
    blockers.extend(f"Required executable not found: {name}." for name, found in executables.items() if not found)
    locations = {}
    try:
        home_value = os.environ.get("CODEX_HOME")
        home = Path(home_value) if home_value is not None else Path.home() / ".codex"
        sqlite_value = os.environ.get("CODEX_SQLITE_HOME")
        sqlite = Path(sqlite_value) if sqlite_value is not None else home
        locations = {
            "CODEX_HOME": {"source": "environment" if home_value is not None else "default", "status": _directory_status(home)},
            "CODEX_SQLITE_HOME": {"source": "environment" if sqlite_value is not None else "CODEX_HOME", "status": _directory_status(sqlite)},
        }
    except (OSError, RuntimeError, ValueError):
        blockers.append("Could not resolve observable client-state directories.")
    for name, observation in locations.items():
        if observation["status"] != "appears-writable":
            blockers.append(f"{name}: {observation['status']}. Inspect the selected client's state from its ordinary authorized terminal.")
    return {
        "schema_version": 1,
        "status": "blocked" if blockers else "no-known-blocker",
        "blockers": blockers,
        "codespaces_environment": os.environ.get("CODESPACES", "").lower() == "true",
        "executables": executables,
        "state_locations": locations,
        "native_startup_verified": False,
        "next_action": "Do not launch or reserve a native invocation while blocked. Keep current-session consultation available. Compare the ordinary terminal with any agent sandbox; use only supported client setup and preserve existing controls." if blockers else "Confirm the actual configured state locations, client version, exec options and existing permissions in the ordinary authorized terminal before any separately authorized native invocation.",
        "limits": "Metadata/access checks only in this process; no writes, config/auth reads, subprocesses, model calls or AWS access. Configured sqlite_home/log_dir and managed policy can override observed locations. Apparent writability is not a successful client startup or proof of spending authority.",
    }
