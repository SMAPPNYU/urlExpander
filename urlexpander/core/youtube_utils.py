__all__ = ['strip_yt_link']

def _strip_yt_link(link):
    '''
    Parses a link to youtube to get the screen name and tweet id
    
    :input link: a link with the domain 'youtube.com' or 'youtu.be'
    :returns: a list of dictionaries with the original link, the video id, or the channel id
    '''
   
    dict_ = {}
    dict_['resolved_url'] = link
        

    if 'v=' in link:
        vid = link[link.index('v='):].strip('v=')
        if len(vid) > 11:
            vid = vid[:11]
        channel = None
    elif 'channel' in link:
        channel = link[link.index('channel'):].strip('channel/')
        if len(channel) > 24:
            channel = channel[:24]
        vid = None
    elif 'youtu.be' in link:
        vid = link.replace('https://', '').replace('http://', '').replace('youtu.be','').strip('/').strip('?a')
        channel = None
    else:
        vid = None
        channel = None
        
    dict_['video_id'] = vid
    dict_['channel'] = channel
    
    return dict_

def strip_yt_link(link):
    '''
    Parses a link to twitter to get the screen name and tweet id
    
    :input link: a link or list of links with the domain 'youtube.com' or 'youtu.be'
    :returns: a list of dictionaries with the original link, the video id, or the channel id
    '''
    
    if isinstance(link, str):
        return _strip_yt_link(link)
    
    elif isinstance(link, list):
        links_to_strip = list(set(link))
        links = [_strip_yt_link(link) for link in links_to_strip]
        return links
    
    else:
        links_to_strip = list(set(list(link)))
        links = [_strip_yt_link(link) for link in links_to_strip]
        return links
