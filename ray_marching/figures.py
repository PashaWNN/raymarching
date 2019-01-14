from abc import abstractmethod, ABC
from numpy import sqrt


class SDF(ABC):
    """ SDF Figure base class """
    def __init__(self, x=0, y=0, z=0, scale_x=1.0, scale_y=1.0, scale_z=1.0, *args, **kwargs):
        self.x = x
        self.y = y
        self.z = z
        self.scale_x = 1/scale_x
        self.scale_y = 1/scale_y
        self.scale_z = 1/scale_z

    def get_value(self, x, y, z):
        return self.formula(
            x=x+self.x*self.scale_x,
            y=y+self.y*self.scale_y,
            z=z+self.z*self.scale_z,
        )

    @abstractmethod
    def formula(self, x, y, z):
        pass


class Sphere(SDF):
    def __init__(self, x=0, y=0, z=0, scale_x=1.0, scale_y=1.0, scale_z=1.0, radius=1.0):
        self.r = radius
        super().__init__(x, y, z, scale_x, scale_y, scale_z)

    def formula(self, x, y, z):
        return sqrt(x**2 + y**2 + z**2) - self.r


class Cube(SDF):
    def __init__(self, x=0, y=0, z=0, scale_x=1.0, scale_y=1.0, scale_z=1.0, side=1.0):
        self.s = side
        super().__init__(x, y, z, scale_x, scale_y, scale_z)

    def formula(self, x, y, z):
        return max(abs(x), abs(y), abs(z)) - self.s/2