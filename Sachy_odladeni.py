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

def najdi_kruznice(obr, prah_kruznice):
    edg = skimage.feature.canny(rgb2gray(obr),3)
    try_radii = np.arange(15, 30)
    res = skimage.transform.hough_circle(edg, try_radii)
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

def vymaluj_kruznice(kruznice, kruznice_prev,  img, img_prev, value=0):
    import copy
    img = copy.copy(img)
    for kruz in kruznice:
        rr,cc = skimage.draw.circle_perimeter(kruz[0], kruz[1], kruz[2])
        img[rr, cc] = value
        rr,cc = skimage.draw.circle_perimeter(kruz[0], kruz[1], kruz[2]+1)
        img[rr, cc] = value
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

def nacti_obrazek():
    URL = "http://uc452cam01-kky.fav.zcu.cz/snapshot.jpg"
    img = skimage.io.imread(URL)
    obr=img
    return obr

def najdi_zmeny(kruznice, kruznice_prev):
    zmeny=[]
    for k in range(len(kruznice)):
        je_kruznice_v_seznamu(kruznice[k], kruznice_prev)
        kr=je_kruznice_v_seznamu(kruznice[k], kruznice_prev)
        if kr==False:
            zmeny.append(k)
    return zmeny

def je_kruznice_v_seznamu(kruz, kruznice_prev):
    for i in range(len(kruznice_prev)):
        vzdal = vzdalenost(kruz, kruznice_prev[i])
        # vzdalenosti.append(vzdal)
        if vzdal < 10:
            return True
    return False


rohy_sachovnice = np.asarray([
    [  92.40322581, 5.9516129 ],
    [  65.30645161, 456.27419355],
    [ 586.59677419, 456.27419355],
    [ 554.33870968, 13.69354839]])

src = np.array((
    (0, 0),
    (0, 400),
    (400, 400),
    (400, 0)
))
dst = rohy_sachovnice


tform3 = tf.ProjectiveTransform()
tform3.estimate(src, dst)

obrazek = nacti_obrazek()
