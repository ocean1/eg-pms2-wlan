import requests
import sys

import re
from collections import defaultdict, OrderedDict


status_re = r'var sockstates =\[(.*)\]'


def usage():
    print "Usage: {} <hostname> <password> [socket:state]...".format(sys.argv[0])
    print "   [socketN] - a pair X:Y where X - socket number (1-4), Y - state (0 - off, 1 - on)"


def login(hostname, password):
    r = requests.post(
        "http://{}/login.html".format(hostname),
        data={"pw": password}
    )
    return r


def ChangeState(hostname, updates):
    params = map(lambda p: map(int, p.split(':')), updates)
    status = defaultdict(str, dict(params))

    ctes = OrderedDict()
    for k in range(1, 5):
        ctes["cte{}".format(k)] = status[k]

    r = requests.post(
        "http://{}".format(hostname),
        data=ctes
    )
    stat = re.findall(status_re, r.text)[0].split(',')
    stat = [bool(int(s)) for s in stat]
    return stat

if __name__ == "__main__":

    try:
        hostname = sys.argv[1]
        password = sys.argv[2]
        login(hostname, password)
        print ChangeState(hostname, sys.argv[3:])
    except Exception as e:
        print e
        usage()
