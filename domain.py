
g_GTLD_Suffix = {
    # Generic
    'biz': None,
    'com': None,
    'info': None,
    'name': None,
    'net': None,
    'org': None,
    'pro': None,
    # Sponsored
    'aero': None,
    'asia': None,
    'cat': None,
    'coop': None,
    'edu': None,
    'gov': None,
    'int': None,
    'jobs': None,
    'mil': None,
    'mobi': None,
    'museum': None,
    'tel': None,
    'travel':  None,
    # Infrastructure
    'arpa': None
}

g_GTLD_Other_Suffix = {
    'cc': None,
    'tv': None,
    'tm': None,
    'cd': None,
    'li': None
}

g_CCTLD_CN_Suffix = {
    'ac': None,
    'com': None,
    'edu': None,
    'gov': None,
    'net': None,
    'org': None,
    'mil': None,
    # geographic names
    'ah': None,
    'bj': None,
    'cq': None,
    'fj': None,
    'gd': None,
    'gs': None,
    'gz': None,
    'gx': None,
    'ha': None,
    'hb': None,
    'he': None,
    'hi': None,
    'hl': None,
    'hn': None,
    'jl': None,
    'js': None,
    'jx': None,
    'ln': None,
    'nm': None,
    'nx': None,
    'qh': None,
    'sc': None,
    'sd': None,
    'sh': None,
    'sn': None,
    'sx': None,
    'tj': None,
    'xj': None,
    'xz': None,
    'yn': None,
    'zj': None,
    'hk': None,
    'mo': None,
    'tw': None
}

g_CCTLD_TW_Suffix = {
    'edu': None,
    'gov': None,
    'mil': None,
    'com': None,
    'net': None,
    'org': None,
    'idv': None,
    'game': None,
    'ebiz': None,
    'club': None
}

g_CCTLD_HK_Suffix = {
    'com': None,
    'edu': None,
    'gov': None,
    'idv': None,
    'net': None,
    'org': None
}

g_CCTLD_MO_Suffix = {
    'com': None,
    'edu': None,
    'gov': None,
    'net': None,
    'org': None
}


def IsNumStr(astr):
    try:
        int(astr)
    except:
        return False
    else:
        return True


def GetFirstLevelDomain(host):

    host = host.lower()
    pColon = host.find(':')
    if pColon != -1:
        port = host[pColon:]
        host = host[:pColon]
    else:
        port = None
    try:
        if host[-1] == '.':
            host = host[:-1]
        if host == '':
            return ''
    except:
        return ''

    hostMembers = host.split('.')
    size = len(hostMembers)
    pos = -1

    if hostMembers[-1] in g_GTLD_Suffix:
        pos -= 1
    elif hostMembers[-1] in g_GTLD_Other_Suffix:
        pos -= 1
    elif hostMembers[-1] == 'cn':
        pos -= 1
        if hostMembers[-2] in g_CCTLD_CN_Suffix:
            pos -= 1
    elif hostMembers[-1] == 'tw':
        pos -= 1
        if hostMembers[-2] in g_CCTLD_TW_Suffix:
            pos -= 1
    elif hostMembers[-1] == 'hk':
        pos -= 1
        if hostMembers[-2] in g_CCTLD_HK_Suffix:
            pos -= 1
    elif hostMembers[-1] == 'mo':
        pos -= 1
        if hostMembers[-2] in g_CCTLD_MO_Suffix:
            pos -= 1
    elif (size == 4) and IsNumStr(hostMembers[-1]):
        pos = 0
    else:
        pos = size

    firstLevelDomain = '.'.join(hostMembers[pos:])
    if port is not None:
        firstLevelDomain += port

    return firstLevelDomain


if __name__ == '__main__':
    import sys
    print GetFirstLevelDomain(sys.argv[1])
