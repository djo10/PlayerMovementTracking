from videoparser import *
from frameProcessing import *
from kmeans import *
from nn import *
import matplotlib.pyplot as plt  # za prikaz slika, grafika, itd.
from mpl_toolkits.mplot3d import Axes3D
from generateresults import *

video = '../data/videos/tottenham.flv'
frameslocation = '../data/frames'

batch_size = 128
nb_classes = 10
nb_epoch = 10

# K-Means za predikciju, kom timu pripada igrac na osnovu piksela(boje) 'dresa'
kmeans = KMeans(n_clusters=2, max_iter=100)

# model neuronske mreze za prepoznavanje broja igraca sa dresa (tj izdvojenog regiona slike)
model = trainandgetnn(batch_size, nb_epoch, nb_classes)

if __name__ == "__main__":

    print "Obradjivanje video snimka, generisanje frejmova..."

    #generisanje frejmova na osnovu odabranog snimka
    frames = videoParser(video, frameslocation)

    # formiranje podataka za kmeans
    tr = prepareKmeans(frames)

    kmeans.fit(tr, normalize=True)

    # obrada frejmova
    players = frameProcessing(frames, model, batch_size, kmeans)

    calculateAvgPos(players, len(frames))

    tAvgPic, t1AvgPic = generateAvgTeam(players)

    team1, team2 = getTeams(players)





    cv2.imshow('OriginalImage', t1AvgPic)
    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyAllWindows()





        #
        # blank_image = np.zeros((595, 920, 3), np.uint8)
        # blank_image[:, :] = (255, 255, 255)
        # for c in players[0].coords:
        #     # temp = blank_image[c[0]-4:c[0]+4, c[1]-4:c[0]+4]
        #     # blank_image[c[0]-4:c[0]+4, c[1]-4:c[0]+4] = (255, 255, 255)
        #     for i in range(c[0]-8, c[0]+8):
        #         for j in range(c[1]-8, c[1]+8):
        #             p = blank_image[i,j]
        #             if p[0]>=5:
        #                 p[0] = p[0]-5
        #                 blank_image[i,j]=p
        #             elif p[1]>=5:
        #                 p[1] = p[1] - 5
        #                 blank_image[i, j] = p
        #             elif p[2]>=5:
        #                 p[2] = p[2] - 5
        #                 blank_image[i, j] = p







        # colors = {0: 'red', 1: 'green'}
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # for idx, cluster in enumerate(kmeans.clusters):
    #     ax.scatter(cluster.center[0], cluster.center[1], cluster.center[2], c=colors[idx], marker='x', s=200)  # iscrtavanje centara
    #     for datum in cluster.data:  # iscrtavanje tacaka
    #         ax.scatter(datum[0], datum[1], datum[2], c=colors[idx])
    # ax.set_xlabel('R')
    # ax.set_ylabel('G')
    # ax.set_zlabel('B')
    #
    # plt.show()
    #



    #
    #
    # cv2.imshow('OriginalImage', t)
    # k = cv2.waitKey(0)
    # if k == 27:
    #     cv2.destroyAllWindows()
    #
    #
    # gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #
    # ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # TOZERO / BINARY
    #
    # labeled_img = label(thresh)
    # regions = regionprops(labeled_img)
    #
    # regions_players = []
    # count=0
    # xxx=[]
    # boje = np.array([np.array([0,0,0])])
    # boje = np.delete(boje, 0, 0)
    #
    # numbers=[]
    # pas = False
    # for region in regions:
    #     if pas:
    #         pas = False
    #         continue
    #
    #     bbox = region.bbox
    #     h = bbox[2] - bbox[0]  # visina
    #     w = bbox[3] - bbox[1]  # sirina
    #
    #     if h==8 and 2<=float(w)<=6:  # IZDVAJAJU SE REGIONI KOJI PREDSTAVLJAJU IGRACE U OBLIKU KUGLICA SA BROJEM
    #
    #         crop = thresh[bbox[0]:bbox[2], bbox[1]:bbox[3]]
    #
    #         center = ((bbox[0]+bbox[2])/2 ), ((bbox[1]+bbox[3])/2)
    #
    #
    #         slika = obrada(crop)
    #
    #         if 2<=w<=3:
    #             numero=[1]
    #         else:
    #             numero = model.predict_classes(slika, batch_size=batch_size)
    #
    #         boja = im[bbox[0]-2][(bbox[1]+bbox[3])/2]
    #
    #         if region.label ==len(regions):
    #             xxx.append(boja.tolist())
    #             boje = np.append(boje, np.array([boja]), axis=0)
    #             numbers.append(numero[0])
    #             slicica1 = im[center[0] - 8:center[0] + 8, center[1] - 8:center[1] + 8]
    #
    #             continue
    #         next = regions[region.label]
    #
    #         bbox1 = next.bbox
    #         hh = bbox1[2] - bbox1[0]  # visina
    #         ww = bbox1[3] - bbox1[1]  # sirina
    #         # print bbox1, next.label
    #
    #         if hh == 8 and 2 <= float(ww) <= 6 and bbox[0]==bbox1[0] and bbox[2]==bbox1[2] and bbox[3]+1==bbox1[1]:
    #             crop2 = thresh[bbox1[0]:bbox1[2], bbox1[1]:bbox1[3]]
    #
    #             center2 = ((bbox1[0] + bbox1[2]) / 2), ((bbox[1] + bbox1[3]) / 2)
    #             # print bbox1, hh, ww, center2
    #
    #             sl = obrada(crop2)
    #
    #             if 2 <= ww <= 3:
    #                 numero1 = [1]
    #             else:
    #                 numero1 = model.predict_classes(sl, batch_size=batch_size)
    #
    #             boja2 = im[bbox1[0] - 2][(bbox[1] + bbox1[3]) / 2]
    #
    #             xxx.append(boja2.tolist())
    #             boje = np.append(boje, np.array([boja2]), axis=0)
    #
    #             numbers.append(numero[0]*10+numero1[0])
    #             pas = True
    #             slicica = im[center2[0]-8:center2[0]+8, center2[1]-8:center2[1]+8]
    #
    #         else:
    #             xxx.append(boja.tolist())
    #             boje = np.append(boje, np.array([boja]), axis=0)
    #             numbers.append(numero[0])
    #             slicica1 = im[center[0] - 8:center[0] + 8, center[1] - 8:center[1] + 8]
    #
    #         # print numbers
    #         regions_players.append(region)
    #     count+=1
    #
    # cv2.imshow('OriginalImage', im)
    # k = cv2.waitKey(0)
    # if k == 27:
    #     cv2.destroyAllWindows()
    #
    #
    # # print len(regions_players)
    # # print boje
    # # print len(boje)
    # # print xxx
    # bb = copy.deepcopy(xxx)
    # # lista = bb.tolist()
    #
    # kmeans.fit(xxx, normalize=True)
    #
    # # for i in xrange(len(boje)):
    # #     print i,  kmeans.predict(lista[i]), boje[i], lista[i]
    #
    # print len(xxx)
    # print len(numbers)
    #
    # # for i in range(len(xxx)):
    # #     print kmeans.predict(bb[i]), numbers[i], xxx[i]
