from setuptools import setup, find_packages
import calendar
import time

gmt = time.gmtime()
ts = calendar.timegm(gmt)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="yaml-to-markdown",
    version=f"0.1.{ts}",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://anevis.github.io/yaml-to-markdown/",
    license="MIT",
    author="anevis",
    install_requires=[
        "click==8.1.7",
        "jsonschema[format]==4.21.1",
        "pyyaml==6.0.1",
    ],
    entry_points={
        "console_scripts": [
            "yaml-to-markdown=yaml_to_markdown.convert:main",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
