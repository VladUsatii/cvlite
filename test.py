#!/usr/bin/env python3
from cvlite import *

# init
cv = cvlite()

if __name__ == "__main__":
	frames = cv.ReadVideo('../data/P1.mp4').readframes()

	# disp init
	disp = cv.Display('test platform', 1920//2, 1080//2)

	for frame in frames:
		frame = cv.resize(frame, 1920//2, 1080//2)
		disp.blit(frame)
