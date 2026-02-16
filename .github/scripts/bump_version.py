import os
import re
import subprocess
from pathlib import Path


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def write_output(key: str, value: str) -> None:
    output_path = os.getenv("GITHUB_OUTPUT")
    if not output_path:
        return
    with open(output_path, "a", encoding="utf-8") as fh:
        fh.write(f"{key}={value}\n")


def latest_version_tag() -> str | None:
    tags = run("git", "tag", "--list", "v*", "--sort=-v:refname").splitlines()
    for tag in tags:
        if re.fullmatch(r"v\d+\.\d+\.\d+", tag):
            return tag
    return None


def read_setup_version() -> str:
    setup_text = Path("setup.py").read_text(encoding="utf-8")
    match = re.search(r"version\s*=\s*['\"](\d+\.\d+\.\d+)['\"]", setup_text)
    if not match:
        raise RuntimeError("Could not parse current version from setup.py")
    return match.group(1)


def commit_log_since(tag: str | None) -> str:
    if tag:
        return run("git", "log", "--format=%s%n%b", f"{tag}..HEAD")
    return run("git", "log", "--format=%s%n%b")


def commits_since(tag: str | None) -> int:
    if tag:
        return int(run("git", "rev-list", "--count", f"{tag}..HEAD"))
    return int(run("git", "rev-list", "--count", "HEAD"))


def determine_bump(log_text: str) -> str:
    if re.search(r"BREAKING CHANGE|!:", log_text, re.IGNORECASE):
        return "major"
    if re.search(r"(?mi)^feat(\(.+\))?:", log_text):
        return "minor"
    return "patch"


def bump_version(current: str, bump: str) -> str:
    major, minor, patch = [int(part) for part in current.split(".")]
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def update_setup_py(new_version: str) -> bool:
    setup_path = Path("setup.py")
    setup_text = setup_path.read_text(encoding="utf-8")
    new_text, replacements = re.subn(
        r"version\s*=\s*['\"]\d+\.\d+\.\d+['\"]",
        f"version='{new_version}'",
        setup_text,
        count=1,
    )
    if replacements == 0:
        raise RuntimeError("Could not find version assignment in setup.py")
    if new_text == setup_text:
        return False
    setup_path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    tag = latest_version_tag()
    current_version = tag[1:] if tag else read_setup_version()

    if commits_since(tag) == 0:
        write_output("released", "false")
        return

    bump_kind = determine_bump(commit_log_since(tag)) if tag else "patch"
    next_version = bump_version(current_version, bump_kind)
    changed = update_setup_py(next_version)

    write_output("version", next_version)
    write_output("released", "true" if changed else "false")
    print(f"Bumped {current_version} -> {next_version} ({bump_kind})")


if __name__ == "__main__":
    main()
