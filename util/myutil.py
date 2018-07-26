import hashlib


def release(pwd):
    md = hashlib.md5()
    md.update(pwd.encode('utf8'))
    return md.hexdigest()

def myuuid(u):
    md = hashlib.md5()
    md.update(u.bytes)
    return md.hexdigest()