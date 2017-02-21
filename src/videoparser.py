import cv2
from os import listdir, makedirs
from os.path import isfile, join, exists
import shutil

def videoParser(videopath, frameslocation):
    if (exists(frameslocation)):
        shutil.rmtree(frameslocation)
    makedirs(frameslocation)
    vidcap = cv2.VideoCapture(videopath)
    success,image = vidcap.read()
    count = 0
    success = True
    frames = []
    while success:

        cv2.imwrite(frameslocation + "/frame%d.jpg" % count, image)     # save frame as JPEG file
        frames.append(frameslocation + "/frame%d.jpg" % count)
        count += 1
        success, image = vidcap.read()
    return frames

def getFrames(path):
    frames = []
    for file in listdir(path):
        if (isfile(join(path, file)) and file.endswith('.jpg')):
            frames.append(join(path, file))

    return frames