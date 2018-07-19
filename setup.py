import sys
from setuptools import setup

long_description = """This package makes working with link data from social media and webpages easier. It not only expands links, but catches errors, and makes parallel link expansion quick and efficient.
```
import urlexpander as ux
ux.expand('https://trib.al/xXI5ruM')
```
returns
```
{'original_url': 'https://trib.al/xXI5ruM',
 'resolved_domain': 'breitbart.com',
 'resolved_url': 'https://www.breitbart.com/video/2017/12/31/lindsey-graham-trump-just-cant-tweet-iran/'}
 ```
 
 Please take a look at the [quickstart](http://nbviewer.jupyter.org/github/SMAPPNYU/urlExpander/blob/master/examples/quickstart.ipynb?flush=true).

    """

setup(
    name="urlexpander",
    packages=['urlexpander', 'urlexpander.core'],
    py_modules=['urlexpander'],
    version='0.0.29',
    description="urlExpander is a Python package for quickly and thoroughly expanding shortened URLs.",
    long_description=long_description,
    author="leon yin",
    author_email="whereisleon@gmail.com",
    url="https://github.com/SMAPPNYU/urlExpander",
    keywords='smapp social media unshorten expand link url',
    license="MIT",
    install_requires=[
        'tldextract',
        'pandas',
        'numpy',
        'tqdm',
        'unshortenit'
    ]
)
