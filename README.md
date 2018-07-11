# urlExpander

![PyPI](https://img.shields.io/pypi/v/urlexpander.svg)](https://pypi.org/project/urlExpander/) [![PyPI](https://img.shields.io/pypi/l/urlexpander.svg)](https://github.com/SMAPPNYU/urlExpander/blob/master/LICENSE)

urlExpander is a Python package for quickly and thoroughly expanding shortened URLs. 

It is inteded to be used by social media researchers who want to do analysis of links.

Analytics and ad-based services make such analysis difficult. Aside from collecting in-depth engagement data, these services obfuscate the destination of their shortened URLs.

urlExpander was created to address this challenge in a scalable and robust manner. It does so by providing utility functions to convert Tweets into link meta datasets, filter for known for [link-shortening services](https://github.com/SMAPPNYU/urlExpander/blob/master/urlexpander/core/constants.py#L4-L25) (like bit.ly), resolve shortened links, and parse the title, description and paragraphs from webpages.

This package differs from other approaches because it handles ad-based urls (like adf.ly, lnx.lu, linkbucks.com, and adfoc.us) thanks to the [Unshortenit](http://unshortenit.readthedocs.io/en/latest/) library, as well as resolves redirects to defunct websites (like blacktolive.com). Most importantly, the urlExpander and offers robust multithreaded url expansion.

The multithreaded url expansion was created to overcome the bottleneck of mass link expansion through parallelization, minimizating requests, caching results, and chunking the input into smaller pieces.

## Documentation
We'll generate a readthedocs shortly!

## Acknowledgements
urlExpander was written by Leon Yin with major contributions by Nicole Baram and Gregory Eady for the Social Media and Political Participation Lab at NYU. 