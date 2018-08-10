"""This module has utility functions for parsing links from Tweets.
Check out the smappdragon package for Tweet parsing.
https://github.com/SMAPPNYU/smappdragon
"""

from urlexpander.core.api import get_domain

__all__ = ['get_link', 'count_matrix', 'strip_tweet_link']
__author__= 'Leon Yin'

def _get_full_text(tweet):
    '''
    Parses a tweet json to retrieve the full text.
    
    :input tweet: a nested dictionary of a Tweet either from the streaming or search API.
    :returns: string of the full_text field hidden in the Tweet
    '''
    if isinstance(tweet, dict):
        if "extended_tweet" in tweet and "full_text" in tweet["extended_tweet"]:
            return tweet["extended_tweet"]["full_text"]
        elif "full_text" in tweet:
            tweet['full_text']
        else:
            return tweet.get("text")
    else:
        dtype = type(tweet)
        raise ValueError("Input needs to be key-value pair! Input is {}".format(dtype))
    
def get_link(tweet):
    '''
    Returns a generator containing tweet metadata about media.
    
    The metadata dict contains the following columns:
    
    columns = {
      'link_domain' : 'the domain of the URL', 
      'link_url_long' : 'the URL (this can be short!)', 
      'link_url_short' : 'The t.co URL', 
      'tweet_created_at' : 'When the tweet was created', 
      'tweet_id' : 'The ID of the tweet', 
      'tweet_text' : 'The Full text of the tweet', 
      'user_id' : 'The Twitter ID of the tweeter'
    }
    
    :input tweet: a nested dictionary of a Tweet either from the streaming or search API.
    :returns: a generator of dictionaries
    '''
    if not isinstance(tweet, dict):
        return
    
    try: 
        row = {
            'user_id': tweet['user']['id'],
            'tweet_id': tweet['id'],
            'tweet_created_at': tweet['created_at'],
            'tweet_text' : _get_full_text(tweet)
        }
    except:
        return

    list_urls = tweet['entities']['urls']
    
    if list_urls:
        for url in list_urls:
            r = row.copy()
            r['link_url_long'] = url.get('expanded_url')
            
            if r['link_url_long']:
                r['link_domain'] = get_domain(r['link_url_long'])
                r['link_url_short'] = url.get('url')

                yield r
  

                
def count_matrix(df, user_col='user_id', domain_col='link_domain', 
                 unique_count_col='tweet_id', domain_list=[]):
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

def _strip_tweet_link(link):
    '''
    Best attempt at stripping twitter links for screen names and tweet ids.
    
    :input link: a link with the domain 'twitter.com'
    :returns: a list of dictionaries with the original link, the screen name, and the tweet_id of the link
    '''
    dict_ = {}
    
    dict_['resolved_url'] = link.lower()
    if 'status' in link.split('/'):
        list_ = link.lower().split('/')
        try:
            if 'i/web/status' in link: dict_['linked_screen_name'] == None
            else: dict_['linked_screen_name'] = list_[list_.index('status') - 1]
            dict_['linked_tweet_id'] = list_[list_.index('status') + 1]
        except:
            dict_['linked_screen_name'] = None
            dict_['linked_tweet_id'] = None
    
    else:
        dict_['linked_screen_name'] = link
        dict_['linked_tweet_id'] = link
    
    return dict_

def strip_tweet_link(link):
    '''
    Parses a link to twitter to get the screen name and tweet id
    
    :input link: a link or list of links with the domain 'twitter.com'
    :returns: a list of dictionaries with the original link, the screen name, and the tweet_id of the link
    '''
    
    if isinstance(link, str):
        return _strip_tweet_link(link)
    elif isinstance(link, list):
        links_to_strip = list(set(link))
        links = [_strip_tweet_link(link) for link in links_to_strip]
        return links
    else:
        links_to_strip = list(set(list(link)))
        links = [_strip_tweet_link(link) for link in links_to_strip]
        return links
