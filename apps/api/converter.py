def dd2dms(dd1,dd2,ndec=6):
    """Convert a decimal degree coordinate pair to a six-tuple of degrees, minutes seconds.
    
    The returned values are not rounded.
    
    Arguments
    
    dd1, dd2 - coordinate pair, in decimal degrees
      
    Example
    
      >>> dd2dms(-74.25,32.1)
      (-74, 15, 6.9444444444444444e-05, 32, 6, 2.7777777777778172e-05)
    """
    # Author: Curtis Price, http://profile.usgs.gov/cprice
    # Disclaimer: Not approved by USGS. (Provisional, subject to revision.)    
    def ToDMS(dd):
        dd1 = abs(float(dd))
        cdeg = int(dd1)
        minsec = dd1 - cdeg
        cmin = int(minsec * 60)
        csec = (minsec % 60) / float(3600)    
        if dd < 0: cdeg = cdeg * -1
        return cdeg,cmin,csec 
    
    try:
        # return a six-tuple
        return ToDMS(dd1) + ToDMS(dd2)           
    except:
        raise Exception, "Invalid input"            

def dms2dd(deg1,min1,sec1,deg2,min2,sec2):
    """Convert a degrees-minutes seconds coordinate pair to decimal degrees.
    
    The returned values are not rounded.
        
    Arguments
    
      deg1,min1,sec1,deg2,min2,sec2 - DMS coordinate pair (six values)
    
    Example
    
    >>> dms2deg(-74,45,0,34,10,20)
    (-74.75, 34.172222222222217)
    """
    # Author: Curtis Price, http://profile.usgs.gov/cprice
    # Disclaimer: Not approved by USGS. (Provisional, subject to revision.)    

    def ToDD(deg,min=0,sec=0):
        dd = abs(deg) + min / 60.0 + sec / 3600.0
        if deg < 0:
            dd = dd * -1.0
        return dd
    try:
        return ToDD(deg1,min1,sec1), ToDD(deg2,min2,sec2)
    except Exception:
        raise Exception, "Invalid input"
