# encoding: utf8
import unittest

from . import Domain


# input, tld, sld, subdomain, private
valid_domains = [
    # gtld
    (u'goat.com', b'com', b'goat', None, False),
    # gtld with subdomain
    (u'www.goat.com', b'com', b'goat', b'www', False),
    # gtld with unicode subdomain
    (u'рф.goat.com', b'com', b'goat', b'xn--p1ai', False),
    # gtld with idna subdomain
    (u'xn--p1ai.goat.com', b'com', b'goat', b'xn--p1ai', False),
    # cctld 
    (u'goat.ca', b'ca', b'goat', None, False),
    # 2-piece cctld 
    (u'goat.co.uk', b'co.uk', b'goat', None, False),
    # 2-piece cctld with subdomain
    (u'www.goat.co.uk', b'co.uk', b'goat', b'www', False),
    # private tld
    (u'uk.com', b'com', b'uk', None, False),
    # private tld
    (u'goat.uk.com', b'com', b'uk', b'goat', False),
    # private tld with subdomain
    (u'www.goat.uk.com', b'com', b'uk', b'www.goat', False),
    # unicode tld
    (u'goat.рф', b'xn--p1ai', b'goat', None, False),
    # idna tld
    (u'goat.xn--p1ai', b'xn--p1ai', b'goat', None, False),
    # unicode tld and sld
    (u'рф.рф', b'xn--p1ai', b'xn--p1ai', None, False),
    # unicode tld and sld with subdomain
    (u'www.рф.рф', b'xn--p1ai', b'xn--p1ai', b'www', False),
    # unicode tld, sld, and subdomain
    (u'рф.рф.рф', b'xn--p1ai', b'xn--p1ai', b'xn--p1ai', False),
    # unicode sld with gtld
    (u'рф.com', b'com', b'xn--p1ai', None, False),
    # new gtld
    (u'goat.wtf', b'wtf', b'goat', None, False),
    # wildcard
    (u'goat.com.bn', b'com.bn', b'goat', None, False),
]

valid_private_domains = [
    # private tld
    (u'goat.uk.com', b'uk.com', b'goat', None, True),
    # private tld with subdomain
    (u'www.goat.uk.com', b'uk.com', b'goat', b'www', True),
]

invalid_domains = [
    # invalid tld with no sld
    u'goat',
    # invalid tld with sld
    u'sub.goat',
    # invalid unicode tld with no sld
    u'gфat',
    # invalid unicode tld with sld
    u'sub.gфat',
    # invalid idna tld with no sld
    u'xn--gat-hfd',
    # invalid idna tld with sld
    u'sub.xn--gat-hfd',
    # valid tld with no sld
    u'com',
    # wildcard sld value
    u'goat.bd',
    # test-period unicode tld (no longer in use)
    u'test.テスト',
    # incorrect formatting
    u'.goat.com',
    # include ,
    u',.google.com',
    # start with -
    u'-a.google.com',
    # end with -
    u'a-.google.com',
    # include *
    u'*a.google.com',
    # consecutive dots
    u'www..google.com',
    # long component
    u'%s.google.com' % (u'a'*64),
]

invalid_private_domains = [
    # valid 2-piece tld with no sld
    u'co.uk',
    # valid private tld with no sld
    u'uk.com',
]


class TestDomainTools(unittest.TestCase):

    def test_wildcard_parsing(self):
        ''' wildcard domains should yield a valid host and invalid domain '''
        domain_name = u'*.google.com'
        domain = Domain(domain_name)
        self.assertEqual(b'com', domain.tld)
        self.assertEqual(b'google', domain.sld)
        self.assertEqual(b'*', domain.subdomain)
        self.assertFalse(domain.valid)
        self.assertTrue(domain.valid_host)

    def test_valid_domain_parsing(self):
        for domain_name, tld, sld, subdomain, private in valid_domains:
            domain = Domain(domain_name)
            self.assertTrue(domain.valid)
            self.assertTrue(domain.tld == tld)
            self.assertTrue(domain.sld == sld)
            self.assertTrue(domain.subdomain == subdomain)
            self.assertTrue(domain.private == private)

    def test_private_domain_parsing(self):
        for domain_name, tld, sld, subdomain, private in valid_private_domains:
            domain = Domain(domain_name, allow_private=True)
            self.assertTrue(domain.valid)
            self.assertTrue(domain.tld == tld)
            self.assertTrue(domain.sld == sld)
            self.assertTrue(domain.subdomain == subdomain)
            self.assertTrue(domain.private == private)

    def test_invalid_domain_parsing(self):
        for domain_name in invalid_domains:
            domain = Domain(domain_name)
            self.assertFalse(domain.valid)

    def test_invalid_private_domain_parsing(self):
        for domain_name in invalid_private_domains:
            domain = Domain(domain_name, allow_private=True)
            self.assertFalse(domain.valid)

    
if __name__ == '__main__':
    unittest.main()
