"""Package setup"""
import setuptools

from python_utils import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_utils",
    version=VERSION,
    author="The Geen Dog",
    # author_email="author@example.com",
    description="A small python utils package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thegreendog/python-utils",
    packages=setuptools.find_packages(exclude=['tests*']),
    install_requires=[
        'pytz',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
