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

def policka(kruz):
    pismeno = ""
    if kruz[1] < 50:
        pismeno = "A"
    else:
        if kruz[1] < 100:
            pismeno = "B"
        else:
            if kruz[1] < 150:
                pismeno = "C"
            else:
                if kruz[1] < 200:
                    pismeno = "D"
                else:
                    if kruz[1] < 250:
                        pismeno = "E"
                    else:
                        if kruz[1] < 300:
                            pismeno = "F"
                        else:
                            if kruz[1] < 350:
                                pismeno = "G"
                            else:
                                if kruz[1] < 400:
                                    pismeno = "H"
    cislice = ""
    if kruz[0] < 50:
        cislice = "1"
    else:
        if kruz[0] < 100:
            cislice = "2"
        else:
            if kruz[0] < 150:
                cislice = "3"
            else:
                if kruz[0] < 200:
                    cislice = "4"
                else:
                    if kruz[0] < 250:
                        cislice = "5"
                    else:
                        if kruz[0] < 300:
                            cislice = "6"
                        else:
                            if kruz[0] < 350:
                                cislice = "7"
                            else:
                                if kruz[0] < 400:
                                    cislice = "8"


    return pismeno + cislice

# def fce():
#     return 0

def najdi_kruznice(obr, prah_kruznice):
    edg = skimage.feature.canny(rgb2gray(obr),3)
    try_radii = np.arange(15, 30)
    res = skimage.transform.hough_circle(edg, try_radii)
#     r, c, try_radii[ridx]

#     prah_kruznice = 0.5
    kruznice = np.asarray(np.nonzero(res > prah_kruznice)).T
    nove_kruznice = []
    for kruz in kruznice:
        nova_kruz = [kruz[1], kruz[2], try_radii[kruz[0]]]
        nove_kruznice.append(nova_kruz)
    kruznice = filtrace_kruznic(nove_kruznice)
    return kruznice

def filtrace_kruznic (kruznice):
    kruznice_filtr = []
    for k in range(len(kruznice)):
        vzdalenosti = []
        for i in range(len(kruznice_filtr)):
            vzdal = vzdalenost(kruznice[k], kruznice_filtr[i])
            vzdalenosti.append(vzdal)

        if len(vzdalenosti) == 0:
            kruznice_filtr.append(kruznice[k])
        else:
            if np.min(vzdalenosti) > 10:
                kruznice_filtr.append(kruznice[k])
    return kruznice_filtr
# print kruznice_filtr

def vymaluj_kruznice(kruznice, kruznice_prev,  img, img_prev, value=0):
    import copy
    img = copy.copy(img)
    for kruz in kruznice:
        rr,cc = skimage.draw.circle_perimeter(kruz[0], kruz[1], kruz[2])
        img[rr, cc] = value
        rr,cc = skimage.draw.circle_perimeter(kruz[0], kruz[1], kruz[2]+1)
        img[rr, cc] = value
#         print kruz

    img_prev= copy.copy(img_prev)
    for kruz in kruznice_prev:
        rr, cc = skimage.draw.circle_perimeter(kruz[0], kruz[1], kruz[2])
        img_prev[rr, cc] = value
        rr, cc = skimage.draw.circle_perimeter(kruz[0], kruz[1], kruz[2] + 1)
        img_prev[rr, cc] = value

    plt.subplot(1,2,1)
    plt.imshow(img_prev, cmap="gray")
    plt.subplot(1,2,2)
    plt.imshow(img, cmap="gray")
    plt.show()
    return img

def vzdalenost(stred1, stred2):
    vzdal = ((stred2[0]-stred1[0])**2+(stred2[1]-stred1[1])**2)**0.5
    return vzdal

# print kruznice_filtr

def nacti_obrazek():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    #
    # # Our operations on the frame come here
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # URL = "http://uc452cam01-kky.fav.zcu.cz/snapshot.jpg"
    # img = skimage.io.imread(URL)

    obr=img
    plt.imshow(obr, cmap="gray")
    # plt._show()

    return obr

def najdi_zmeny(kruznice, kruznice_prev):
    zmeny=[]
    for k in range(len(kruznice)):
        je_kruznice_v_seznamu(kruznice[k], kruznice_prev)
        kr=je_kruznice_v_seznamu(kruznice[k], kruznice_prev)

        if kr==False:
            zmeny.append(k)

        # if len(vzdalenosti) == 0:
        #         zmeny.append(kruznice[k])
        # else:
        #     if np.min(vzdalenosti) > 10:
        #             zmeny.append(kruznice[k])
        # print kr
    return zmeny


def je_kruznice_v_seznamu(kruz, kruznice_prev):
    # vzdalenosti = []

    for i in range(len(kruznice_prev)):
        vzdal = vzdalenost(kruz, kruznice_prev[i])
        # vzdalenosti.append(vzdal)
        if vzdal < 10:
            return True


    return False


# jen na zacatku
obrazek = nacti_obrazek()

# plt.imshow(obrazek)

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
warped = tf.warp(obrazek, tform3, output_shape=(400, 400))
print "obrazek, ", obrazek[:5,:5]
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

kruznice =[[20, 35, 15],
     [225, 177, 10],
     [217, 23 ,11],
     [129, 56, 12]]

kruznice_prev = [[20, 35, 15],
        [217, 23, 11],
        [55, 117, 10],
        [129, 56, 12]]
#
# print najdi_zmeny(kr1, kr2)
# print je_kruznice_v_seznamu(kr1, kr2)

obr = nacti_obrazek()
obr = tf.warp(obr, tform3, output_shape=(400, 400))
obr_prev = nacti_obrazek()
obr_prev = tf.warp(obr_prev, tform3, output_shape=(400, 400))

zmeny = najdi_zmeny(kruznice, kruznice_prev)
print zmeny
# vymaluj_kruznice(kr1, kr2, obr, obr_prev, [255, 0, 0])
zmenene_kruznice = []

if len(zmeny)>0:
    zmenene_kruznice = [kruznice[zmeny[0]]]

    # print zmenene_kruznice
    # zmenene_kruznice = [[60, 78, 20]]
vymaluj_kruznice(zmenene_kruznice, kruznice_prev, obr, obr_prev, [1.0, 0, 0])

# print zmeny[0]

# zmenene_kruznice = [kruznice[zmeny[0]]]
print zmenene_kruznice

# plt.imshow(obr)
# rohy_sachovnice = plt.ginput(4)
# plt.show()
print rohy_sachovnice

zmena_prev = najdi_zmeny(kruznice_prev, kruznice)
# print kruznice[zmeny[0]]
print policka(kruznice_prev[zmena_prev[0]]) + " -> " + policka(kruznice[zmeny[0]])
# + " -> " + policka(kruznice_prev[])

# print zmena_prev
# print policka(kruznice_prev[zmena_prev[0]])

#
#     print zmeny
# obr = nacti_obrazek()
# while True:
#     obr_prev = obr
#     obr = nacti_obrazek()
# #
#     kruznice = najdi_kruznice(obr, 0.4)
#     kruznice_prev = najdi_kruznice(obr_prev, 0.4)
# #
#     zmeny = najdi_zmeny(kr1, kr2)
#     print zmeny
#     vymaluj_kruznice(kr1, kr2, obr, obr_prev, [255, 0, 0])
#     zmenene_kruznice = []
#     if len(zmenene_kruznice)>0:
#     # if len(zmenene_kruznice)==1:
#     vymaluj_kruznice(zmenene_kruznice, kruznice_prev, obr, obr_prev, [255, 0, 0])
# #
#     print zmeny
#     print najdi_zmeny(kruznice, kruznice_prev)

    # plt.imshow(obr, cmap="gray")
    # plt.show()


# cap = cv2.VideoCapture(1)
# ret, frame = cap.read()
#
# # Our operations on the frame come here
# img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


# while True:
#     pass

