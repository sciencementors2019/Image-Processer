import os
os.chdir('C:\\Users\\video')
from matplotlib.pyplot import imread
os.chdir('D:\\smc2019\\Image-Processer')
fimg = imread("flow.bmp")
from skimage import color
gimg = color.colorconv.rgb2grey(fimg)
from skimage import measure
contours = measure.find_contours(gimg, 0.85)
import matplotlib.pyplot as plt
    
for n, contour in enumerate(contours):
    plt.plot(contour[:, 1], contour[:, 0], linewidth=2)
print(len(contours))
plt.savefig("test.svg", format="svg")
