#!/usr/bin/env python3
from cvlite import *

# init
cv = cvlite()

if __name__ == "__main__":
	readvid = cv.ReadVideo('../data/P1.mp4')
	frames = readvid.readframes()

	# disp init
	disp = cv.Display('test platform', 1920//2, 1080//2)

	for frame in frames:
		frame = cv.resize(frame, 1920//2, 1080//2)

		print(frame[0][0], frame[0][50])
		disp.blit(frame, '3D')

