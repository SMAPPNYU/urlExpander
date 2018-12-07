'''These are variables that are useful to reference.
There are several curated lists of link shortening domains,
the url of datasets for tutorials.
'''

__author__= 'Leon Yin'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

# these domains need a redirect (Leon Yin + UnshortenIT 2018)
short_domain_ad_redirects = [
    'sh.st',  'adf.ly', 'lnx.lu',
    'adfoc.us', 'j.gs','q.gs',
    'u.bb', 'ay.gy', 'atominik.com',
    'tinyium.com', 'microify.com', 'linkbucks.com',
    'www.linkbucks.com', 'jzrputtbut.net', 'any.gs',
    'cash4links.co', 'cache4files.co', 'dyo.gs',
    'filesonthe.net', 'goneviral.com', 'megaline.co',
    'miniurls.co', 'qqc.co', 'seriousdeals.net',
    'theseblogs.com', 'theseforums.com',
    'tinylinks.co', 'tubeviral.com', 'ultrafiles.net',
    'urlbeat.net', 'whackyvidz.com','yyv.co',
    'href.li', 'anonymz.com', 'festyy.com', 
    'ceesty.com', 'tiny.cc'
]

# these are standard domain shorteners (Leon Yin 2018)
short_domain = [
    'dlvr.it', 'bit.ly', 'buff.ly',
    'ow.ly',  'goo.gl', 'shar.es', 
    'ift.tt', 'fb.me',  'washex.am', 
    'smq.tc',  'trib.al', 'is.gd',
    'paper.li', 'waa.ai', 'tinyurl.com',
    'ht.ly', '1.usa.gov', 'deck.ly',
    'bit.do', 'lc.chat', 'urls.tn',
    'soo.gd',  's2r.co', 'clicky.me',
    'budurl.com', 'bc.vc', 'branch.io',
    'capsulink.com', 'ux9.de', 'fuck.it',
    't2m.io', 'shrt.li', 'elbo.in',
    'shrtfly.com', 'hiveam.com',
    'slink.be', 'plu.sh', 'cutt.ly',
    'zii.bz', 'munj.pw', 't.co',
    'go.usa.gov', 'on.fb.me', 'j.mp',
    'amp.twimg.com', 'ofa.bo',
]

# there are domain shorteners for common news outlets (Leon Yin 2018).
short_domain_media = [
    'on.rt.com', 'wapo.st', 'hill.cm', 
    'dailym.ai', 'cnn.it', 'nyti.ms',
    'politi.co', 'fxn.ws', 'usat.ly', 
    'huff.to', 'nyp.st', 'cbsloc.al',
    'wpo.st', 'on.wsj.com', 'nydn.us',
    'on.wsj.com',
]

# there are link shorteners with the actual link appended on the end
url_appenders = ['ln.is', 'linkis.com']

all_short_domains = short_domain_ad_redirects + short_domain + url_appenders

congress_dataset_url = ('https://raw.githubusercontent.com/SMAPPNYU/'
                        'urlExpander/master/datasets/'
                        'congress_sample_links.csv')

us_nation_domain_url = ('https://raw.githubusercontent.com/SMAPPNYU/'                                                                   'urlExpander/master/datasets/'
                        'us_national_domains.csv')