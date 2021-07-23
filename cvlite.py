#!/usr/bin/env python3
#
# Computer Vision Lite
#
# A lightweight computer-vision wrapper/library for fast, optimized, and challenging algorithmic tasks.
#
# By: Vlad Usatii
#

# os \ env
import sys, os

# matplot
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.image as mpimg

# AV & video arrays
import av
import numpy as np
from PIL import *
import sdl2
import sdl2.ext

# calc
from skimage.transform import resize
import scipy.misc as sm

# video optimization
import ffmpeg
import subprocess


# convention:
# cvl = cvlite()
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
			self.spec = [stream for stream in ffmpeg.probe(str(src))["streams"] if stream["codec_type"] == "video"]
			self.size = (self.spec[0].get("height"), self.spec[0].get("width"), 3)
			self.width = self.size[0]
			self.height = self.size[1]
			self.aspectratio = str(int((10 * (self.size[1]/self.size[0])) - (self.size[1]/self.size[0]))) + ":" + str(int(9))

		def readframes(self):
			cmd = ['ffmpeg', '-i', self.video, '-vf', 'scale=%d:%d'%(int(self.size[0]),int(self.size[1])), '-r', str(30), '-an', '-c:v', 'rawvideo', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-loglevel', 'quiet', '-']
			p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

			while True:
				arr = np.fromstring(p.stdout.read(int(self.size[0])*int(self.size[1])*3), dtype=np.uint8)
				if len(arr) == 0:
					p.wait()
					return

				yield arr.reshape((int(self.size[1]), int(self.size[0]), 3))

	def backgroundSubtractor(self, frame, threshold1: int, threshold2: int, new: int):
		frame[(frame > threshold1) & (threshold2 < 150)] = new
		return frame

	#TODO: make this faster with CPython
	def gaussianblur(self, frame, intensity: int):
		from scipy.ndimage.filters import gaussian_filter
		return gaussian_filter(frame, sigma=(intensity, intensity, 0))

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
		bw = ['bw', 'Bw', 'BW', 'bW']
		hsl = ['HSL' 'hsl', 'Hsl', 'HSl', 'hSl', 'hSL', 'hsL', 'HsL']
		if colorspace in bgr:
			frame = frame.copy()
			frame[:, :, [0, 1, 2]] = frame[:, :, [2, 1, 0]]
			return frame
		elif colorspace in bw:
			dimensions = frame.shape[2]
			frame = np.dot(frame[...,:3], [0.2989, 0.5870, 0.1140])
			if dimensions == 3:
				frame = np.atleast_3d(frame)	
			# frame = np.array(frame, ndmin=dimensions, copy=True).T.swapaxes(0,1)
			return frame
		else:
			raise ValueError("\n\nYou must enter a valid colorspace.")


	def threshold(self, frame, T: int):
		frame = frame.copy()
		h = frame.shape[1]
		w = frame.shape[0]

		for x in range(0, w):
			for y in range(0, h):
				if frame[x, y][[0]] >= T:
					frame[x, y][[0]] = 255

		return frame

# TODO: Write catch and exception handler
# - Finish plot and frequency tracker
# - Create video feature detector
# - Corner Detection Algorithms
#	* Shi-Tomasi
