#cvlite

Made for Python3, with Python3.

### Introduction

cvlite is a lightweight, computer-vision library, designed for all devices in the cleanest, fastest way possible. The original goal of the library was to accomplish faster notational speed than Computer Vision Library 2, a massive open-source C++ project, made for C++ originally. A Python plug-in was later developed by a pull request and was merged a few weeks back, as I write this.

cvlite aims to simplify the computer vision process through basic function declarations, class-based modules, and latency tests. Our matrices are the exact same, but have better customization features.

### Getting Started

To install from Product API, type the following:

```
git clone https://github.com/VladUsatii/cvlite
```

Your library will update regularly with initialization.

Next, make a python3 file and import cvlite:

```python
from cvlite import *

cvl = cvlite()
```

#### Playing a Video File

ReadVideo() is a handy function designed for reading videos.
ReadPhoto() is a handy function designed for displaying a single frame.

To play a video, initialize ReadVideo() and add your relative video file in the parantheses as a string. From there, you can do many different things with your video. We recommend importing sdl2 and sdl2.ext to blit a 3D frame to the screen:

Before blitting, read the frames with a handy function called:

```python
ReadVideo('path/to/file').readframes() # returns
```

```
pip install PySDL2
```

Run this simple command to blit to the screen with our SDL2-based lightweight option:

```python
rv = ReadVideo('path/to/file').readframes()
for frame in rv:
	cvlite().blit(rv, '3D') # or 2D for 2D features
```
