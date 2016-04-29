import cStringIO
import urllib
import scipy
import scipy.misc
import skimage
import skimage.io
import skimage.data
import skimage.draw
from skimage.filters import threshold_otsu, gaussian_filter
import skimage.transform
# from skimage.filter import threshold_otsu, gaussian_filter
from skimage.morphology import binary_closing, binary_erosion, binary_opening, label, binary_dilation
from skimage.measure import regionprops
from skimage.color import label2rgb, rgb2gray
import skimage.feature
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
import numpy as np
import cv2


URL = "http://uc452cam01-kky.fav.zcu.cz/snapshot.jpg"
img = skimage.io.imread(URL)
plt.imshow(img)
plt.show()



cap = cv2.VideoCapture(1)
ret, frame = cap.read()

# Our operations on the frame come here
img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


plt.imshow(img, cmap="gray")
plt.show()
