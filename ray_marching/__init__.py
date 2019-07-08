from numpy import cos, sin, tan, array, dot, zeros, uint8
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
        a = self.alpha
        b = self.beta
        self._rotation_matrix = array([
            [cos(a) * cos(b), -cos(a) * sin(b), sin(a)],
            [sin(b), cos(b), 0],
            [-cos(b) * sin(a), sin(a) * sin(b), cos(a)],
        ])
        self._cam_coordinates = dot(self._rotation_matrix, array([
            [self.dist], [0], [0],
        ]))
        self._vec_x0y0z0 = dot(self._rotation_matrix, array([
            [-1], [0], [0],
        ]))
        self._pixel_size = (2 * tan(self.fov / 2)) / self.height

        self._u = dot(self._rotation_matrix, array([
            [0], [0], [1],
        ])) * self._pixel_size

        self._v = dot(self._rotation_matrix, array([
            [0], [1], [0],
        ])) * self._pixel_size

        self.cx, self.cy, self.cz = ndarray.tolist(ndarray.flatten(self._cam_coordinates))
        self.dist0 = self.sdf(self.cx, self.cy, self.cz)

    def _ray_direction(self, x, y):
        """ Get direction of ray corresponding to screen coordinates"""
        return self._vec_x0y0z0 + x * self._u + y * self._v

    def _get_pixel(self, x, y):
        rx, ry, rz = ndarray.tolist(ndarray.flatten(self._ray_direction(x, y)))
        k = self.dist0 + self.sdf(self.cx + rx * self.dist0, self.cy + ry * self.dist0, self.cz + rz * self.dist0)
        for _ in range(self.iters - 1):
            k = k + self.sdf(self.cx + rx * k, self.cy + ry * k, self.cz + rz * k)
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
