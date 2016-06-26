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
# from __future__ import print_function

import math
import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage import transform as tf

margins = dict(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0, right=1)

def nacti_obrazek():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    #
    # # Our operations on the frame come here
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # URL = "http://uc452cam01-kky.fav.zcu.cz/snapshot.jpg"
    # img = skimage.io.imread(URL)

    obr=img
    # plt.imshow(obr, cmap="gray")
    # plt._show()

    return obr

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# plt.imshow(img, cmap="gray")
# cap = cv2.VideoCapture(0)
# ret, frame = cap.read()
#
# # Our operations on the frame come here
img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
rohy_sachovnice = np.asarray(plt.ginput(4))
# plt.show()
# rohy_sachovnice = np.asarray([
#     [ 132.40322581,   96.27419355],
#     [ 106.59677419,  412.40322581],
#     [ 457.56451613,  413.69354839],
#     [ 438.20967742,  109.17741935]])


print rohy_sachovnice

src = np.array((
    (0, 0),
    (0, 400),
    (400, 400),
    (400, 0)
))
dst = rohy_sachovnice


tform3 = tf.ProjectiveTransform()
tform3.estimate(src, dst)

# s kazdym nactenim
# print obrazek[:5,:5,:]
warped = tf.warp(img, tform3, output_shape=(400, 400))
print "obrazek, ", img [:5,:5]
print "warped ", warped[:5,:5]

fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(8, 3))
fig.subplots_adjust(**margins)
plt.gray()
# ax1.imshow(obrazek)
ax1.plot(dst[:, 0], dst[:, 1], '.r')
ax1.axis('off')
# ax2.imshow(warped)
ax2.axis('off')
# plt.show()

obr = nacti_obrazek()
obr = tf.warp(obr, tform3, output_shape=(400, 400))

plt.imshow(obr)
plt.show()

