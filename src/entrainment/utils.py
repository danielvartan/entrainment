import numpy as np

def reorder(x, start_at = 0):
    """Reorder a list or array by a starting point.
    
    :Example:
    
    >>> reorder([1, 2, 3], 1)
    [2, 3, 1]
    """ 
    n = len(x)
    
    if (not start_at == 0):
        order = list(np.arange(start_at, n))
        order.extend(list(np.arange(0, start_at)))
        
        return [x[i] for i in order]
    else:
        return x
