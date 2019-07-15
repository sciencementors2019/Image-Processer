#!/usr/bin/env python
import os
from matplotlib.pyplot import imread
fimg = imread("New Bitmap Image.bmp")
from skimage import color
gimg = color.colorconv.rgb2grey(fimg)
from skimage import measure
contours = measure.find_contours(gimg, 0.85, fully_connected='high', positive_orientation='low')
import matplotlib.pyplot as plt
    
for n, contour in enumerate(contours):
    plt.plot(contour[:, 1], contour[:, 0], linewidth=2)
plt.savefig("test.svg", format="svg")
