# -*- coding: utf-8 -*-

# From http://www.iana.org/domains/root/db
GENERAL_TLD = ['com','edu','gov','net','org','mil','travel','aero',
               'asia','cat','coop','int','jobs','mobi','museum','post',
               'tel','xxx','pro','arpa']

REGOIN_TLD  = { "cn": ['xj', 'sh', 'ac', 'gs', 'zj', 'yn', 'ah', 'gz', 
                       'bj', 'gx', 'jl', 'hk', 'gd', 
                       'hn', 'hl', 'edu', 'hb', 'cq', 'ha', 'fj', 'he',
                       'xz', 'sx', 'jx','ln', 'tw', 
                       'mo', 'js', 'nx', 'hi', 'tj', 'sn', 'nm', 'sc', 'qh',
                       'sd'],
                "tw": ['idv','game','club','ebiz'],
                "hk": ['idv'],
                }

def GetFirstLevelDomain(raw_host=""):

    raw_host.lower()
    port = 80
    if ":" in raw_host:
        try:
            (host, port) = raw_host.split(':')
        except ValueError:
            raise ValueError('Too many ":" in %s' % raw_host)
    else:
        host = raw_host
    
    rev = host.split(".")[::-1]
    
    if rev[0] in GENERAL_TLD:
        rev = rev[:2]
    elif len(rev[0].decode('utf-8')) == 2:
        if rev[1] in GENERAL_TLD+REGOIN_TLD.get(rev[0], []):
            rev = rev[:3]
        else:
            rev = rev[:2]
    else:
        raise ValueError('Not valid domain')

    return ".".join(rev[::-1])


if __name__ == '__main__':
    import sys
    print GetFirstLevelDomain(sys.argv[1])
