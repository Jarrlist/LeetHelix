def area_circle(r):
    return 3.14 * r * r

def volume_cylinder(r, h):
    base_area = area_circle(r)
    return base_area * h
