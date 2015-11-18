# -*- coding: utf-8 -*-
'''\
:mod:`domaintools` -- Domain name parsing tools
===============================================

.. moduleauthor:: Mark Lee <markl@evomediagroup.com>
.. moduleauthor:: Gerald Thibault <jt@evomediagroup.com>
'''
import dns.resolver
import dns.query
import logging
import re
from urlparse import urlparse
try:
    from .data import TLDS
except:
    TLDS = None


logging.basicConfig()
logger = logging.getLogger(__name__)

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
    '''Handles parsing domains. All domain names are canonicalized 
        via lowercasing and conversion to punycode. __unicode__ will
        return the decoded version

    TODO make sure it's compliant with http://tools.ietf.org/html/rfc1035

    :param domain_string: the domain name to parse.
    :type domain_string: unicode
    '''
    __whitespace_regex = re.compile(ur'\s+')

    __domain_part_regex = re.compile(ur'^[a-zA-Z0-9\*]([a-zA-Z0-9\-]*[a-zA-Z0-9]){0,62}')

    def __init__(self, domain_string, allow_private=False):
        if not TLDS:
            raise Exception('TLDs could not be loaded from data.py. To create '
                'the file, run build_data_file.py') 
        if u':' in domain_string:
            # strip out port numbers
            domain_string, port = domain_string.rsplit(u':', 1)
        self.allow_private = allow_private
        self.__private = False
        try:
            self.__full_domain = domain_string.lower().encode('idna')
        except:
            self.__full_domain = domain_string.lower()
        self.__domain_parts = self.__full_domain.split('.')
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
            return '%s.%s' % (self.sld, self.tld)
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
            dots = tld.count('.')
            if dots == len(self.__domain_parts) - 1:
                return None
            result = self.__domain_parts[-2-dots]
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
            dots = tld.count('.')
            if dots == len(self.__domain_parts) - 2:
                return None
            result = '.'.join(self.__domain_parts[:-2-dots])
        return result

    @cached_property
    def tld(self):
        '''The top level domain (TLD) (i.e., co.uk).

        :rtype: unicode, or None if the TLD is invalid.

        >>> d = Domain(u'www.brokerdaze.co.uk')
        >>> d.tld
        u'co.uk'
        '''
        logger.info('Parsing TLD for domain: %s' % self.__full_domain)
        result = None
        if len(self.__domain_parts) == 1:
            logger.info('  Ignoring (too short)')
            return result
        tld = self.__domain_parts[-1]
        if tld in TLDS:
            choices = TLDS[tld]
            for i in range(len(self.__domain_parts)):
                _parts = self.__domain_parts[-1-i:]
                check = '.'.join(_parts)
                logger.info('  Checking %s' % check)
                if check in choices:
                    logger.info('    Found match')  
                    # found a match, first check if it's private
                    self.__private = choices[check]
                    if self.__private:
                        logger.info('     -Private')
                        if not self.allow_private:
                            # ignore this and return the true tld
                            self.__private = False
                            logger.info('     -Ignoring (allow_private=False)')
                            break
                    # valid match, store it and try for a longer match
                    result = check                
                    continue

                if i == 0:
                    # do not try wildcard matches on single components
                    continue
                # check for wildcard
                check2 = '.'.join(['*'] + _parts[1:])
                logger.info('  Checking %s' % check2)
                if check2 in choices:
                    # wildcard found in choices, the tested tld is valid
                    logger.info('    Found match')  
                    result = check
                if result:
                    break
        else:
            # no match, assume it's a valid TLD not present in the dat file
            # try an SOA check to make sure it exists
            logger.info('  Not found in TLD list. Trying SOA check')
            try:
                answers = dns.resolver.query(qname = dns.name.from_text(tld),
                                             rdtype='soa')
                assert answers
                logger.info('    SOA record found, assuming valid')
                result = tld
            except Exception as e:
                # SOA not found
                logging.info('    SOA record not found, assuming invalid')
                pass
        logger.info('  Returning effective TLD: %s' % result)
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
        if self.tld is None or self.sld is None or '' in self.__domain_parts:
            return False
        for part in self.__domain_parts:
            if len(part) > 63:
                return False
            if part[-1] == '-':
                return False
            if part[0] == '*' and len(part) > 1:
                return False
            if self.__domain_part_regex.match(part) is None:
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
        return self.__full_domain.decode('idna')

    def __str__(self):
        u'''Returns the full domain name, in punycode (if necessary).

        >>> str(Domain(u'www.brokerdaze.рф'))
        'www.brokerdaze.xn--p1ai'
        >>> str(Domain('www.brokerdaze.xn--p1ai'))
        'www.brokerdaze.xn--p1ai'
        '''
        return self.__full_domain

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

