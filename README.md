# urlExpander

[![PyPI](https://img.shields.io/pypi/v/urlexpander.svg)](https://pypi.org/project/urlExpander/) [![PyPI](https://img.shields.io/pypi/l/urlexpander.svg)](https://github.com/SMAPPNYU/urlExpander/blob/master/LICENSE)
[![DOI](https://zenodo.org/badge/140624652.svg)](https://zenodo.org/badge/latestdoi/140624652)

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

## Quickstart
```
import urlexpander
urlexpander.expand('https://trib.al/xXI5ruM')
```
returns
```
'https://www.breitbart.com/video/2017/12/31/lindsey-graham-trump-just-cant-tweet-iran/'
```
The function shines given a massive list of urls to unshorten:
```
resolved_links = urlexpander.expand(list_of_short_urls, 
                                    chunksize=1280, 
                                    n_workers=64,
                                    cache_file='tmp.json')
```

Check out this [Jupyter Notebook](http://nbviewer.jupyter.org/github/SMAPPNYU/urlExpander/blob/master/examples/quickstart.ipynb?flush_cache=true) for a more in-depth quickstart!

## More Examples
[Links as Data](https://github.com/yinleon/links-as-data)<br>
How to extract links from congressional Tweets, preprocess them, and use them as features to predict poltical affiliation. View the Notebook on [GitHub](https://github.com/yinleon/links-as-data/blob/master/nbs/congress-links.ipynb) | [NbViewer](http://bit.ly/links-as-data) | [Slides](http://bit.ly/links-as-data-slides)| [Binder](https://mybinder.org/v2/gh/yinleon/links-as-data/master?filepath=nbs%2Fcongress-links.ipynb)

## Documentation
We'll generate a readthedocs shortly!

## Acknowledgements
urlExpander was written by [Leon Yin](http://www.leonyin.org/) with contributions by Megan Brown, Nicole Baram and Gregory Eady for the [Social Media and Political Participation Lab at NYU](www.smappnyu.org). 

Please cite urlExpander in your publications if it helps your research. Here is an example BibTeX entry:

```
@misc{leon_yin_2018_1345144,
  author       = {Leon Yin},
  title        = {SMAPPNYU/urlExpander: Initial release},
  month        = aug,
  year         = 2018,
  doi          = {10.5281/zenodo.1345144},
  url          = {https://doi.org/10.5281/zenodo.1345144}
}
```
Please also send us your work :)

## Research Output
urlExpander is being used is several forthcoming publications from the SMaPP Lab (and perhaps from you?).
We'll keep a running tally here.

Yin, Leon, Franziska Roscher, Richard Bonneau, Jonathan Nagler, and Joshua A. Tucker. 2018.
“[Your Friendly Neighborhood Troll: The Internet Research Agency’s Use of Local and Fake News in the 2016 US
Presidential Campaign.](https://smappnyu.org/wp-content/uploads/2018/11/SMaPP_Data_Report_2018_01_IRA_Links_1.pdf)” <i>SMaPP Data Report</i>. 2018:01
