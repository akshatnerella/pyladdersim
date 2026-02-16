import argparse
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


def parse_setup_version(text: str) -> str:
    match = re.search(r"version\s*=\s*['\"](\d+\.\d+\.\d+)['\"]", text)
    if not match:
        raise RuntimeError("Could not parse version from setup.py")
    return match.group(1)


def base_branch_version(base_remote: str, base_ref: str) -> str:
    setup_on_base = run("git", "show", f"{base_remote}/{base_ref}:setup.py")
    return parse_setup_version(setup_on_base)


def bump_version(version: str, bump: str) -> str:
    major, minor, patch = [int(part) for part in version.split(".")]
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def update_setup(new_version: str) -> bool:
    setup_path = Path("setup.py")
    original = setup_path.read_text(encoding="utf-8")
    updated, replacements = re.subn(
        r"version\s*=\s*['\"]\d+\.\d+\.\d+['\"]",
        f"version='{new_version}'",
        original,
        count=1,
    )
    if replacements == 0:
        raise RuntimeError("Could not find version assignment in setup.py")
    if updated == original:
        return False
    setup_path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bump", choices=["major", "minor", "patch"], required=True)
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--base-remote", default="origin")
    args = parser.parse_args()

    setup_text = Path("setup.py").read_text(encoding="utf-8")
    current_version = parse_setup_version(setup_text)
    base_version = base_branch_version(args.base_remote, args.base_ref)
    target_version = bump_version(base_version, args.bump)

    changed = update_setup(target_version)
    write_output("version", target_version)
    write_output("changed", "true" if changed else "false")
    print(f"current={current_version} base={base_version} target={target_version} changed={changed}")


if __name__ == "__main__":
    main()
