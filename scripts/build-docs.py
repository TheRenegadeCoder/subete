#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

import tomli


def main():
    config = tomli.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    project = config["project"]
    release = project["version"]
    version = ".".join(release.split(".")[:2])
    destdir = "dochtml" if len(sys.argv) < 2 else sys.argv[1]
    subprocess.run(
        [
            "sphinx-build",
            "-b",
            "html",
            "-d",
            "doctrees",
            "-A",
            f"release={release}",
            "-A",
            f"version={version}",
            "docs",
            destdir,
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
