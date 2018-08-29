import os
import sys
import requests
import unittest
import datetime
import collections

sys.path.append(os.path.abspath('../')) 
import urlexpander

class expand(unittest.TestCase):
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

        
if __name__ == '__main__':
    unittest.main()