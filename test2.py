#!/usr/bin/env python3
from cvlite import cvlite
import numpy as np


cvl = cvlite()
vid = cvl.ReadVideo().readframes()

while True:
	cv.blit(vid, "3D")
