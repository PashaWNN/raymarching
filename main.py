from ray_marching import RayMarching, figures


sphere = figures.Sphere()
cube = figures.Cube(side=1.5)


def cube_minus_sphere(x, y, z):
    return max(-sphere.get_value(x, y, z), cube.get_value(x, y, z))

def cube_plus_sphere(x, y, z):
    return min(sphere.get_value(x, y, z), cube.get_value(x, y, z))


renderer = RayMarching(
    width=512,
    height=512,
    dist=2.2,
    sdf=cube_plus_sphere)


im = renderer.render_to_image()
im.show()
