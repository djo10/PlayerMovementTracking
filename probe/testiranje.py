import matplotlib.pyplot as plt
import numpy as np

from skimage.io import imread
from skimage.color import rgb2gray

from skimage.measure import label
from skimage.measure import regionprops

from skimage.morphology import dilation, erosion, opening, closing

from skimage.morphology import square, diamond, disk

from skimage.filter.rank import threshold
from skimage.filter.rank import otsu


img = imread('frame61.jpg')

img_gray = rgb2gray(img)

img_tr = img_gray > 0.5
plt.imshow(img_tr, 'gray')
plt.show()


labeled_img = label(img_tr)
regions = regionprops(labeled_img)

def draw_regions(regs, img_size):
    img_r = np.ndarray((img_size[0], img_size[1]), dtype='float32')
    for reg in regs:
        coords = reg.coords  # coords vraca koordinate svih tacaka regiona
        for coord in coords:
            img_r[coord[0], coord[1]] = 1.
    return img_r

regions_barcode = []
for region in regions:
    bbox = region.bbox
    h = bbox[2] - bbox[0]  # visina
    w = bbox[3] - bbox[1]  # sirina

    if float(h) == w:
        plt.imshow(region.image, 'gray')
        plt.show()
        regions_barcode.append(region)

plt.imshow(draw_regions(regions_barcode, img_tr.shape), 'gray')

plt.show()