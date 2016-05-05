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

def fce():
    return 0

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
    plt.imshow(img_prev)
    plt.subplot(1,2,2)
    plt.imshow(img)
    plt.show()
    return img

def vzdalenost(stred1, stred2):
    vzdal = ((stred2[0]-stred1[0])**2+(stred2[1]-stred1[1])**2)**0.5
    return vzdal

# print kruznice_filtr

def nacti_obrazek():
    URL = "http://uc452cam01-kky.fav.zcu.cz/snapshot.jpg"
    img = skimage.io.imread(URL)
    plt.imshow(img)
    # plt._show()
    obr=img
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
    # print zmeny
        print kr
    return zmeny


def je_kruznice_v_seznamu(kruz, kruznice_prev):
    # vzdalenosti = []

    for i in range(len(kruznice_prev)):
        vzdal = vzdalenost(kruz, kruznice_prev[i])
        # vzdalenosti.append(vzdal)
        if vzdal < 10:
            return True


    return False

# kr1=[[20, 35, 15],
#      [15, 47, 10],
#      [17, 23 ,11],
#      [29, 56, 12]]
#
# kr2 = [[20, 35, 15],
#        [25, 67, 10],
#        [17, 23, 11],
#        [35, 26, 19]]
#
# print najdi_zmeny(kr1, kr2)
# print je_kruznice_v_seznamu(kr1, kr2)

obr = nacti_obrazek()
while True:
    obr_prev = obr
    obr = nacti_obrazek()

    kruznice = najdi_kruznice(obr, 0.4)
    kruznice_prev = najdi_kruznice(obr_prev, 0.4)

    zmeny = najdi_zmeny(kruznice, kruznice_prev)
    print zmeny
    # vymaluj_kruznice(kruznice, kruznice_prev, obr, obr_prev, [255, 0, 0])
    zmenene_kruznice = []
    if len(zmenene_kruznice) > 0:
        vymaluj_kruznice([kruznice[zmeny[0]]], kruznice_prev, obr, obr_prev, [255, 0, 0])

    print zmeny
    print najdi_zmeny(kruznice, kruznice_prev)
    plt.imshow(obr, cmap="gray")
    plt.show()


# cap = cv2.VideoCapture(1)
# ret, frame = cap.read()
#
# # Our operations on the frame come here
# img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


# while True:
#     pass

