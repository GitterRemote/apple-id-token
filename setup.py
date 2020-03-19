#!/usr/bin/env python3
import os
from setuptools import find_packages, setup


version = "1.0.0"

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    long_description = readme.read()

EXTRAS_REQUIRE = {
    "tests": ["pytest"]
}

EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"]

setup(
    name="AppleIDToken",
    version=version,
    author="Shuaihu Wang",
    author_email="shuaihu.w@gmail.com",
    description="Verify Apple ID token (JWT) from server in Python",
    license="MIT",
    keywords="apple id token authenticate web jwt signing",
    url="https://github.com/GitterRemote/apple-id-token",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    long_description=long_description,
    python_requires=">=3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=["pyjwt[crypto]", "requests", "rsa"],
    extras_require=EXTRAS_REQUIRE,
)
