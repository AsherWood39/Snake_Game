def scanline_fill(poly, width):
    """Basic scanline fill - Module 2"""
    points = []
    ymin = min(y for x,y in poly)
    ymax = max(y for x,y in poly)
    
    for y in range(ymin, ymax+1):
        intersections = []
        for i in range(len(poly)):
            x1, y1 = poly[i]
            x2, y2 = poly[(i+1)%len(poly)]
            if (y1 <= y < y2) or (y2 <= y < y1):
                if x1 == x2:
                    intersections.append(x1)
                else:
                    t = (y - y1) / (y2 - y1)
                    intersections.append(x1 + t * (x2 - x1))
        
        if len(intersections) >= 2:
            left = min(intersections)
            right = max(intersections)
            for x in range(int(left), int(right)+1):
                if 0 <= x < width:
                    points.append((x, y))
    return points
