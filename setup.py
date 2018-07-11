import sys
from setuptools import setup

setup(
    name="urlexpander",
    packages=['urlexpander', 'urlexpander.core'],
    py_modules=['urlexpander'],
    version='0.0.8',
    description="urlExpander is a Python package for quickly and thoroughly expanding shortened URLs.",
    long_description="This package makes working with link data from social media and webpages easier. It not only expands links, but catches errors, and makes parallel link expansion quick and efficient.",
    author="leon yin",
    author_email="ly501@nyu.edu",
    url="https://github.com/SMAPPNYU/urlExpander",
    keywords='unshorten expand link url parallel multithread unwind unwound',
    license="MIT",
    install_requires=[
        'tldextract',
        'pandas',
        'numpy',
        'tqdm',
        'unshortenit'
    ]
)
