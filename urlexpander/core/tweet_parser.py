"""This module has utility functions for parsing links from Tweets.
Check out the smappdragon package for Tweet parsing.
https://github.com/SMAPPNYU/smappdragon
"""

from urlexpander.core.api import get_domain

__all__ = ['get_link']
__author__= 'Leon Yin'

def _get_full_text(tweet):
    '''
    Parses a tweet json to retrieve the full text.
    
    :input tweet: a nested dictionary of a Tweet either from the streaming or search API.
    :returns: string of the full_text field hidden in the Tweet
    '''
    if "extended_tweet" in tweet and "full_text" in tweet["extended_tweet"]:
        return tweet["extended_tweet"]["full_text"]
    try:
        return tweet["text"]
    except:
        return tweet['full_text']
    
def get_link(tweet):
    '''
    Returns a generator containing tweet metadata about media.
    
    The metadata dict contains the following columns:
    
    columns = {
      'link.domain' : 'the domain of the URL', 
      'link.url_long' : 'the URL (this can be short!)', 
      'link.url_short' : 'The t.co URL', 
      'tweet.created_at' : 'When the tweet was created', 
      'tweet.id' : 'The ID of the tweet', 
      'tweet.text' : 'The Full text of the tweet', 
      'user.id' : 'The Twitter ID of the tweeter'
    }
    
    :input tweet: a nested dictionary of a Tweet either from the streaming or search API.
    :returns: a generator of dictionaries
    '''
    if not isinstance(tweet, dict):
        return
    
    row = {
        'user.id': tweet['user']['id'],
        'tweet.id': tweet['id'],
        'tweet.created_at': tweet['created_at'],
        'tweet.text' : _get_full_text(tweet)
    }

    list_urls = tweet['entities']['urls']
    
    if list_urls:
        for url in list_urls:
            r = row.copy()
            r['link.url_long'] = url.get('expanded_url')
            
            if r['link.url_long']:
                r['link.domain'] = get_domain(r['link.url_long'])
                r['link.url_short'] = url.get('url')

                yield r  
                