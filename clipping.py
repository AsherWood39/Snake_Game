def compute_code(x, y, xmin, ymin, xmax, ymax):
    code = 0
    if x < xmin: code |= 1
    if x > xmax: code |= 2
    if y < ymin: code |= 4
    if y > ymax: code |= 8
    return code

def cohen_sutherland(x0, y0, x1, y1, viewport):
    """Cohen-Sutherland clipping - Module 3"""
    xmin, ymin, xmax, ymax = viewport
    code0 = compute_code(x0, y0, xmin, ymin, xmax, ymax)
    code1 = compute_code(x1, y1, xmin, ymin, xmax, ymax)
    
    while True:
        if not (code0 | code1):
            return (x0, y0, x1, y1)  # Fully inside
        if code0 & code1:
            return None  # Fully outside
        
        # Clip
        x, y = 0, 0
        code_out = code0 if code0 else code1
        if code_out & 1:    # Left
            x, y = xmin, y0 + (y1-y0)*(xmin-x0)/(x1-x0)
        elif code_out & 2:  # Right
            x, y = xmax, y0 + (y1-y0)*(xmax-x0)/(x1-x0)
        elif code_out & 4:  # Bottom
            x, y = x0 + (x1-x0)*(ymin-y0)/(y1-y0), ymin
        elif code_out & 8:  # Top
            x, y = x0 + (x1-x0)*(ymax-y0)/(y1-y0), ymax
        
        if code_out == code0:
            x0, y0, code0 = x, y, compute_code(x, y, xmin, ymin, xmax, ymax)
        else:
            x1, y1, code1 = x, y, compute_code(x, y, xmin, ymin, xmax, ymax)
