import setuptools
from setuptools import find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setuptools.setup(
    name="pyaqua",
    version="0.1.0",
    packages=find_packages(),
    url="https://github.com/samapriya/pyaqua",
    install_requires=[
        "requests>=2.23.1",
        "beautifulsoup4>=4.9.3",
        "pandas>=1.3.3",
        "python_dateutil>=2.8.2",
        "rapidfuzz>=1.9.0",
        "geojson >= 2.5.0",
        "area >= 1.1.1",
        "natsort >= 8.1.0",
        "tenacity >= 8.0.1",
        'pyproj>=1.9.5.1;platform_system!="Windows"',
        'shapely>=1.6.4;platform_system!="Windows"',
        'fiona>=1.8.6;platform_system!="Windows"',
        'geopandas>=0.5.0;platform_system!="Windows"',
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
    description="Simple CLI for Aqualink API",
    entry_points={
        "console_scripts": [
            "pyaqua=pyaqua.pyaqua:main",
        ],
    },
)
