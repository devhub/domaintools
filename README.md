# domaintools

Domain parsing with python

## Usage

Basic usage:

    from domaintools import Domain
    d = Domain('www.example.com')

Validate domain (also validates TLD):

    >>> d.valid
    True

Access domain parts:

    >>> d.domain
    u'example.com'

    >>> d.subdomain
    u'www'

    >>> d.tld
    u'com'

    >>> d.sld
    u'example'

IDN domain support

    >>> d = Domain('xn--4gqx73hwke.com', decode_idna=True)
    >>> d.domain
    u'\u7edf\u4e00\u7801.com'

## Installation

    pip install 'git+git://github.com/devhub/domaintools.git'

## License

domaintools is released under the the [MIT license](http://creativecommons.org/licenses/MIT/).

## Credits

Originally developed by [Mark Lee](https://github.com/malept) while employed at EVO Media Group.
