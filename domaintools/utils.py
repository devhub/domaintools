from six import binary_type


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


def normalize_domain(domain_string):
    '''Normalize a domain to text '''
    if isinstance(domain_string, binary_type):
        # convert bytes to text
        domain_string = domain_string.decode('utf8')
    # strip out port numbers
    domain_string, _, _ = domain_string.partition(u':')
    # idna decode
    domain_string = domain_string.lower().encode('idna').decode('idna')
    return domain_string
