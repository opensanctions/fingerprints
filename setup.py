from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="fingerprints",
    version="1.2.3",
    description="A library to generate entity fingerprints.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="names people companies normalisation iso20275",
    author="Friedrich Lindenberg",
    author_email="friedrich@opensanctions.org",
    url="http://github.com/opensanctions/fingerprints",
    license="MIT",
    packages=find_packages(exclude=["tests", "tools"]),
    namespace_packages=[],
    package_data={},
    include_package_data=True,
    zip_safe=False,
    test_suite="nose.collector",
    install_requires=[
        "normality>=2.0.0,<=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "mypy",
            "black",
            "pyyaml",
            "types-pyyaml",
            "bump2version",
        ],
    },
)
