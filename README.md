# Ray Marching algorithm renderer

![demo][image] ![demo][image2]

[image]: https://github.com/pashawnn/raymarching/blob/master/cube.png
[image2]: https://github.com/pashawnn/raymarching/blob/master/sphere.png

Inspired by [this](https://habr.com/post/353422/) article on Habr.

This is my Python 3 implementation of graphical renderer using Ray Marching algorithm.

## Requirements and installation

This program requires NumPy package for calculations and PIL for image creating and showing.
You can install it with this:
```
$ pip install Pillow numpy
```
or this:
```
$ pip install -r requirements.txt
```
command.

To run demo, just type:
```
$ python3 main.py
```

## How it works?

In ray marching algorithm, the whole 3D scene is a signed distance function. So, to define a model, you just need to define `f(x, y, z)` function, that returns a minimal distance to this model from `(X, Y, Z)`. If this coordinates is inside of a model, distance would be with a minus sign.

For example, sphere definition in Python:
```python
from math import sqrt


def formula(x, y, z, r):
    return sqrt(x**2 + y**2 + z**2) - r
``` 

It's simple!

To render this object, you need to instantiate renderer:
```python
renderer = RayMarching(
    width=128,               # Viewport width
    height=128,              # Viewport height
    dist=2.6,                # Distance between (0,0,0) and camera
    iterations=50,           # Number of marching iterations
    sdf=formula)              # Signed Distance Function
```
And then call render method:
```python
im = renderer.render_to_image()  # PIL.Image
# or
ar = renderer.render_to_array()  # NumPy array, integer is pixel brightness
```


Feel free to do experiments with it and to contribute to my repo.

---

##### TODO:

* teapot model
* UI, maybe
* multiprocessing for better performance
* ...
