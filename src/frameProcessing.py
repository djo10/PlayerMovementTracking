import cv2
from skimage.measure import label
from skimage.measure import regionprops
import numpy as np
import matplotlib.pyplot as plt


def frameProcessing(frames):

    for frame in frames:
        print frame
        im = cv2.imread(frame)

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # TOZERO / BINARY

        # cv2.imshow('OriginalImage', thresh)
        # k = cv2.waitKey(0)
        # if k == 27:
        #     cv2.destroyAllWindows()

        labeled_img = label(thresh)
        regions = regionprops(labeled_img)

        regions_players = []
        for region in regions:
            bbox = region.bbox
            h = bbox[2] - bbox[0]  # visina
            w = bbox[3] - bbox[1]  # sirina
            if float(h) == w:      # IZDVAJAJU SE REGIONI KOJI PREDSTAVLJAJU IGRACE U OBLIKU KUGLICA SA BROJEM
                if (h == 16):
                    # plt.imshow(region.image, 'gray')
                    # plt.show()
                    regions_players.append(region)

        for reg in regions_players:     # za svaku kuglicu opet pretrazivati regione koji ce predstavljati brojeve
            pass

        # plt.imshow(draw_regions(regions_players, gray.shape), 'gray')
        # plt.imshow(im)
        # plt.show()


def draw_regions(regs, img_size):
    img_r = np.ndarray((img_size[0], img_size[1]), dtype='float32')
    for reg in regs:
        coords = reg.coords
        for coord in coords:
            img_r[coord[0], coord[1]] = 1.
    return img_r