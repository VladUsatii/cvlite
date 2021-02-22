#!/usr/bin/env python3
# cvlite classes
#
# By: Vlad Usatii
#
import sys, os
import matplotlib.pyplot as plt
import matplotlib as mpl
import av
import numpy as np
from PIL import *
import sdl2
import sdl2.ext

# HARDWARE ACCELERATION ON CUDA GPU
# from numba import jit, cuda


class cvlite(object):
	def __init__(self):
		self.X = 'X'
		self.Y = 'Y'

	class ReadPhoto(object):
		def __init__(self, src: str):
			self.photo = src

		def show(self):
			while True:
				img = Image.open(str(self.photo))
				arr = np.array(img)
				yield arr

	class ReadVideo(object):
		def __init__(self, src: str):
			self.video = src

		def readframes(self):
			v = av.open(str(self.video))
			for frame in v.decode(video=0):
				img = frame.to_image()
				arr = np.array(img)
				yield arr

	def resize(self, frame, W: int, H: int):
		return np.asarray(Image.fromarray(np.uint8(frame)).resize((W, H), Image.NEAREST))

	def rotate(self, frame, degrees: int):
		return np.asarray(Image.fromarray(np.uint8(frame)).rotate(degrees))

	def flip(self, frame, flip):
		if flip == self.X:
			return np.fliplr(frame)
		elif flip == self.Y:
			return np.flipud(frame)
		else:
			raise ValueError("\n\nYou must use either cvlite().X or cvlite().Y to flip on the X or Y-axis.")

	class Display(object):
		def __init__(self, windowTitle: str, W: int, H: int):
			sdl2.ext.init()
			self.surf = sdl2.ext.Window(windowTitle, size=(W, H))
			self.surf.show()

		def blit(self, vc, dimensionality: str):
			updates = sdl2.ext.get_events()
			for event in updates:
				if event.type == sdl2.SDL_QUIT:
					sys.exit(0)
			if dimensionality == '3D':
				win = sdl2.ext.pixels3d(self.surf.get_surface())
				win[:, :, 0:3] = vc.swapaxes(0, 1)
			elif dimensionality == '2D':
				win = sdl2.ext.pixels2d(self.surf.get_surface())
				win[:, :] = vc.swapaxes(0, 1)
			else:
				raise ValueError("\n\nYou must enter either 2D or 3D for a dimension.")
			self.surf.refresh()

	def colorspace(self, frame, colorspace: str):
		bgr = ['BGR', 'bgr', 'b.g.r.', 'Bgr', 'BGr', 'bGr', 'bGR', 'bgR', 'BgR']
		hsl = ['HSL' 'hsl', 'Hsl', 'HSl', 'hSl', 'hSL', 'hsL', 'HsL']
		if colorspace in bgr:
			frame[:, :, [0, 1, 2]] = frame[:, :, [2, 1, 0]]
			return frame
		else:
			raise ValueError("\n\nYou must enter a valid colorspace.")

# TODO: Write catch and exception handler
# - Create photo reader
# - Create video feature detector
# - Corner Detection Algorithms
#	* Shi-Tomasi
