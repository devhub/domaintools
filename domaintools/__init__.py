# -*- coding: utf-8 -*-
'''\
:mod:`domaintools` -- Domain name parsing tools
===============================================

.. moduleauthor:: Mark Lee <markl@evomediagroup.com>
'''

import re
from urlparse import urlparse
from data import (
    cctlds, cctld_slds, fake_tlds, no_custom_slds, some_custom_slds, tlds)


def cached_property(f):
    '''Decorator which caches property values.

    :param f: The function to decorate.
    :type f: function
    :returns: The wrapper function.
    '''

    def cached(self):
        prop = '__%s' % f.__name__
        if hasattr(self, prop):
            result = getattr(self, prop)
        else:
            result = f(self)
            setattr(self, prop, result)
        return result
    # needed so that doctests are properly discovered
    cached.__doc__ = f.__doc__
    return property(cached)


class Domain(object):
    '''Handles parsing domains. Does not currently handle IDN. All domain names
    are canonicalized via lowercasing.

    TODO make sure it's compliant with http://tools.ietf.org/html/rfc1035

    :param domain_string: the domain name to parse.
    :type domain_string: unicode
    '''

    # Per http://en.wikipedia.org/wiki/Domain_name#Allowed_character_set
    __valid_chars = re.compile(ur'^[a-z0-9.-]+$')
    __whitespace_regex = re.compile(ur'\s+')

    def __init__(self, domain_string, decode_idna=False):
        if u':' in domain_string:
            # strip out port numbers
            domain_string, port = domain_string.rsplit(u':', 1)
        if decode_idna and 'xn--' in domain_string:
            # convert to IDN
            domain_string = domain_string.decode('idna')
        self.__full_domain = domain_string.lower()
        self.__domain_parts = self.__full_domain.split(u'.')
        if self.__domain_parts[-1] == u'':
            self.__domain_parts.pop()

    @cached_property
    def domain(self):
        '''The full domain name (second level domain + top level domain)

        :rtype: unicode, or None if the domain name is invalid.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.domain
        u'brokerdaze.co.uk'
        '''
        if self.valid:
            return u'%s.%s' % (self.sld, self.tld)
        else:
            return None

    @cached_property
    def sld(self):
        '''The second level domain (SLD).

        :rtype: unicode, or None if the SLD does not exist.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.sld
        u'brokerdaze'
        '''
        result = None
        tld = self.tld
        if tld is not None:
            if '.' in tld:
                if len(self.__domain_parts) >= 3:
                    result = self.__domain_parts[-3]
            elif len(self.__domain_parts) >= 2:
                result = self.__domain_parts[-2]
        return result

    @cached_property
    def subdomain(self):
        '''The subdomain (i.e., www).

        :rtype: unicode, or None if the subdomain does not exist.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.subdomain
        u'www'
        '''
        result = None
        tld = self.tld
        if tld is not None:
            if '.' in tld:
                if len(self.__domain_parts) >= 4:
                    result = u'.'.join(self.__domain_parts[:-3])
            elif len(self.__domain_parts) >= 3:
                result = u'.'.join(self.__domain_parts[:-2])
        return result

    @cached_property
    def tld(self):
        '''The top level domain (TLD) (i.e., co.uk).

        :rtype: unicode, or None if the TLD is invalid.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.tld
        u'co.uk'
        '''
        result = None
        tld = self.__domain_parts[-1]
        if tld in fake_tlds and self.__domain_parts[-2] in fake_tlds[tld]:
            result = self.__domain_parts[-2] + '.' + tld
        elif tld in tlds:
            result = tld
        elif tld in cctlds:
            if len(self.__domain_parts) >= 2:
                tld_sld = self.__domain_parts[-2]
                if tld in (no_custom_slds + some_custom_slds) and \
                   tld_sld in cctld_slds[tld]:
                    result = u'%s.%s' % (tld_sld, tld)
                elif tld not in no_custom_slds:
                    result = tld
        return result

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
        result = True
        try:
            if len(self.__domain_parts) < 2 or u'' in self.__domain_parts or \
               self.__valid_chars.match(self.__str__()) is None or \
               '' in self.__domain_parts or self.tld is None or \
               self.sld is None:
                result = False
        except UnicodeError:
            result = False
        return result

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
        return self.__full_domain

    def __str__(self):
        u'''Returns the full domain name, in punycode (if necessary).

        >>> str(Domain(u'www.brokerdaze.рф'))
        'www.brokerdaze.xn--p1ai'
        >>> str(Domain('www.brokerdaze.xn--p1ai'))
        'www.brokerdaze.xn--p1ai'
        '''
        frags = [self.subdomain] if self.subdomain else []
        frags.extend([self.sld.encode('idna'), self.tld.encode('idna')])
        return '.'.join(frags)

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

    @classmethod
    def extract(cls, data):
        '''Extracts domain objects from a string with spaces and line breaks.

        :param data: The data to parse the domain names out of.
        :type data: a unicode string or a file-like object
        :returns: A list of extracted domains.
        :rtype: list

        >>> Domain.extract(u"""www.foo.com notadomain baz.bar.net
        ... quux.something.co.za\\tone.two\\t\\tthree.cc""")
        ... # doctest: +ELLIPSIS
        [<...foo.com>, <...bar.net>, <...something.co.za>, <... three.cc>]
        '''
        result = []

        def parse_string(string):
            for section in re.split(cls.__whitespace_regex, string.strip()):
                if '://' in section:
                    # assume it's a URL instead of a bare domain name
                    url = urlparse(section)
                    if url.hostname is not None:
                        section = url.hostname
                d = Domain(section)
                if d.valid:
                    result.append(d)
        if isinstance(data, unicode):
            parse_string(data)
        elif hasattr(data, '__iter__'):
            for line in data:
                parse_string(line)
        return result
