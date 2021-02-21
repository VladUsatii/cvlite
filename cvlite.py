#!/usr/bin/env python3
# cvlite classes
#
# By: Vlad Usatii
#
import sys, os
import matplotlib.pyplot as plt
import av
import numpy as np
from PIL import *
import sdl2
import sdl2.ext

class cvlite(object):

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
		return np.array(Image.fromarray(np.uint8(frame)).resize((W, H), Image.NEAREST))

	class Display(object):
		def __init__(self, windowTitle: str, W: int, H: int):
			sdl2.ext.init()
			self.surf = sdl2.ext.Window(windowTitle, size=(W, H))
			self.surf.show()

		def blit(self, vc):
			updates = sdl2.ext.get_events()
			for event in updates:
				if event.type == sdl2.SDL_QUIT:
					sys.exit(0)
			win = sdl2.ext.pixels3d(self.surf.get_surface())
			win[:, :, 0:3] = vc.swapaxes(0, 1)
			self.surf.refresh()

	def colorspace(self, frame, colorspace: str):
		bgr = ['BGR', 'bgr', 'b.g.r.', 'Bgr', 'BGr', 'bGr', 'bGR', 'bgR', 'BgR']
		hsl = ['HSL' 'hsl', 'Hsl', 'HSl', 'hSl', 'hSL', 'hsL', 'HsL']
		if colorspace in bgr:
			frame[:, :, [0, 1, 2]] = frame[:, :, [2, 1, 0]]
			return frame

# TODO: Write catch and exception handler
# - Create photo reader
# - Create video feature detector
# - Corner Detection Algorithms
#	* Shi-Tomasi
