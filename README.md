# urlExpander

[![PyPI](https://img.shields.io/pypi/v/urlexpander.svg)](https://pypi.org/project/urlExpander/) [![PyPI](https://img.shields.io/pypi/l/urlexpander.svg)](https://github.com/SMAPPNYU/urlExpander/blob/master/LICENSE)

urlExpander is a Python package for quickly and thoroughly expanding shortened URLs. 

## About
urlExpander is inteded to be used by social media researchers who want to do analysis of links.

Analytics and ad-based services make such analysis difficult. Aside from collecting in-depth user engagement data, these services obfuscate the destination of the shortened URLs.

urlExpander was created to address this challenge in a scalable and robust manner. It does so by providing utility functions to convert Tweets into link datasets, filter for known for [link-shortening services](https://github.com/SMAPPNYU/urlExpander/blob/master/urlexpander/core/constants.py#L4-L25) (like bit.ly), resolve shortened links, and parse the title and meta description from webpages.

This package differs from other approaches because it handles ad-based urls (like adf.ly, lnx.lu, linkbucks.com, and adfoc.us) thanks to the [Unshortenit](http://unshortenit.readthedocs.io/en/latest/) library, as well as resolves redirects to defunct websites (like blacktolive.com). Most importantly, urlExpander and offers multithreaded url expansion.

The multithreaded url expansion was created to overcome the bottleneck of mass link expansion through parallelization, minimizating http requests, caching results, and chunking the input into smaller pieces.

## Installation
```
pip install urlexpander
```

## Documentation
We'll generate a readthedocs shortly!

## Acknowledgements
urlExpander was written by [Leon Yin](http://www.leonyin.org/) with major contributions by Nicole Baram and Gregory Eady for the [Social Media and Political Participation Lab at NYU](https://wp.nyu.edu/smapp/). 

Please cite urlExpander in your publications if it helps your research. Here is an example BibTeX entry:

```
@software{urlexpander,
  author = {Leon Yin and SMaPP Lab},
  title = {urlExpander},
  year = {2018}
  version = {0.0.11},
  howpublished = {https://github.com/SMAPPNYU/urlExpander},
}```