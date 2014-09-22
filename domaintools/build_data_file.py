import os.path
import pprint
import requests


PUBLIC_SUFFIX_URL = 'https://publicsuffix.org/list/effective_tld_names.dat'


def parse_tld_data(data):
    """ Parses raw data from the suffix list into a python dict """
    private = False
    tlds = {}
    for line in data.split('\n'):
        line = line.strip().decode('utf8')
        if line.startswith('// ===BEGIN PRIVATE DOMAINS==='):
            # set the private flag, all future values are private
            private = True
            continue
        if not line or line.startswith('//'):
            continue
        line = line.encode('idna')
        frags = line.split('.')
        if frags[-1] not in tlds:
            tlds[frags[-1]] = {}
        tlds[frags[-1]][line] = private
    return tlds

def update_data_file():
    """ grabs the latest public suffix list, parses it, and saves to data.py"""
    rsp = requests.get(PUBLIC_SUFFIX_URL)
    data = rsp.content
    tlds = parse_tld_data(data)
    out = 'TLDS = %s' % pprint.pformat(tlds)
    frags = __file__.rsplit('/',1)
    if len(frags) == 1:
        filename = 'data.py'
    else:
        filename = os.path.join(frags[0], 'data.py')
    f = open(filename, 'w')
    f.write(out)
    f.close()


if __name__ == '__main__':
    update_data_file()
