from numpy import cos, sin, tan, sqrt, array, dot, zeros, uint8
from numpy.linalg import norm
from numpy import ndarray
from typing import Callable
from PIL import Image


class RayMarching:
    def __init__(self, width: int = 77, height: int = 50, alpha: float = 35.0, beta: float = 25.0, iterations: int = 50,
                 dist: float = 1.4, fov: float = 39, sdf: Callable[[float, float, float], float] = lambda x, y, z: 0.0):
        self.width = width
        self.height = height
        self.alpha = alpha
        self.beta = beta
        self.dist = dist
        self.fov = fov
        self.sdf = sdf
        self.iters = iterations

    @property
    def _rotation_matrix(self):
        a = self.alpha
        b = self.beta
        return array([
            [cos(a) * cos(b), -cos(a) * sin(b), sin(a)],
            [sin(b), cos(b), 0],
            [-cos(b) * sin(a), sin(a) * sin(b), cos(a)],
        ])

    @property
    def _cam_coordinates(self):
        """ Get camera coordinates """
        return dot(self._rotation_matrix, array([
            [self.dist], [0], [0],
        ]))

    @property
    def _vec_x0y0z0(self):
        """ Get vector between cam and screen center """
        return dot(self._rotation_matrix, array([
            [-1], [0], [0],
        ]))

    @property
    def _pixel_size(self):
        """ Get pixel size on the screen """
        return (2 * tan(self.fov / 2)) / self.height

    @property
    def _u(self):
        return dot(self._rotation_matrix, array([
            [0], [0], [1],
        ])) * self._pixel_size

    @property
    def _v(self):
        return dot(self._rotation_matrix, array([
            [0], [1], [0],
        ])) * self._pixel_size

    def _ray_direction(self, x, y):
        """ Get direction of ray corresponding to screen coordinates"""
        return self._vec_x0y0z0 + x * self._u + y * self._v

    def _ray(self, x, y, d):
        """ Find ray corresponding to screen coordinates """
        return self._cam_coordinates + d * (self._ray_direction(x, y) /
                                            norm(self._ray_direction(x, y)))

    def _dist0(self, cx, cy, cz):
        return self.sdf(cx, cy, cz)

    def _get_pixel(self, x, y):
        cx, cy, cz = ndarray.tolist(ndarray.flatten(self._cam_coordinates))
        rx, ry, rz = ndarray.tolist(ndarray.flatten(self._ray_direction(x, y)))
        dist0 = self._dist0(cx, cy, cz)
        k = dist0 + self.sdf(cx + rx * dist0, cy + ry * dist0, cz + rz * dist0)
        for _ in range(self.iters - 1):
            k = k + self.sdf(cx + rx * k, cy + ry * k, cz + rz * k)
        return k

    def render_to_array(self):
        plot = zeros((self.height, self.width))
        h2 = round(self.width / 2)
        w2 = round(self.height / 2)
        for y in range(-w2, w2):
            for x in range(-h2, h2):
                plot[y + w2, x + h2] = self._get_pixel(y, x)
        return plot

    def render_to_image(self) -> Image:
        plot = self.render_to_array()
        return Image.fromarray((plot * 200).astype(uint8), 'L')
