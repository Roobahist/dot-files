#!/usr/bin/env python3
"""Check that this public repository contains only approved portable files."""
import json
import pathlib
import re
import subprocess
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]
manifest_path = ROOT / "mac-setup-files.txt"
files = [line.strip() for line in manifest_path.read_text().splitlines()
         if line.strip() and not line.startswith("#")]
assert len(files) == len(set(files)) and files, "Bad shared file manifest"

EXTRA_FILES = {
    ".gitignore", "README.md", "apply.sh", "install.sh",
    "setup-global-gitignore.sh", "mac-setup-files.txt", "scripts/check-public.py",
    ".github/workflows/ci.yml", ".github/workflows/notify-mac-setup.yml",
}
actual = set(subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "-z"]).decode().split("\0"))
actual.discard("")
assert actual == set(files) | EXTRA_FILES, f"Unexpected tracked file paths: {sorted(actual ^ (set(files) | EXTRA_FILES))}"

PATTERNS = (
    ("user home path", re.compile(r"/Users/|/home/[A-Za-z0-9._-]+")),
    ("email address", re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")),
    ("private key or known token", re.compile(
        r"-----BEGIN [^-]*PRIVATE KEY-----|github_pat_[A-Za-z0-9_]+|gh[pousr]_[A-Za-z0-9]+|AKIA[A-Z0-9]{16}")),
    ("assigned credential", re.compile(
        r"\b(?:password|passwd|auth_token|access_token|client_secret|api_key)\s*[:=]\s*['\"]?\S+", re.I)),
    ("private workflow terminology", re.compile(r"\bgrading\b", re.I)),
)
for name in files:
    relative = pathlib.PurePosixPath(name)
    assert not relative.is_absolute() and ".." not in relative.parts
    assert relative.parts[0] in {"aerospace", "alacritty", "atuin", "karabiner", "sketchybar", "unsplash"}
    target = ROOT / relative
    assert target.is_file() and not target.is_symlink(), name
    text = target.read_text()
    for reason, pattern in PATTERNS:
        assert not pattern.search(text), f"{name}: {reason}"
    if target.suffix == ".toml":
        tomllib.loads(text)
    if target.suffix == ".json":
        json.loads(text)

karabiner = json.loads((ROOT / "karabiner/karabiner.json").read_text())
assert len(karabiner["profiles"]) == 1
rules = karabiner["profiles"][0]["complex_modifications"]["rules"]
assert len([r for r in rules if r.get("enabled") is False]) == 1
assert sum(r["description"].startswith("Example (disabled)") for r in rules) == 1
assert len(rules) == 5
print(f"Portable profile validated: {len(files)} configuration files")
