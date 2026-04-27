from datetime import datetime

def today():
    """Bugünün tarihini GG-AA-YY formatında döndürür"""
    return datetime.now().strftime("%d-%m-%y")

def nowtime():
    """Şu anki saati SS:DD formatında döndürür"""
    return datetime.now().strftime("%H:%M")

def to_date(tarih):
    """GG-AA-YY formatındaki tarihi datetime objesine çevirir"""
    return datetime.strptime(tarih, "%d-%m-%y")



def canirent(datelist,newst,newfn):
    newst = to_date(newst)
    newfn = to_date(newfn)
    
    for _st,_fn,iade in datelist:
        _st = to_date(_st)
        if iade != "-":
            _fn = iade
        _fn = to_date(_fn)
        
        if newst <= _fn and newfn >= _st:
            return False
    return True
        
        

def caniiade(datelist,_iade):
    
    _iade = to_date(_iade)
    
    for __st,__fn,iade in datelist:
        _st = to_date(__st)
        if iade != "-":
            __fn = iade
        _fn = to_date(__fn)
    
    
        if _iade >= _st and _iade < _fn:
            return [True,__st,__fn]
    return [False,0,0]