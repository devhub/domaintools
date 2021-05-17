# -*- coding: utf-8 -*-
'''\
:mod:`domaintools` -- Domain name parsing tools
===============================================

.. moduleauthor:: Mark Lee <markl@evomediagroup.com>
.. moduleauthor:: Gerald Thibault <jt@evomediagroup.com>
'''
import logging
import re
from urlparse import urlparse

from tldextract import extract, TLDExtract

from .utils import cached_property, normalize_domain


logging.basicConfig()
logger = logging.getLogger(__name__)

extract_private = TLDExtract('.private', include_psl_private_domains=True)

DOMAIN_PART_REGEX = re.compile(ur'(?!-)[A-Z\d-]{1,63}(?<!-)$', re.IGNORECASE)


class Domain(object):
    '''Handles parsing domains. All domain names are canonicalized 
        via lowercasing and conversion to punycode. __unicode__ will
        return the decoded version

    TODO make sure it's compliant with http://tools.ietf.org/html/rfc1035

    :param domain_string: the domain name to parse.
    :type domain_string: bytes or text
    '''

    def __init__(self, domain_string, allow_private=False):
        self.allow_private = allow_private
        self.__private = False
        self.error = False
        try:
            self.text = normalize_domain(domain_string)
            self.labels = [x.encode('idna') for x in self.text.split('.')]
        except UnicodeError:
            self.error = True

    @cached_property
    def parsed(self):
        if self.error:
            return None
        e = extract(self.text)
        if self.allow_private:
            e2 = extract_private(self.text)
            if e2 != e:
                e = e2
                self.__private = True    
        return e

    @property
    def domain(self):
        '''The full domain name (second level domain + top level domain)

        :rtype: bytes, or None if the domain name is invalid.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.domain
        b'brokerdaze.co.uk'
        '''
        if self.valid:
            return b'%s.%s' % (self.sld, self.tld)

    @property
    def tld(self):
        '''The top level domain (TLD) (i.e., co.uk).

        :rtype: bytes, or None if the TLD is invalid.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.tld
        b'co.uk'
        '''
        if self.parsed and self.parsed.suffix:
            return self.parsed.suffix.encode('idna')

    @property
    def sld(self):
        '''The second level domain (SLD).

        :rtype: bytes, or None if the SLD does not exist.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.sld
        b'brokerdaze'
        '''
        if self.parsed and self.parsed.domain:
            return self.parsed.domain.encode('idna')

    @property
    def subdomain(self):
        '''The subdomain (i.e., www).

        :rtype: bytes, or None if the subdomain does not exist.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.subdomain
        b'www'
        '''
        if self.parsed and self.parsed.subdomain:
            return self.parsed.subdomain.encode('idna')

    @cached_property
    def valid(self):
        '''Determines if the domain is valid.

        :returns: True if valid, False otherwise.
        :rtype: bool

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.valid
        True
        >>> d = Domain(u'foo')
        >>> d.valid
        False
        '''
        if not self.valid_host:
            return False
        if self.labels[0] == '*':
            # wildcard pattern
            return False
        return True

    @cached_property
    def valid_host(self):
        '''Determines if the host is valid.

        :returns: True if valid, False otherwise.
        :rtype: bool

        >>> d = Domain(u'*.brokerdaze.co.uk')
        >>> d.valid
        False
        >>> d.valid_host
        True
        '''
        if self.tld is None or self.sld is None:
            return False
        if len(self.text) > 253:
            return False
        for i, part in enumerate(self.labels):
            if part == '*' and i == 0:
                # wildcard pattern
                continue
            if DOMAIN_PART_REGEX.match(part) is None:
                return False
        return True

    @cached_property
    def private(self):
        if self.tld is None:
            return False
        return self.__private

    def __repr__(self):
        '''Generates a representation of the object, with the domain as an
        ASCII string.

        >>> Domain(u'www.brokerdaze.co.uk')
        <Domain: www.brokerdaze.co.uk>
        '''
        return '<%s: %s>' % (self.__class__.__name__, self.__str__())

    def __unicode__(self):
        '''Returns the full domain name. Any punycode is converted.

        >>> unicode(Domain('www.brokerdaze.co.uk'))
        u'www.brokerdaze.co.uk'
        '''
        return self.text

    def __str__(self):
        '''Returns the full domain name, in punycode (if necessary).

        >>> str(Domain(u'www.brokerdaze.рф'))
        b'www.brokerdaze.xn--p1ai'
        >>> str(Domain(b'www.brokerdaze.xn--p1ai'))
        b'www.brokerdaze.xn--p1ai'
        '''
        return self.text.encode('idna')
    __bytes__ = __str__

    try:
        unicode
    except NameError:
        # python3
        __str__ = __unicode__

    def __eq__(self, other):
        '''Ensures that two ``Domain`` objects with the same domain name are
        equivalent.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d == Domain(u'www.brokerdaze.co.uk')
        True
        >>> d == Domain(u'www2.brokerdaze.co.uk')
        False
        '''
        return self.tld == other.tld and self.sld == other.sld and \
               self.subdomain == other.subdomain

    def __ne__(self, other):
        '''Ensures that two ``Domain`` objects with different domain names
        are not equivalent.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d != Domain(u'www.brokerdaze.co.uk')
        False
        >>> d != Domain(u'www2.brokerdaze.co.uk')
        True
        '''
        return not self.__eq__(other)
