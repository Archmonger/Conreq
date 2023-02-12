from pathlib import Path

from setuptools import find_packages, setup

# Variables
ROOT_DIR = Path(__file__).parent
with (ROOT_DIR / ".version").open() as f:
    VERSION = f.read().strip()
with (ROOT_DIR / "README.md").open() as f:
    README = f.read().strip()


# PyPi Information
PACKAGE = {
    "name": "conreq",
    "version": VERSION,
    "packages": find_packages(str(ROOT_DIR)),
    "description": "",
    "long_description": README,
    "long_description_content_type": "text/markdown",
    "author": "Archmonger",
    "author_email": "archiethemonger@gmail.com",
    "url": "https://github.com/Archmonger/Conreq",
    "license": "GPLv3",
    "include_package_data": True,
    "zip_safe": False,
    "classifiers": [
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Internet :: WWW/HTTP",
    ],
}


# Requirements
requirements = []
with (ROOT_DIR / "requirements" / "main.txt").open() as f:
    requirements.extend(
        line
        for line in map(str.strip, f)
        if not line.startswith("#") and not line.startswith("git+")
    )

PACKAGE["install_requires"] = requirements


# Install
if __name__ == "__main__":
    setup(**PACKAGE)
