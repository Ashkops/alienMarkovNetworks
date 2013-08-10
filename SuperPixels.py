import os
import sys

import numpy as np

import skimage
import skimage.data

from skimage.segmentation import slic, felzenszwalb, quickshift, mark_boundaries

import matplotlib.pyplot as plt

import pomio


# Module wraps skimage segementation functions

def displayImage(image, imgTitle, orientation):
    assert orientation == "upper" or orientation == "lower", "orientation parameter to displayImage must be \"upper\" or \"lower\"."
    plt.imshow(image, origin=orientation)
    plt.title(imgTitle)
    plt.show()


def getSuperPixels_SLIC(image, nbSegments):
    # See [http://scikit-image.org/docs/dev/api/skimage.segmentation.html?highlight=slic#skimage.segmentation.slic] for parameter definitions
    # Function signature: skimage.segmentation.slic(image, n_segments=100, ratio=10.0, max_iter=10, sigma=1, multichannel=None, convert2lab=True)
    segmentationMask = slic(image, nbSegments)
    return segmentationMask


def getSuperPixels_Graph(image):
    # See [http://scikit-image.org/docs/dev/api/skimage.segmentation.html?highlight=slic#skimage.segmentation.felzenszwalb]
    # Function usage:    skimage.segmentation.felzenszwalb(image, scale=1, sigma=0.8, min_size=20)
    # Produces an oversegmentation of a multichannel (i.e. RGB) image using a fast, minimum spanning tree based clustering on the image grid. The parameter scale sets an observation level. Higher scale means less and larger segments. sigma is the diameter of a Gaussian kernel, used for smoothing the image prior to segmentation.
    # image : (width, height, 3) or (width, height) ndarray. Input image.
    # scale : float. Free parameter. Higher means larger clusters.
    # sigma : float. Width of Gaussian kernel used in preprocessing.
    # min_size : int. Minimum component size. Enforced using postprocessing.
    superPixelImage = skimage.segmentation.felzenszwalb(image, scale=25, sigma=1.0, min_size=50)
    return superPixelImage
    

def getSuperPixels_Quickshift(image):
    # See [http://scikit-image.org/docs/dev/api/skimage.segmentation.html?highlight=slic#skimage.segmentation.quickshift]
    # image : (width, height, channels) ndarray.  Input image.
    # ratio : float, optional, between 0 and 1 (default 1). Balances color-space proximity and image-space proximity. Higher values give more weight to color-space.
    # kernel_size : float, optional (default 5). Width of Gaussian kernel used in smoothing the sample density. Higher means fewer clusters.
    # max_dist : float, optional (default 10). Cut-off point for data distances. Higher means fewer clusters.
    # return_tree : bool, optional (default False). Whether to return the full segmentation hierarchy tree and distances.
    # sigma : float, optional (default 0).  Width for Gaussian smoothing as preprocessing. Zero means no smoothing.
    # convert2lab : bool, optional (default True). Whether the input should be converted to Lab colorspace prior to segmentation. For this purpose, the input is assumed to be RGB.
    # random_seed : None (default) or int, optional. Random seed used for breaking ties.
    superPixelImage = skimage.segmentation.quickshift(image)
    return superPixelImage
    

def generateImageWithSuperPixelBoundaries(image, segmentationMask):
    # Function returns an image with superpixel boundaries displayed as lines.  It is assumed that the image was the source for the segmentation mask.
    # See [http://scikit-image.org/docs/dev/api/skimage.segmentation.html?highlight=slic#skimage.segmentation.mark_boundaries]
    # Function signature: skimage.segmentation.mark_boundaries(image, label_img, color=(1, 1, 0), outline_color=(0, 0, 0))
    superPixelImage = mark_boundaries(image, segmentationMask)
    return superPixelImage



def testSLIC_lenaRGB(numSuperPixels):
    lenaImg = skimage.data.lena()
    lena_superPixels_SLIC = generateImageWithSuperPixelBoundaries(lenaImg, getSuperPixels_SLIC(lenaImg, numSuperPixels) )
    displayImage(lena_superPixels_SLIC, imgTitle="Lena SLIC" , orientation="upper")
    
def testGraph_lenaRGB():
    lenaImg = skimage.data.lena()
    lena_superPixels_Graph = generateImageWithSuperPixelBoundaries(lenaImg, getSuperPixels_Graph(lenaImg) )
    displayImage(lena_superPixels_Graph, imgTitle="Lena Graph" , orientation= "upper")
    
def testQuickshift_lenaRGB():
    lenaImg = skimage.data.lena()	
    lena_superPixels_Quickshift = generateImageWithSuperPixelBoundaries(lenaImg, getSuperPixels_Quickshift(lenaImg) )
    displayImage(lena_superPixels_Quickshift, imgTitle="Lena Quickshift" , orientation="upper")


def testSuperPixelOnImage(image, superPixelAlgoName):
    if (superPixelAlgoName == "SLIC" or superPixelAlgoName == "Quickshift" or superPixelAlgoName == "Graph" ):
        print "\tINFO: Using " + str(superPixelAlgoName) + " with default settings to generate superpixel over-segmentation"
    else:
        print "\tWARN: Defaulting to SLIC algorithm with default settings to generate superpixel over-segmentation"
    
    if(superPixelAlgoName == "SLIC"):
        displayImage( generateImageWithSuperPixelBoundaries(image, getSuperPixels_SLIC(image, 400) ) , imgTitle="Car SLIC" , orientation="lower" )
    elif(superPixelAlgoName == "Quickshift"):
        displayImage( generateImageWithSuperPixelBoundaries(image, getSuperPixels_Quickshift(image) ) , imgTitle="Car Quickshift" , orientation="lower" )
    elif(superPixelAlgoName == "Graph"):
        displayImage( generateImageWithSuperPixelBoundaries(image, getSuperPixels_Graph(image) ) , imgTitle="Car Graph" , orientation="lower" )



def testSLIC_broomBroomRGB(carImg):
    testSuperPixelOnImage(carImg, "SLIC")


def testGraph_broomBroomRGB(carImg):
    testSuperPixelOnImage(carImg, "Graph")


def testQuickshift_broomBroomRGB(carImg):
    testSuperPixelOnImage(carImg, "Quickshift")



if __name__ == "__main__":
    # Examples on lena.png from skimage
    print "Oversegmentation examples will be displayed."
    print "\tOversegmentation with lena.png:\n"
    
    testSLIC_lenaRGB(400)
    testGraph_lenaRGB()
    testQuickshift_lenaRGB()
    
    # Examples on car image (idx ) from MSRC
    print "\tOversegmentation with car image from MSRC dataset::\n"
    msrcData = sys.argv[1] #"/home/amb/dev/mrf/data/MSRC_ObjCategImageDatabase_v2"
    carImg = pomio.msrc_loadImages(msrcData, ['Images/7_3_s.bmp'] )[0].m_img
    print "\tSLIC algo:"
    testSLIC_broomBroomRGB(carImg)
    
    print "\tGraph algo:"
    testGraph_broomBroomRGB(carImg)

    print "\tQuickshift algo:"
    testQuickshift_broomBroomRGB(carImg)
    
    print "Test examples complete."