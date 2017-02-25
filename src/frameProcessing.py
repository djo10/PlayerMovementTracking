import cv2
from skimage.measure import label
from skimage.measure import regionprops
import numpy as np
from player import *

class Player:
    def __init__(self, number, team, pic):
        self.number = number
        self.coords = []
        self.team = team
        self.pic = pic
        self.avg = (0. , 0.)
        self.avgPosPic = None




def frameProcessing(frames, model, batch_size, kmeans):
    count = 0
    players = []
    for frame in frames:
        im = cv2.imread(frame)
        im = im[185:780, 260:1180]

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # TOZERO / BINARY

        labeled_img = label(thresh)
        regions = regionprops(labeled_img)

        pas = False
        for region in regions:
            if pas:
                pas = False
                continue

            bbox = region.bbox
            h = bbox[2] - bbox[0]  # visina
            w = bbox[3] - bbox[1]  # sirina
            if float(h) == 8 and 2 <= float(w) <= 6:

                crop = thresh[bbox[0]:bbox[2], bbox[1]:bbox[3]]
                center = ((bbox[0] + bbox[2]) / 2), ((bbox[1] + bbox[3]) / 2)

                slika = obrada(crop)

                boja = im[bbox[0] - 2][(bbox[1] + bbox[3]) / 2]

                if 2 <= w <= 3:
                    numero = [1]
                else:
                    numero = model.predict_classes(slika, batch_size=batch_size)

                if region.label == len(regions):
                    slicica1 = im[center[0] - 8:center[0] + 8, center[1] - 8:center[1] + 8]
                    team = kmeans.predict(boja.tolist())

                    found = True
                    for i in players:
                        if i.number == numero[0] and i.team == team:
                            i.coords.append(center)
                            found = False
                            break
                    if found:
                        igrac = Player(numero[0], team, slicica1)
                        igrac.coords.append(center)
                        players.append(igrac)

                    continue
                next = regions[region.label]

                bbox1 = next.bbox
                hh = bbox1[2] - bbox1[0]  # visina
                ww = bbox1[3] - bbox1[1]  # sirina

                if hh == 8 and 2 <= float(ww) <= 6 and bbox[0] == bbox1[0] and bbox[2] == bbox1[2] and bbox[3] + 1 == \
                        bbox1[1]:
                    crop2 = thresh[bbox1[0]:bbox1[2], bbox1[1]:bbox1[3]]

                    center2 = ((bbox1[0] + bbox1[2]) / 2), ((bbox[1] + bbox1[3]) / 2)

                    sl = obrada(crop2)

                    if 2 <= ww <= 3:
                        numero1 = [1]
                    else:
                        numero1 = model.predict_classes(sl, batch_size=batch_size)

                    boja2 = im[bbox1[0] - 2][(bbox[1] + bbox1[3]) / 2]

                    slicica = im[center2[0] - 8:center2[0] + 8, center2[1] - 8:center2[1] + 8]

                    broj = numero[0] * 10 + numero1[0]
                    tm = kmeans.predict(boja2.tolist())

                    found = True
                    for i in players:
                        if i.number == broj and i.team == tm:
                            i.coords.append(center2)
                            found = False
                            break
                    if found:
                        igrac = Player(broj, tm, slicica)
                        igrac.coords.append(center2)
                        players.append(igrac)
                    pas = True

                else:
                    slicica1 = im[center[0] - 8:center[0] + 8, center[1] - 8:center[1] + 8]
                    team = kmeans.predict(boja.tolist())

                    found = True
                    for i in players:
                        if i.number == numero[0] and i.team == team:
                            i.coords.append(center)
                            found = False
                            break
                    if found:
                        igrac = Player(numero[0], team, slicica1)
                        igrac.coords.append(center)
                        players.append(igrac)

        print count
        count+=1
    return players


def draw_regions(regs, img_size):
    img_r = np.ndarray((img_size[0], img_size[1]), dtype='float32')
    for reg in regs:
        coords = reg.coords
        for coord in coords:
            img_r[coord[0], coord[1]] = 1.
    return img_r

def obrada(image):
    image = cv2.resize(image, (16, 16))

    pixels = []
    for i in range(6 * 28):
        pixels.append(0.)

    for r in image:
        for i in range(6):
            pixels.append(0.)
        for col in r:
            pixels.append(float(col) / 255.)
        for i in range(6):
            pixels.append(0.)
    for i in range(6 * 28):
        pixels.append(0.)

    slika = np.array(pixels)
    slika = np.array([slika])

    return slika


def prepareKmeans(frames):
    n = len(frames)-3
    x=n/3
    l=[1, x,x*2,x*3]
    colors = []
    for i in l:
        im = cv2.imread(frames[i])
        im = im[185:780, 260:1180]

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # TOZERO / BINARY

        labeled_img = label(thresh)
        regions = regionprops(labeled_img)

        pas =False
        for region in regions:
            if pas:
                pas = False
                continue

            bbox = region.bbox
            h = bbox[2] - bbox[0]  # visina
            w = bbox[3] - bbox[1]  # sirina
            if float(h) == 8 and 2 <= float(w) <= 6:

                boja = im[bbox[0] - 2][(bbox[1] + bbox[3]) / 2]

                if region.label == len(regions):
                    colors.append(boja.tolist())
                    continue
                next = regions[region.label]

                bbox1 = next.bbox
                hh = bbox1[2] - bbox1[0]  # visina
                ww = bbox1[3] - bbox1[1]  # sirina

                if hh == 8 and 2 <= float(ww) <= 6 and bbox[0] == bbox1[0] and bbox[2] == bbox1[2] and bbox[3] + 1 == bbox1[1]:
                    crop2 = thresh[bbox1[0]:bbox1[2], bbox1[1]:bbox1[3]]

                    boja2 = im[bbox1[0] - 2][(bbox[1] + bbox1[3]) / 2]

                    colors.append(boja2.tolist())
                    pas = True
                else:
                    colors.append(boja.tolist())

    return colors


def calculateAvgPos(igraci, frlen):
    out =[]
    for i in range(len(igraci)):
        if len(igraci[i].coords)< frlen*0.5:
            out.append(i)

    for i in reversed(out):
        igraci.pop(i)
    for igrac in igraci:
        r=0
        c=0
        for point in igrac.coords:
           r+=point[0]
           c+=point[1]
        igrac.avg=(r/len(igrac.coords), c/len(igrac.coords))
