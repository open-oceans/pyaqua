import setuptools
from setuptools import find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setuptools.setup(
    name="pyaqua",
    version="0.2.0",
    packages=find_packages(),
    url="https://github.com/samapriya/pyaqua",
    install_requires=[
        "requests>=2.23.1",
        "pandas>=1.3.3",
        "python_dateutil>=2.8.2",
        "pytz>=2023.3.post1",
        "rapidfuzz>=1.9.0",
        "geojson >= 2.5.0",
        "area >= 1.1.1",
    ],
    license="Apache 2.0",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    author="Samapriya Roy",
    author_email="samapriya.roy@gmail.com",
    description="Simple CLI for Aqualink.org API",
    entry_points={
        "console_scripts": [
            "pyaqua=pyaqua.pyaqua:main",
        ],
    },
)
