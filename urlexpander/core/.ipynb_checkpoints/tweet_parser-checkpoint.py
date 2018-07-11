from urlexpander.core.api import get_domain

__all__ = ['get_link']

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