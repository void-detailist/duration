from setuptools import find_packages, setup

with open("VERSION", "r") as f:
    version = f.read().strip()

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="isoduration8601",
    version=version,
    author="Amir Lesani",
    author_email="amirhossein@void-star.co",
    description="Operations with ISO 8601 durations",
    url="https://github.com/bolsote/isoduration",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    zip_safe=False,
    long_description="parse and generate iso 8601",
    long_description_content_type="text/markdown",
    keywords=[
        "datetime",
        "date",
        "time",
        "duration",
        "duration-parsing",
        "duration-string",
        "iso8601",
        "iso8601-duration",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
