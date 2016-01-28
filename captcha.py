from urllib.request import urlopen
from antigate import AntiGate, AntiGateError
import log
import socket
import urllib.error

_key = open('antigate.txt').read().strip()


def solve(url, timeout=10):
    try:
        data = urlopen(url, timeout=timeout).read()
    except urllib.error.URLError:
        log.warning('captcha timeout')
        return None
    except Exception:
        log.error('captcha error', True)
        return None
    with open('captcha.png', 'wb') as f:
        f.write(data)

    try:
        return str(AntiGate(_key, 'captcha.png'))
    except AntiGateError as e:
        print(e)
        return None
    except Exception:
        log.error('captcha error', True)
        return None
