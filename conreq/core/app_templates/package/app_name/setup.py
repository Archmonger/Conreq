import json
from pathlib import Path

from setuptools import find_packages, setup


# Helper Functions
def read_file(file_path):
    with file_path.open() as f:
        return f.read()


# Variables
ROOT_DIR = Path(__file__).parent
APP_STORE = json.loads(read_file(ROOT_DIR / "app_store.json"))


# PyPi Information
PACKAGE = {
    "name": APP_STORE["package_name"],
    "version": APP_STORE["version"],
    "packages": find_packages(str(ROOT_DIR)),
    "description": APP_STORE["description"],
    "long_description": APP_STORE["long_description"],
    "long_description_content_type": APP_STORE["long_description_content_type"],
    "author": APP_STORE["author"],
    "author_email": APP_STORE["author_email"],
    "url": APP_STORE["repository_url"],
    "license": APP_STORE["license_type"],
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
with (ROOT_DIR / "requirements.txt").open() as f:
    for line in map(str.strip, f):
        if not line.startswith("#"):
            requirements.append(line)
PACKAGE["install_requires"] = requirements


# Install
if __name__ == "__main__":
    setup(**PACKAGE)
