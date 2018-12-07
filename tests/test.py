import os
import sys
import requests
import unittest
import datetime
import collections

sys.path.append(os.path.abspath('../')) 
import urlexpander

__author__ = 'Leon Yin'

class expand(unittest.TestCase):
    '''
    This is a simple test to make sure the urlexpander's core function works for a single link, and a list of links. If these bitlinks dissappear, the tests will fail. So it may be smart to change these every quarter.
    '''
    @classmethod
    def setUpClass(cls):
        cls.urls = [
            'https://trib.al/xXI5ruM',
            'http://bit.ly/1Sv81cj',
            'https://www.youtube.com/watch?v=8NwKcfXvGl4',
            'https://t.co/zNU1eHhQRn',
        ]
        
        cls.resolved_urls = [
            'https://www.breitbart.com/video/2017/12/31/lindsey-graham-trump-just-cant-tweet-iran/',
            'http://www.billshusterforcongress.com/congressman-shuster-endorses-donald-trump/',
            'https://www.youtube.com/watch?v=8NwKcfXvGl4',
            'http://www.nfib.com/content/press-release/elections/small-business-endorses-shuster-for-reelection-73730/?utm_campaign=Advocacy&utm_source=Twitter&utm_medium=Social'
        ]
        
    def test_expand_one(self):
        self.assertEqual(self.resolved_urls[0],
                         urlexpander.expand(self.urls[0]))
    
    def test_expand_many(self):
        self.assertEqual(self.resolved_urls, 
                        urlexpander.expand(self.urls))

    def test_cacheing(self):
        self.assertEqual(self.resolved_urls, 
                        urlexpander.expand(self.urls, cache_file='__cache.json'))
        self.assertEqual(self.resolved_urls, 
                        urlexpander.expand(self.urls, cache_file='__cache.json'))
        os.remove('__cache.json')
    
    def test_cacheing(self):
        self.assertEqual(self.resolved_urls, 
                        urlexpander.expand(self.urls, cache_file='__cache.json'))
        
if __name__ == '__main__':
    unittest.main()