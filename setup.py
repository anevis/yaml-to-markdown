import os
from typing import List

from setuptools import setup, find_packages

version = os.environ.get("RELEASE_VERSION")

with open("README.md", "r") as fh:
    long_description = fh.read()

long_description = long_description.replace(
    "](", "](https://anevis.github.io/yaml-to-markdown/"
).replace(".md)", ".html)")

with open("requirements.txt", "r") as req_file:
    raw_requirements = req_file.readlines()

requirements: List[str] = []
for req in raw_requirements:
    if req.strip() == "# Dev dependencies":
        break
    if req.startswith("#") or req.strip() == "":
        continue
    requirements.append(req.strip())

setup(
    name="yaml-to-markdown",
    version=version,
    description="Converts a YAML/JSON file or python Dict/List to a Markdown file",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://anevis.github.io/yaml-to-markdown/",
    license="MIT",
    author="anevis",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "yaml-to-markdown=yaml_to_markdown.convert:main",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
