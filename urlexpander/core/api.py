import os
import glob
import json
import itertools
import datetime
import concurrent
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
           'is_short_domain',
           'expand',
           'multithread_expand',
           'count_matrix']
__author__= 'Leon Yin'

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
        domain = "{}.{}.{}".format(extracted.subdomain, extracted.domain, extracted.suffix)
    domain = domain.lower().replace('www.', '')
    
    return domain

def is_short(url, list_of_domains=[]):
    '''
    A function which returns True if a domain is in a list_of_domains. 
    Make sure that domain and list_of_domains is preprocessed (or not at all),
    in the same way.
    
    :input domain: (str) a standardized domain name
    :input list_of_domains: (list of str) of standardized domain names, defaults to `constants.all_short_domains`
    :returns:
    '''
    if not list_of_domains:
        list_of_domains =constants.all_short_domains
    domain = get_domain(url)
    
    return is_short_domain(domain, list_of_domains=list_of_domains)

def is_short_domain(domain, list_of_domains=[]):
    '''
    A function which returns True if a domain is in a list_of_domains. 
    Make sure that domain and list_of_domains is preprocessed (or not at all),
    in the same way.
    
    :input domain: (str) a standardized domain name
    :input list_of_domains: (list of str) of standardized domain names, defaults to `constants.all_short_domains`
    :returns:
    '''
    if not list_of_domains:
        list_of_domains = constants.all_short_domains
        
    if domain in list_of_domains:
        return True
    
    return False

def _parse_error(error):
    '''
    Although some redirects no longer work, we can still use the response from the error to figure out where it woudl have gone.
    This function parses error messages from requests.head (called in unshorten), to try to figure out what website the bit-link
    was intended to re-direct to.
    
    :param error: a string of the error response from unshorten.
    :returns: the domain parsed from the error string, and the long_url. If the error can't be parsed, the domain is -1
    '''
    if 'ConnectionPool' in error:
        vals = error.split("ConnectionPool(host='")[1].split("',")
        domain = vals[0]
        url_endpoint = vals[1].split('Max retries exceeded with url: ')[-1].split(" (Caused by")[0]
        url_endpoint = os.path.join('http://', domain + url_endpoint)
    else:
        domain, url_endpoint = -1, error
    return domain, url_endpoint

def _chunks(iterable, chunksize):
    """Yield successive n-sized chunks from l.
    
    :input iterable: an iterable
    :input chunksize: chunksize
    """
    for i in range(0, len(iterable), chunksize):
        yield iterable[i:i + chunksize]
    
def expand(link, timeout=2, dscriptive=False, **kwargs):
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
        url_long = r.url
        domain = get_domain(url_long)

    except requests.exceptions.RequestException as e:
        domain, url_long = _parse_error(str(e))
                   
    if domain == 'ln.is':
        url_long = link.replace('ln.is/', '')
        domain = get_domain(url_long)
        
    if domain in constants.short_domain_ad_redirects:
        url_long = unshortenit.UnshortenIt().unshorten(link,
                                                       timeout=timeout)
        domain = get_domain(url_long)

    return dict(original_url=link,
                resolved_domain=domain,
                resolved_url=url_long)


def multithread_expand(links_to_unshorten, chunksize=1280, n_workers=64, 
                       cache_file=None, random_seed=303, 
                       return_errors=True, **kwargs):
    '''
    Calls unshorten_3 with multiple (n_workers) threads to unshorten a list of urls.
    
    :param links_to_unshorten: (list) a list of urls (str) to unshorten
    :param chunksize: (int) chunks links_to_unshorten, which makes computation quicker with larger inputs
    :param n_workers: (int) how many threads
    :param cache_file: (str) a path to a json file to read and write results in
    :param random_seed: (int) initializes the random state for shuffling the input
    :param return_errors: (bool) whether to return a tuple of dataframe of shortened link, and dict of errors
        or just the dataframe of shortened links
        
    
    :returns: (DataFrame) a dataframe unshorted domains, long, and original URLs.
    '''
    
    # shuffle the inputs, this is to reduce the changes of making requests to the same domain.
    np.random.seed(random_seed)
    np.random.shuffle(links_to_unshorten)

    # read cache file
    out = []
    if cache_file and os.path.exists(cache_file):
        with open(cache_file, 'r') as f_:
            for line in f_:
                out.append(json.loads(line))
            # which urls are already in the temp file?
            abd_ = [_['original_url'] for _ in out]
            # which urls are in the temp file AND we want to unshorten
            out = [link for link in out if link['original_url'] in links_to_unshorten]
            # which links do we have left?
            links_to_unshorten = [link for link in links_to_unshorten if link not in abd_]
    
    # chunk the list of arguments
    for chunk in tqdm(_chunks(links_to_unshorten, chunksize=chunksize)):
        # create n_workers threads, and map chunked argumnets to them
        with concurrent.futures.ThreadPoolExecutor(max_workers = n_workers) as executor:
            future_to_url = {executor.submit(expand, url, **kwargs): 
                             url for url in chunk}
            for i, future in enumerate(concurrent.futures.as_completed(future_to_url)):
                try:
                    data = future.result()
                except Exception as exc:
                    data = str(type(exc))
                finally:
                    out.append(data)
                    
                    # save the results
                    if cache_file and isinstance(data, dict):
                        with open(cache_file, 'a') as f_:
                            f_.write(json.dumps(data) + '\n')
                       
    # how many instances failed?
    error = [{i: _} for i, _ in enumerate(out) if not isinstance(_, dict)]
    
    # read the rest to a dataframe
    results = [row for row in out if isinstance(row, dict)]
    
    if return_errors:
        return results, error
    else:
        return results
    

def count_matrix(df, user_col='user.id', domain_col='link.domain', 
                 unique_count_col='tweet.id', domain_list=[]):
    '''
    Creates a count matrix of number of domains shared per user. 
    Where each column is a count of domains, and each row represents on user.
    
    
    :input df: (pandas dataframe) an un-aggregrated dataframe of links shared by user.
    :input user_col: (str) the name of the column in input dataframe to aggragate on. 
            Feeds into the index argument in `pd.pivot_table`.
    :inout domain_col: (str) the name of the column in the input dataframe to count.
            Feeds into the columns argument in `pd.pivot_table`.
    :input count_unique_col: (str) the name of the column to count unique values amongst domain_col.
    :input domain_list: (list) a list of normalized domains to create the count matrix on.
    
    :returns: matrix (pandas dataframe) counts per domain by user.
    '''
    # check the correct columns are present
    for col in [user_col, domain_col, unique_count_col]:
        try:
            assert(col in df.columns)
        except:
            raise ValueError(f"{col} is not a column in the input dataframe")
    
    # what are all the domains available?
    all_domains = df[domain_col].unique()    
    
    # create a count matrix
    matrix = df.pivot_table(index=user_col, 
                            columns=[domain_col],
                            values=[unique_count_col],
                            aggfunc=lambda x: len(x.unique()),
                            fill_value=0)
    
    # standardize the column names, and remove any hierarchys for readability.
    matrix = matrix.T.reset_index(level=0, drop=True).T
    matrix.columns.name = None
    
    # filter out columns not included in domain_list
    if domain_list:
        matrix = matrix[[c for c in all_domains if c in domain_list]]
    
    return matrix
