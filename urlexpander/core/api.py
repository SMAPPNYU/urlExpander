"""
This is the main module of the urlExpander package.
It houses functions to standardize urls, and extract domain names from links.
It also has the expand and multithread expand functions, which are the crux of this package.
"""

import os
import glob
import json
import itertools
import datetime
import concurrent.futures
import collections
import requests
from urllib.parse import urlparse

import unshortenit
from tqdm import tqdm as tqdm
import numpy as np
import pandas as pd
import tldextract

from urlexpander.core import constants

__all__ = ['strip_url',
           'get_domain',
           'is_short',
           'expand',
           'multithread_function']

__author__ = 'Leon Yin'

def strip_url(url):
    '''
    Best attempt to standardize websites.
    
    :input url: a string of a URl
    :returns: a URL stripped of www. and https:
    '''
    if url:
        return url.replace('www.', '').replace('http://', '').replace('https://', '').rstrip('/')
    else:
        return url

def _chunks(l, chunksize):
    """Yield successive n-sized chunks from l.
    Taken from https://stackoverflow.com/a/312464/5094480
    """
    for i in range(0, len(l), chunksize):
        yield l[i:i + chunksize]

def get_domain(url):
    '''
    Returns domain name of a URL (and removes "www.")
    e.g. 'https://www.nytimes.com/2016/12/23/upshot/...' to 'nytimes.com'
    
    :input url: a string of a url, can contain https://
    :returns: a string of the domain
    '''
    extracted = tldextract.extract(url)
    if extracted.suffix == '' or extracted.domain == '':
        domain = url
    elif extracted.subdomain == '':
        domain = "{}.{}".format(extracted.domain, extracted.suffix)
    else:
        domain = "{}.{}".format(extracted.domain, extracted.suffix)
    domain = domain.lower()
    return domain

def is_short(url, list_of_domains=constants.all_short_domains):
    '''
    Returns True if a domain is in a list_of_domains. 
    Make sure that domain and list_of_domains is preprocessed (or not at all),
    in the same way.
    
    :input domain: (str) a standardized domain name
    :input list_of_domains: (list of str) of standardized domain names
    :returns: boolean
    '''
    domain = get_domain(url)
    
    return _is_short_domain(domain, list_of_domains=list_of_domains)

def _is_short_domain(domain, list_of_domains=constants.all_short_domains):
    '''
    A function which returns True if a domain is in a list_of_domains. 
    Make sure that domain and list_of_domains is preprocessed (or not at all),
    in the same way.
    
    :input domain: (str) a standardized domain name
    :input list_of_domains: (list of str) of standardized domain names
    :returns: boolean
    '''
    if domain in list_of_domains:
        return True
    return False

def _parse_error(error, verbose=False):
    '''
    Although some redirects no longer work, we can still use the response from the error to figure out where it would have gone.
    This function parses error messages from requests.head (called in expand), to try to figure out what website the bit-link was intended to re-direct to.
    
    :param error: a string of the error response from unshorten.
    :returns: the domain parsed from the error string, and the long_url. If the error can't be parsed, the domain is -1
    '''
    if 'ConnectionPool' in error:
        if verbose:
            print("ConnectionPool")
        vals = error.split("ConnectionPool(host='")[1].split("',")
        domain = vals[0]
        url_endpoint = vals[1].split('Max retries exceeded with url: ')[-1].split(" (Caused by")[0]
        url_endpoint = os.path.join('http://', domain, '__CONNECTIONPOOL_ERROR__')
        
    elif 'Client Error: ' in error or 'Server Error' in error:
        if verbose:
            print("ConnectionError or Server Error")
        url_endpoint = error.split(" for url: ")[-1]
        domain = get_domain(url_endpoint)
        url_endpoint = os.path.join('http://', domain, '__CLIENT_ERROR__')
        
    else:
        if verbose:
            print("Unknown error")
        domain, url_endpoint = -1, None
    
    return domain, url_endpoint


def _expand(link, timeout=2, verbose=False, **kwargs):
    '''
    Expands a url, while taking into consideration: special link shortener or analytics platforms that either need a sophisticated
    redirect(st.sh), or parsing of the url (ln.is)
    
    :param link: string of a link to unshorten.
    :returns: a dictionary with the original link, the unshortened link, and the unshortened domain.
    '''
    try:
        r = requests.head(link, 
                          allow_redirects=True, 
                          timeout=timeout,
                          **kwargs)
        r.raise_for_status()
        url_long = r.url
        domain = get_domain(url_long)
        if verbose:
            print("First expansion OK")
        
    except requests.exceptions.RequestException as e:
        if verbose:
            print("First expansion Failed")
        domain, url_long = _parse_error(str(e), verbose=verbose)

    # replace list with constants.url_appenders
    if domain in constants.url_appenders:
        if verbose:
            print("domain in url appenders")
        url_long = url_long.replace(domain, '')
        domain = get_domain(url_long)
    
    elif domain in constants.short_domain_ad_redirects or domain == -1:
        if verbose:
            print("domain in ad redirect")
        url_long = unshortenit.UnshortenIt().unshorten(link,
                                                       timeout=timeout)
        domain = get_domain(url_long)
        

    return dict(original_url=link,
                resolved_domain=domain,
                resolved_url=url_long)

def expand(links_to_unshorten, chunksize=1280, n_workers=1, 
           cache_file=None, random_seed=303, 
           verbose=0, filter_function=None, **kwargs):
    '''
    Calls expand with multiple (``n_workers``) threads to unshorten a list of urls. Unshortens all urls by default, unless one sets a ``filter_function``.
    
    :param links_to_unshorten: (list, str) either an idividual or list (str) of urls to unshorten
    :param chunksize: (int) chunks links_to_unshorten, which makes computation quicker with larger inputs
    :param n_workers: (int) how many threads
    :param cache_file: (str) a path to a json file to read and write results in
    :param random_seed: (int) initializes the random state for shuffling the input
    :param verbose: (int) whether to print updates and errors. 0 is silent. 1 is progress bar. 2 is progress bar and errors.
    :param filter_function: (func) a boolean used to filter url shorteners out
        
    
    :returns: (list) a list of resolved urls
    '''
    
    if isinstance(links_to_unshorten, str):
        return _expand(links_to_unshorten, **kwargs)['resolved_url']
    
    else:
        links_to_unshorten_ = links_to_unshorten.copy()

        # get uniques
        if isinstance(links_to_unshorten, list):
            links_to_unshorten = list(set(links_to_unshorten))
        elif isinstance(links_to_unshorten, pd.Series):
            links_to_unshorten = links_to_unshorten.unique().tolist()

        # shuffle the inputs, this is to reduce the changes of making requests to the same domain.
        np.random.seed(random_seed)
        np.random.shuffle(links_to_unshorten)

        # filter for URLs that need to be shortened according to some boolean function.
        if filter_function:
            links_to_unshorten = [_ for _ in links_to_unshorten if filter_function(_)]

        # read cache file
        unshortened_urls = []
        if cache_file and os.path.exists(cache_file):
            with open(cache_file, 'r') as f_:
                for line in f_:
                    unshortened_urls.append(json.loads(line))
                abd_ = [_['original_url'] for _ in unshortened_urls]
                links_to_unshorten = list(set(abd_).symmetric_difference(set(links_to_unshorten)))
        
        # chunk the list of arguments
        if verbose:
            print("There are {} links to unshorten".format(len(links_to_unshorten)))
            total = (len(links_to_unshorten) // chunksize) + 1
            chunk_iter = tqdm(_chunks(links_to_unshorten, chunksize=chunksize), total=total)
        else:
            chunk_iter = _chunks(links_to_unshorten, chunksize=chunksize)
        
        for chunk in chunk_iter:
            # create n_workers threads, and map chunked argumnets to them
            with concurrent.futures.ThreadPoolExecutor(max_workers = n_workers) as executor:
                future_to_url = {executor.submit(_expand, url, **kwargs): 
                                 url for url in chunk}
                for i, future in enumerate(concurrent.futures.as_completed(future_to_url)):
                    try:
                        data = future.result()
                    except Exception as exc:
                        data = str(type(exc))
                        #error.append({chunk[i] : str(type(exc))})
                        if verbose == 2:
                            print("{} failed to resolve due to error: {}".format(chunk[i],
                                                                                 str(type(exc))))
                    finally:
                        if isinstance(data, dict):
                            unshortened_urls.append(data)
                            # save the results
                            if cache_file:
                                with open(cache_file, 'a') as f_:
                                    f_.write(json.dumps(data) + '\n')

        # reorder the urls (or join them into OG list)
        resolved_dict = {_['original_url'] : _['resolved_url'] for _ in unshortened_urls}
        unshortened_urls_ = [resolved_dict.get(_,_) for _ in links_to_unshorten_]

        return unshortened_urls_


def multithread_function(links_to_unshorten, function, cache_col,
                         chunksize=1280, n_workers=64, 
                         cache_file=None, random_seed=303, 
                         verbose=0, **kwargs):
    '''
    Calls 'function' with multiple (n_workers) threads.
    
    :param links_to_unshorten: (list) a list of urls (str) to unshorten
    :param chunksize: (int) chunks links_to_unshorten, which makes computation quicker with larger inputs
    :param n_workers: (int) how many threads
    :param cache_col: (str) the unique key-name to use to save cached rows.
    :param cache_file: (str) a path to a json file to read and write results in
    :param random_seed: (int) initializes the random state for shuffling the input
    :param verbose: (bool) whether to return errors and updates
        
    
    :returns: (list) a list of dictionaries perfect for Pandas Dataframes.
    ''' 
    # shuffle the inputs, this is to reduce the changes of making requests to the same domain.
    np.random.seed(random_seed)
    np.random.shuffle(links_to_unshorten)

    # read cache file
    unshortened_urls = []
    error = []
    if cache_file and os.path.exists(cache_file):
        with open(cache_file, 'r') as f_:
            for line in f_:
                unshortened_urls.append(json.loads(line))
            abd_ = [_[cache_col] for _ in unshortened_urls]
            links_to_unshorten = [link for link in links_to_unshorten if link not in abd_]
    
    if verbose:
        chunk_iter = tqdm(_chunks(links_to_unshorten, chunksize=chunksize))
    else:
        chunk_iter = _chunks(links_to_unshorten, chunksize=chunksize)

    for chunk in chunk_iter:
        # create n_workers threads, and map chunked argumnets to them
        with concurrent.futures.ThreadPoolExecutor(max_workers = n_workers) as executor:
            future_to_url = {executor.submit(function, url, **kwargs): 
                             url for url in chunk}
            for i, future in enumerate(concurrent.futures.as_completed(future_to_url)):
                try:
                    data = future.result()
                except Exception as exc:
                    data = str(type(exc))
                    if verbose:
                            print("{} failed to resolve due to error: {}".format(chunk[i],
                                                                                 str(type(exc))))
                finally:
                    if isinstance(data, dict):
                        unshortened_urls.append(data)
                        # save the results
                        if cache_file:
                            with open(cache_file, 'a') as f_:
                                f_.write(json.dumps(data) + '\n')
    
    return unshortened_urls
    
