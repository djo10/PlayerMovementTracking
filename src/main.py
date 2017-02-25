from videoparser import *
from frameProcessing import *
from kmeans import *
from nn import *
import matplotlib.pyplot as plt  # za prikaz slika, grafika, itd.
from mpl_toolkits.mplot3d import Axes3D
from generateresults import *


def getmenustr(teams):
    s = ""
    s+= 30 * "-"+ " MENU "+ 30 * "-"
    s+= "\n    TEAM 1      \n"
    for i, player in enumerate(teams[0]):
        s+= str(i+1)+". "+str(player.number)+'\n'

    s+="\n    TEAM 2     \n "
    for i, player in enumerate(teams[1]):
        s+=str(i+1)+". "+str(player.number)+'\n'

    s+=67 * "-"
    return s

video = '../data/videos/tottenham.flv'
frameslocation = '../data/frames'
resultlocation = '../data/results'

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

    if (exists(resultlocation)):
        shutil.rmtree(resultlocation)
    makedirs(resultlocation)

    teamPics = generateAvgTeam(players)

    for p in players:
        genAvgPlayer(p)

    teams = getTeams(players)

    strmenu = getmenustr(teams)

    loop = True

    while loop:  ## While loop which will keep going until loop = False
        print strmenu  ## Displays menu
        choice = raw_input("Enter your choice: 1 or 2 for team or teamnum-playeridx for player: ")
        choice = choice.split("-")
        # print choice.split("-")
        print choice

        if int(choice[0])==0:
            loop = False
        elif len(choice) == 1:
            # str = "Team "+choice[0]+" Average Formation"
            plt.imshow(teamPics[int(choice[0])-1])
            plt.show()
            # cv2.imshow(str, teamPics[int(choice[0])-1])
            # k = cv2.waitKey(0) & 0xFF
            # if k == 27:
            #     cv2.destroyAllWindows()
        elif len(choice) == 2:
            pl = teams[int(choice[0])-1][int(choice[1])-1]
            # str = "Player " + pl.number + " from Team "+ pl.team+" average movement - Heat Map"
            plt.imshow(pl.avgPosPic)
            plt.show()
            # cv2.imshow(str, pl.avgPosPic)
            # k = cv2.waitKey(0) & 0xFF
            # if k == 27:
            #     cv2.destroyAllWindows()

        else:
            # Any integer inputs other than values 1-5 we print an error message
            raw_input("Wrong option selection. Enter any key to try again..")



    # cv2.imshow('OriginalImage', t1AvgPic)
    # k = cv2.waitKey(0)
    # if k == 27:
    #     cv2.destroyAllWindows()




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
