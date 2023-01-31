import requests as r
import time

he={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}

def rget_cycle(a,to,st,rn):
    rn+=1
    if rn>5:
        raise RuntimeError
    time.sleep(1)
    return rget(a,to,st,rn)

def rget(a,to=10,st=False,rn=0):
    try:return r.get(a,headers=he,timeout=to,stream=st)
    except:return rget_cycle(a,to,st,rn)

def rpost_cycle(a,d,to,st,rn):
    rn+=1
    if rn>5:
        raise RuntimeError
    time.sleep(1)
    return rpost(a,d,to,st,rn)

def rpost(a,d,to=10,st=False,rn=0):
    try:return r.post(a,headers=he,data=d,timeout=to,stream=st)
    except:return rpost_cycle(a,d,to,st,rn)

def valid_cycle(a,te,to,st,rn):
    rn+=1
    if rn>5:
        raise RuntimeError
    time.sleep(1)
    return valid(a,te,to,st,rn)

def valid(a,te,to=10,st=False,rn=0):
    ret=rget(a,to,st)
    return valid_cycle(a,te,to,st,rn)if te not in ret.text else ret
