"""This module has utility functions for scraping text from URLs,
Specifically it helps get the title, description (like what shows up on Google), and paragraphs.
"""

import re
import html
import requests
from collections import OrderedDict

from urlexpander.core import constants

__all__ = ['get_webpage_meta',
           'get_webpage_paragraphs',
           'get_webpage_description',
           'get_webpage_title']
__author__= 'Leon Yin'


def _search_webpage_title(text, headers=constants.headers, **kwargs):
    title = None
    regex = re.compile('<title>(.*?)</title>', re.IGNORECASE|re.DOTALL)
    try:
        title = regex.search(text).group(1)
        title = html.unescape(title)
    except: pass
    return title

    
def _search_webpage_description(text, headers=constants.headers, **kwargs):
    desc = None
    regex =  re.compile('<meta property="og?:description" content="(.*?)>',
                        re.IGNORECASE|re.DOTALL)
    try:
        desc = regex.search(text).group(1).rstrip('/').rstrip(' ').rstrip('"')
        desc = html.unescape(desc)
    except:
        pass
    return desc

def _search_webpage_paragraphs(text, headers=constants.headers, **kwargs):
    paragraphs = []
    try:
        paragraphs = re.findall(r'<p>(.*?)</p>', text)
        paragraphs = [html.unescape(p) for p in paragraphs]
    except:
        pass
    return paragraphs

def _search_image(text, headers=constants.headers, **kwargs):
    img_url = None
    regex =  re.compile('<meta property="og?:image" content="(.*?)>',
                        re.IGNORECASE|re.DOTALL)
    try:
        img_url = regex.search(text).group(1).rstrip('/').rstrip(' ').rstrip('"')
        img_url = html.unescape(desc)
    except:
        pass
    return img_url

def get_webpage_title(url, headers=constants.headers, **kwargs):
    r = requests.get(url, headers=headers, **kwargs)
    title = _search_webpage_title(r.text)
    return title

def get_webpage_description(url, headers=constants.headers, **kwargs):
    r = requests.get(url, headers=headers, **kwargs)
    desc = _search_webpage_description(r.text)
    return desc

def get_webpage_paragraphs(url, headers=constants.headers, **kwargs):
    r = requests.get(url, headers=headers, **kwargs)
    paragraphs = _search_webpage_paragraphs(r.text)
    return paragraphs

def get_webpage_meta(url, headers=constants.headers, **kwargs):
    r = requests.get(url, headers=headers, **kwargs)
    text = r.text
    meta = OrderedDict(url = url,
                       title = _search_webpage_title(text),
                       description = _search_webpage_description(text),
                       paragraphs = _search_webpage_paragraphs(text))
    return meta
