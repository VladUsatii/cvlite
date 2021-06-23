#!/usr/bin/env python3
from cvlite import cvlite
import numpy as np

cv = cvlite()

if __name__ == "__main__":
	readvid = cv.ReadVideo("../data/P1.mp4")
	frames = readvid.readframes()

	# disp init
	disp = cv.Display("test 2", 1920//2, 1080//2)

	for frame in frames:
		frame = cv.resize(frame, 1920//2, 1080//2)
		frame = cv.colorspace(frame, "BGR")
		frame = cv.backgroundSubtractor(frame, 50, 100, 200)
		print(frame[0][0], frame[0][50])
		disp.blit(frame, '3D')
