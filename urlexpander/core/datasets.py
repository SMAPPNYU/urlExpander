import pandas as pd

from urlexpander.core import constants

__all__ = ['congress_twitter_links']
__author__= 'Leon Yin'

def congress_twitter_links():
    '''
    Returns a Pandas dataframe of a random sample of 50K 
    URLs parsed from Twitter aaccounts from the 115th congress.
    
    URLs are parsed using `tweet_parser.get_link`.
    
    columns = {
      'link.domain' : 'the domain of the URL', 
      'link.url_long' : 'the URL (this can be short!)', 
      'link.url_short' : 'The t.co URL', 
      'tweet.created_at' : 'When the tweet was created', 
      'tweet.id' : 'The ID of the tweet', 
      'tweet.text' : 'The Full text of the tweet', 
      'user.id' : 'The Twitter ID of the tweeter'
    }
    
    :returns: (df) of Tweets with cols 
    '''
    df_congress = pd.read_csv(constants.congress_dataset_url,
                              dtype={'tweet.id':str,'user.id':str})
    return df_congress