from videoparser import *
from frameProcessing import *

video = '../data/videos/video.avi'
frameslocation = '../data/frames'

if __name__ == "__main__":

    frames = videoParser(video, frameslocation)

    print frames

    frameProcessing(frames)

    print frames
    print len(frames)







    #
    # im = cv2.imread(frameslocation+'/frame222.jpg')
    #
    # gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #
    # ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # TOZERO / BINARY
    #
    # # cv2.imshow('OriginalImage', thresh)
    # # k = cv2.waitKey(0)
    # # if k == 27:
    # #     cv2.destroyAllWindows()
    #
    # labeled_img = label(thresh)
    # regions = regionprops(labeled_img)
    #
    # print len(regions)
    #
    # regions_players = []
    # count=0
    # for region in regions:
    #     bbox = region.bbox
    #     h = bbox[2] - bbox[0]  # visina
    #     w = bbox[3] - bbox[1]  # sirina
    #     # print h, w, region.coords
    #     #
    #     # plt.imshow(region.image, 'gray')
    #     # plt.show()
    #     if float(h) == w:  # IZDVAJAJU SE REGIONI KOJI PREDSTAVLJAJU IGRACE U OBLIKU KUGLICA SA BROJEM
    #         # if (h == 16):
    #         #     cv2.imwrite("../data/players/player%d.jpg" % count, region.image)
    #         #     plt.imshow(region.image, 'gray')
    #         #     plt.show()
    #             regions_players.append(region)
    #     count+=1
    #
    # print len(regions_players)
    #
    # for reg in regions_players:  # za svaku kuglicu opet pretrazivati regione koji ce predstavljati brojeve
    #     pass
    #
    # plt.imshow(draw_regions(regions_players, gray.shape), 'gray')
    # # plt.imshow(im)
    # plt.show()
    #
    # # reg1 = regions_players[0]
    # # reg2 = regions_players[2]
    # # reg3 = regions_players[3]
    # # reg4 = regions_players[4]
    #
    # # grayreg = cv2.cvtColor(reg1, cv2.COLOR_BGR2GRAY)
    #
    # # ret, threshreg = cv2.threshold(reg1, 127, 255, cv2.THRESH_BINARY)
    #
    # # plt.imshow(reg2.image, 'gray')
    # # plt.show()
    #
