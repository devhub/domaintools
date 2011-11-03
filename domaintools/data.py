# -*- coding: utf-8 -*-
'''Data relating to parsing domain names.
.. moduleauthor:: Mark Lee <markl@evomediagroup.com>
'''

'''Valid TLDs.'''
tlds = ['aero', 'asia', 'biz', 'cat', 'com', 'coop', 'edu', 'gov', 'info',
        'int', 'jobs', 'mil', 'mobi', 'museum', 'name', 'net', 'org', 'pro',
        'tel', 'travel']
'''Valid ccTLDs.'''
cctlds = ['ac', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'an', 'ao', 'aq',
          'ar', 'as', 'at', 'au', 'aw', 'ax', 'az', 'ba', 'bb', 'bd', 'be',
          'bf', 'bg', 'bh', 'bi', 'bj', 'bm', 'bn', 'bo', 'br', 'bs', 'bt',
          'bv', 'bw', 'by', 'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci',
          'ck', 'cl', 'cm', 'cn', 'co', 'cr', 'cu', 'cv', 'cx', 'cy', 'cz',
          'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ee', 'eg', 'er', 'es',
          'et', 'eu', 'fi', 'fj', 'fk', 'fm', 'fo', 'fr', 'ga', 'gb', 'gd',
          'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 'gr',
          'gs', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'hu', 'id',
          'ie', 'il', 'im', 'in', 'io', 'iq', 'ir', 'is', 'it', 'je', 'jm',
          'jo', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr', 'kw',
          'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu',
          'lv', 'ly', 'ma', 'mc', 'md', 'me', 'mg', 'mh', 'mk', 'ml', 'mm',
          'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx',
          'my', 'mz', 'na', 'nc', 'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np',
          'nr', 'nu', 'nz', 'om', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl',
          'pm', 'pn', 'pr', 'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'rs',
          'ru', 'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sj',
          'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'st', 'su', 'sv', 'sy', 'sz',
          'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to',
          'tp', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug', 'uk', 'us', 'uy',
          'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf', 'ws', 'ye',
          'yt', 'za', 'zm', 'zw', 'ht']
'''Fake TLDs. (users get subdomains instead of valid SLDs)'''
fake_tlds = {
    'com': ['ar', 'br', 'cn', 'de', 'eu', 'gb', 'hu', 'jpn','kr', 'no', 'qc',
            'ru', 'sa', 'se', 'uk', 'us', 'uy', 'za'],
    'net': ['gb', 'se', 'uk'],
    'org': ['ae'],
    }

# IDN ccTLDs.
cctlds += [t.decode('idna') for t in [
    'xn--fiqs8s',  # China (Simplified)
    'xn--fiqz9s',  # China (Traditional)
    'xn--fzc2c9e2c',  # Sri Lanka (Sinhala)
    'xn--j6w193g',  # Hong Kong
    'xn--kprw13d',  # Taiwan (Simplified)
    'xn--kpry57d',  # Taiwan (Traditional)
    'xn--mgbaam7a8h',  # United Arab Emirates
    'xn--mgbayh7gpa',  # Jordan
    'xn--mgberp4a5d4ar',  # Saudi Arabia
    'xn--o3cw4h',  # Thailand
    'xn--p1ai',  # Russian Federation
    'xn--pgbs0dh',  # Tunisia
    'xn--wgbh1c',  # Egypt
    'xn--xkc2al3hye2a',  # Sri Lanka (Tamil)
    'xn--ygbi2ammx',  # Palestinian Territory
]]

'''ccTLDs which do not allow custom SLDs.'''
no_custom_slds = ['au', 'nz', 'uk', 'za']
'''ccTLDs which allow custom SLDs, but also have two-level TLDs.'''
some_custom_slds = ['ae', 'af', 'cn', 'ec', 'es', 'in', 'jp', 'mx', 'ph',
                    'pr', 'pro', 'pt', 'sg', 'tw', 'us']
'''Valid SLDs for ccTLDs which do not allow custom SLDs, or have both schemes.
'''
cctld_slds = {
    # for now, only add the ones we care about.
    # second ae line is "deprecated" SLDs.
    'ae': ['co', 'net', 'org',
           'name', 'pro'],
    'af': ['com', 'net', 'org'],
    # first au line is public slds, second is "community geographic" slds
    'au': ['com', 'net', 'org', 'edu', 'asn', 'id',
           'act', 'nsw', 'nt', 'qld', 'sa', 'tas', 'vlc', 'wa'],
    # first cn line is generic slds, other lines are province slds
    'cn': ['ac', 'com', 'net', 'org',
           'ah', 'bj', 'cq', 'fj', 'gd', 'gs', 'gx', 'gz', 'ha', 'hb', 'he',
           'hi', 'hl', 'hn', 'jl', 'js', 'jx', 'ln', 'nm', 'nx', 'qh', 'sc',
           'sd', 'sh', 'sn', 'sx', 'tj', 'tw', 'xj', 'xz', 'yn', 'zj'],
    'ec': ['com', 'info', 'fin', 'med', 'net', 'org', 'pro'],
    'es': ['com', 'nom', 'org'],
    'in': ['co', 'firm', 'net', 'org', 'gen', 'ind'],
    'jp': ['co', 'gr', 'ne', 'or'],
    'mx': ['com', 'net', 'org'],
    'nz': ['ac', 'co', 'geek', 'gen', 'maori', 'net', 'org', 'school'],
    'ph': ['com', 'i', 'net', 'ngo', 'org'],
    'pr': ['biz', 'com', 'est', 'info', 'isla', 'name', 'net', 'org', 'pro'],
    'pro': ['aaa', 'aca', 'acct', 'avocat', 'bar', 'cpa', 'jur', 'law', 'med',
            'recht'],
    'pt': ['com', 'net', 'nome', 'org', 'publ'],
    'sg': ['com', 'net', 'org', 'per'],
    'tw': ['club', 'com', 'ebiz', 'game', 'idv', 'net', 'org'],
    'uk': ['co', 'ltd', 'me', 'net', 'org', 'plc'],
    'us': ['kids'],
    'za': ['co', 'nom', 'org']}
