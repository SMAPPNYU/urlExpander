# urlExpander
urlExpander is a Python package for quickly and thoroughly expanding shortened URLs. It was inteded to be used by social media researchers who want to do analysis of links. urlExpander is a cornerstone for such workflows by providing utility functions to convert raw tweets into link datasets, filter known link-shortening services (like bit.ly), and resolve those shortened links. 

This package differs from other approaches because it handles redirects, ad based urls (like adf.ly, lnx.lu, linkbucks.com, and adfoc.us) thanks to the [Unshortenit](http://unshortenit.readthedocs.io/en/latest/), resolves redirects to defunct websites (like blacktolive.com), and offers robust multithreaded url expansion.

The multithreaded url expansion was created to overcome the bottleneck of mass link expansion by caching results in an intermediary json file, and chunking the input into smaller sizes.