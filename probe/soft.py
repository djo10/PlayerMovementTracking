import matplotlib.pyplot as plt
import numpy as np

import cv2

from skimage.morphology import opening, closing
from skimage.morphology import square, diamond, disk

from skimage.io import imread
from skimage.color import rgb2gray
from skimage.measure import label
from skimage.measure import regionprops



# img = imread('girl.jpg')
#
# img2gray = rgb2gray(img)
#
#
# plt.imshow(img2gray, 'gray')
# plt.show()
# print img2gray.shape
# print img2gray.dtype


im = cv2.imread('frame170.jpg')

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

ret,thresh1 = cv2.threshold(gray ,127,255,cv2.THRESH_BINARY)


# cv2.imshow('OriginalImage', gray)
# cv2.imshow('OriginalImage', thresh1)

labeled_img = label(thresh1)
regions = regionprops(labeled_img)

print('Ukupan broj regiona: {}'.format(len(regions)))

def draw_regions(regs, img_size):
    img_r = np.ndarray((img_size[0], img_size[1]), dtype='float32')
    for reg in regs:
        coords = reg.coords
        for coord in coords:
            img_r[coord[0], coord[1]] = 1.
    return img_r

regions_barcode = []
for region in regions:
    bbox = region.bbox
    h = bbox[2] - bbox[0]  # visina
    w = bbox[3] - bbox[1]  # sirina
    if float(h) ==w:
        if(h == 16):
            regions_barcode.append(region)

print(len(regions_barcode))

ratios = []
for region in regions:
    bbox = region.bbox
    h = bbox[2] - bbox[0]  # visina
    w = bbox[3] - bbox[1]  # sirina
    ratio = float(h) / w
    ratios.append(ratio)

#n, bins, patches = plt.hist(ratios, bins=10)
#plt.show()

str_elem = disk(5)  # parametar je poluprecnik diska

#img_barcode_tr_cl = closing(thresh1, selem=str_elem)
#img_barcode_tr_cl = opening(thresh1, selem=square(3))

#plt.imshow(img_barcode_tr_cl, 'gray')
#plt.show()

#plt.imshow(draw_regions(regions_barcode, thresh1.shape), 'gray')
plt.imshow(im)
plt.show()

    # k = cv2.waitKey(0)
# if k == 27:
#     cv2.destroyAllWindows()



# VIDEO

# vidcap = cv2.VideoCapture('video.avi')
# success,image = vidcap.read()
# count = 0
# success = True
# while success:
#   success,image = vidcap.read()
#   print 'Read a new frame: ', success
#   cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
#   count += 1