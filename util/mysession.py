from uuid import uuid4
from util.myutil import myuuid

s = {}

class MySession:
    def __init__(self,handler):
        self.handler = handler

    def __getitem__(self, item):
        # 凭证　的　值
        c = self.handler.get_cookie('uid')
        if c:
            d = s.get(c,None)
            if d:
                v = d.get(item)
                return v
            else:
                return None
        else:
            return None

    def __setitem__(self, key, value):
        c = self.handler.get_cookie('uid')
        if c:
            d = s.get(c,None)
            if d:
                d[key] = value
            else:
                d = {}
                d[key] = value
                s[c] = d

        else:
            u = myuuid(uuid4())
            d = {}
            d[key] = value
            s[u] = d
            self.handler.set_cookie('uid',u,expires_days=10)
