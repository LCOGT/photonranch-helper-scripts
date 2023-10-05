
import numpy as np
import matplotlib.pyplot as plt
import time
import bz2 
import os
import datetime
import random
from astropy.io import fits 
from skimage.io import imsave
from auto_stretch.stretch import Stretch


###############################################
######   make some interesting noise    #######
###############################################

def perlin(x,y,seed=0):
    # permutation table
    np.random.seed(seed)
    p = np.arange(256,dtype=int)
    np.random.shuffle(p)
    p = np.stack([p,p]).flatten()
    # coordinates of the top-left
    xi = x.astype(int)
    yi = y.astype(int)
    # internal coordinates
    xf = x - xi
    yf = y - yi
    # fade factors
    u = fade(xf)
    v = fade(yf)
    # noise components
    n00 = gradient(p[p[xi]+yi],xf,yf)
    n01 = gradient(p[p[xi]+yi+1],xf,yf-1)
    n11 = gradient(p[p[xi+1]+yi+1],xf-1,yf-1)
    n10 = gradient(p[p[xi+1]+yi],xf-1,yf)
    # combine noises
    x1 = lerp(n00,n10,u)
    x2 = lerp(n01,n11,u) 
    return lerp(x1,x2,v) 

def lerp(a,b,x):
    "linear interpolation"
    return a + x * (b-a)

def fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def gradient(h,x,y):
    "grad converts h to the right gradient vector and return the dot product with (x,y)"
    vectors = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vectors[h%4]
    return g[:,:,0] * x + g[:,:,1] * y


def crop (nparray, xlen, ylen):
    return nparray[0:ylen, 0:xlen]

def normalize(nparray):
    maxval = np.amax(nparray)
    minval = np.amin(nparray)
    data = nparray + np.abs(minval)
    data = data / (maxval + np.abs(minval))
    return data

def get_perlin(squarelen=768):
    lin = np.linspace(0,2,squarelen,endpoint=False)
    x,y = np.meshgrid(lin,lin) 
    data = perlin(x,y,seed=int(time.time()))
    return data

###############################################
######           file handling          #######
###############################################

def to_bz2(filename):
    with open(filename, 'rb') as uncomp:
        comp = bz2.compress(uncomp.read())
    with open(filename + '.bz2', 'wb') as target:
        target.write(comp)


###############################################
###### create the header and data files #######
###############################################

def make_header(extras={}):
    header_dict = {
        "DATE-OBS": datetime.datetime.now().isoformat().split('.')[0],
        "IMAGETYP": "TEST DATA",
        "CRVAL1": random.random()*24,
        "CRVAL2": (random.random() * 180) - 90,
        "ALTITUDE": round(random.random() * 60 + 30, 3),
        "AZIMUTH": round(random.random() * 180, 3),
        "FILTER": "'L'",
        "AIRMASS": round(random.random() * 2 + 1, 3),
        "EXPTIME": round(random.randint(1,20), 3),
        "USERID": "'google-oauth2|100354044221813550027'",
        "USERNAME": "'Test Script'", 
        "HEADER": "'header'",
        **extras
    }
    return header_dict

def make_data_files(header_dict={}, savedirectory="generated_files"):
    filename = f"{savedirectory}/generated.fits"

    hdu = fits.PrimaryHDU()
    hdu.data = get_perlin(768)

    # add header to fits data
    for key in header_dict:
        hdu.header[key] = header_dict[key]
    
    # write header text file
    with open(f'{savedirectory}/generated.txt', 'w') as txt:
        txt.write(str(hdu.header))

    # write jpg file
    positive_jpg_data = hdu.data + np.abs(np.amin(hdu.data)) # make all vals positive
    jpg_data = Stretch().stretch(positive_jpg_data)  # stretch
    jpg_8 = (jpg_data * 256).astype('uint8')  # convert to 8-bit int for jpg
    imsave(f"{savedirectory}/generated.jpg", jpg_8)

    # write fits file
    hdu.writeto(filename, overwrite=True)

    # write bz2 fits file
    to_bz2(filename)
