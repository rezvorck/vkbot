import configparser
import accounts

cp = configparser.ConfigParser()
cp.read(accounts.getFile('inf.cfg'))


def get(param, typename='s'):
    param = param.split('.')
    if typename == 's':
        return cp[param[0]].get(param[1])
    elif typename == 'i':
        return cp[param[0]].getint(param[1])
    elif typename == 'f':
        return cp[param[0]].getfloat(param[1])
    elif typename == 'b':
        return cp[param[0]].getboolean(param[1])
