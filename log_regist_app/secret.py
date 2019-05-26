import random
import string
import hashlib
import time


def getSalt():
    code = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 6)
    salt = ''.join(code)
    return salt

def set_secret(pwd,salt=None):
    if salt == None:
        h = hashlib.sha3_256()
        salt = getSalt()
        h.update((pwd+salt).encode())
        s_pwd = h.hexdigest()
        return s_pwd
    else:
        h = hashlib.sha3_256()
        h.update((pwd + salt).encode())
        in_pwd = h.hexdigest()
        return in_pwd

def order_secret():
    now = str(time.time())
    # print(now)
    h = hashlib.sha3_256()
    h.update(now.encode())
    s_now = h.hexdigest()
    return s_now


