import sys
from setuptools import setup

long_description = """This package makes working with link data from social media and webpages easier. It not only expands links, but catches errors, and makes parallel link expansion quick and efficient.
```
import urlexpander
urlexpander.expand('https://trib.al/xXI5ruM')
```
returns
```
'https://www.breitbart.com/video/2017/12/31/lindsey-graham-trump-just-cant-tweet-iran/'
```
 
 Please take a look at the [quickstart](http://nbviewer.jupyter.org/github/SMAPPNYU/urlExpander/blob/master/examples/quickstart.ipynb?flush_cache=true).

    """

setup(
    name="urlexpander",
    packages=['urlexpander', 'urlexpander.core'],
    py_modules=['urlexpander'],
    version='0.0.34',
    description="urlExpander is a Python package for quickly and thoroughly expanding shortened URLs.",
    long_description=long_description,
    author="leon yin",
    author_email="whereisleon@gmail.com",
    url="https://github.com/SMAPPNYU/urlExpander",
    keywords='smapp social media unshorten expand link url',
    long_description_content_type="text/markdown",
    license="MIT",
    install_requires=[
        'tldextract',
        'pandas',
        'numpy',
        'tqdm',
        'unshortenit',
    ]
)
