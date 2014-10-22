# encoding: utf8
import unittest

from . import Domain


# input, tld, sld, subdomain, private
valid_domains = [
    # gtld
    (u'goat.com', 'com', 'goat', None, False),
    # gtld with subdomain
    (u'www.goat.com', 'com', 'goat', 'www', False),
    # gtld with unicode subdomain
    (u'рф.goat.com', 'com', 'goat', 'xn--p1ai', False),
    # gtld with idna subdomain
    (u'xn--p1ai.goat.com', 'com', 'goat', 'xn--p1ai', False),
    # cctld 
    (u'goat.ca', 'ca', 'goat', None, False),
    # 2-piece cctld 
    (u'goat.co.uk', 'co.uk', 'goat', None, False),
    # 2-piece cctld with subdomain
    (u'www.goat.co.uk', 'co.uk', 'goat', 'www', False),
    # private tld
    (u'uk.com', 'com', 'uk', None, False),
    # private tld
    (u'goat.uk.com', 'com', 'uk', 'goat', False),
    # private tld with subdomain
    (u'www.goat.uk.com', 'com', 'uk', 'www.goat', False),
    # unicode tld
    (u'goat.рф', 'xn--p1ai', 'goat', None, False),
    # idna tld
    (u'goat.xn--p1ai', 'xn--p1ai', 'goat', None, False),
    # unicode tld and sld
    (u'рф.рф', 'xn--p1ai', 'xn--p1ai', None, False),
    # unicode tld and sld with subdomain
    (u'www.рф.рф', 'xn--p1ai', 'xn--p1ai', 'www', False),
    # unicode tld, sld, and subdomain
    (u'рф.рф.рф', 'xn--p1ai', 'xn--p1ai', 'xn--p1ai', False),
    # unicode sld with gtld
    (u'рф.com', 'com', 'xn--p1ai', None, False),
    # new gtld
    (u'goat.wtf', 'wtf', 'goat', None, False),
    # wildcard
    (u'goat.com.bn', 'com.bn', 'goat', None, False),
    ]

valid_private_domains = [
    # private tld
    (u'goat.uk.com', 'uk.com', 'goat', None, True),
    # private tld with subdomain
    (u'www.goat.uk.com', 'uk.com', 'goat', 'www', True),
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
    u'goat.bn',
    # test-period unicode tld (no longer in use)
    u'test.テスト',
    # incorrect formatting
    u'.goat.com',
    ]

invalid_private_domains = [
    # valid 2-piece tld with no sld
    u'co.uk',
    # valid private tld with no sld
    u'uk.com',
    ]

class TestDomainTools(unittest.TestCase):

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
