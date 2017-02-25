import cv2
import numpy as np

def generateAvgTeam(players):
    template = cv2.imread('template2.jpg')
    template2 = cv2.imread('template2.jpg')
    # print template.shape
    # (595, 920, 3)
    template = template[10:555, 20:828]
    template2 = template2[10:555, 20:828]
    t = cv2.resize(template, (920, 595))
    t1 = cv2.resize(template2, (920, 595))

    for ig in players:
        for i in range(16):
            for j in range(16):
                if ig.team==0:
                    t[ig.avg[0] + i, ig.avg[1] + j] = ig.pic[i,j]
                else:
                    t1[ig.avg[0] + i, ig.avg[1] + j] = ig.pic[i, j]

    return t, t1


def genAvgPlayer(player):
    blank_image = np.zeros((595, 920, 3), np.uint8)
    blank_image[:, :] = (255, 255, 255)
    for c in player.coords:
        for i in range(c[0]-8, c[0]+8):
            for j in range(c[1]-8, c[1]+8):
                p = blank_image[i,j]
                if p[0]>=5:
                    p[0] = p[0]-5
                    blank_image[i,j]=p
                elif p[1]>=5:
                    p[1] = p[1] - 5
                    blank_image[i, j] = p
                elif p[2]>=5:
                    p[2] = p[2] - 5
                    blank_image[i, j] = p

    return blank_image

def getTeams(players):
    t1=[]
    t2=[]

    for p in players:
        if p.team==0:
            t1.append(p)
        else:
            t2.append(p)

    return t1,t2