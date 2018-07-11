from setuptools import setup

setup(
    name="urlExpander",
    version='0.0.2',
    description="A package for expanding shortened links.",
    long_description="This package makes working with link data from social media and webpages easier. It not only expands links, but catches errors, and makes parallel link expansion quick and efficient.",
    packages=['urlexpander'],
    author="leon yin",
    author_email="ly501@nyu.edu",
    url="https://github.com/smappnyu",
    keywords='unshorten expand link url parallel multithread unwind unwound',
    license="MIT",
    py_modules=['urlexpander'],
    install_requires=[
        'tldextract',
        'pandas',
        'numpy',
        'tqdm',
        'unshortenit'
    ]
)
