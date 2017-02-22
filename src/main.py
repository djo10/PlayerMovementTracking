from videoparser import *
from frameProcessing import *
from knn import *

video = '../data/videos/video.avi'
frameslocation = '../data/frames'

if __name__ == "__main__":

    # frames = videoParser(video, frameslocation)
    #
    # print frames
    #
    # frameProcessing(frames)
    #
    # print frames
    # print len(frames)






    trainingset = get_training_set()

    im = cv2.imread(frameslocation+'/frame174.jpg')

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (5, 5), 0)

    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # TOZERO / BINARY

    cv2.imshow('OriginalImage', thresh)
    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyAllWindows()

    labeled_img = label(thresh)
    regions = regionprops(labeled_img)

    print len(regions)

    regions_players = []
    count=0
    for region in regions:
        bbox = region.bbox
        h = bbox[2] - bbox[0]  # visina
        w = bbox[3] - bbox[1]  # sirina
        # print h, w, region.label, bbox

        # plt.imshow(region.image, 'gray')
        # plt.show()
        if float(h) ==8:  # IZDVAJAJU SE REGIONI KOJI PREDSTAVLJAJU IGRACE U OBLIKU KUGLICA SA BROJEM
            # if (h == 16):
            #     cv2.imwrite("../data/players/player%d.jpg" % count, region.image)
            crop = thresh[bbox[0]:bbox[2], bbox[1]:bbox[3]]

            resized_image = cv2.resize(crop, (28, 28))



            # grayc = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            #
            # retc, cc = cv2.threshold(grayc, 127, 255, cv2.THRESH_BINARY)  # TOZERO / BINARY
            # print crop.dtype
            # print crop.shape
            # print resized_image.shape
            # print resized_image


            # print resized_image
            # a = np.array(resized_image)
            # print a.flatten()
            # print resized_image.flatten()
            data = Digit()
            for r in resized_image:
                for col in r:
                    data.data.append(int(col))
            data.init()
            # print data.data

            results = []
            for train in trainingset:
                distance = data.distance(train)
                touple = distance, train
                results.append(touple)
            results = sorted(results, key=lambda result: result[0])
            labelmap = {}
            for y in range(0, 51):
                result = results[y]
                l = result[1].label
                if l in labelmap:
                    labelmap[l] += 1
                else:
                    labelmap[l] = 1
            labelmap = sorted(labelmap.iteritems(), key=operator.itemgetter(1), reverse=True)
            print labelmap, labelmap[0][0]

            cv2.imshow('OriginalImage', resized_image)
            k = cv2.waitKey(0)
            if k == 27:
                cv2.destroyAllWindows()
            # plt.imshow(thresh)
            # plt.show()
            # print region.coords
            regions_players.append(region)
        count+=1

    print len(regions_players)

    for reg in regions_players:  # za svaku kuglicu opet pretrazivati regione koji ce predstavljati brojeve
        pass

    plt.imshow(draw_regions(regions_players, gray.shape), 'gray')
    # plt.imshow(im)
    plt.show()

    # reg1 = regions_players[0]
    # reg2 = regions_players[2]
    # reg3 = regions_players[3]
    # reg4 = regions_players[4]

    # grayreg = cv2.cvtColor(reg1, cv2.COLOR_BGR2GRAY)

    # ret, threshreg = cv2.threshold(reg1, 127, 255, cv2.THRESH_BINARY)

    # plt.imshow(reg2.image, 'gray')
    # plt.show()

