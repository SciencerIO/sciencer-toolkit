from locale import currency
import pathlib
from setuptools import setup

curr_dir_path = pathlib.Path(__file__).parent

readme_content = (curr_dir_path/"README.md").read_text()

setup(
    name="sciencer",
    version="0.1.2",
    description="A smarter way to find new articles",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    url="https://github.com/SciencerIO/sciencer-toolkit",
    author="SciencerIO",
    author_email="diogo.rato.11@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities"
    ],
    packages=["sciencer", "sciencer.collectors", "sciencer.expanders",
              "sciencer.providers", "sciencer.filters", "sciencer.utils"],
    include_package_data=True,
    install_requires=["requests"],
)
