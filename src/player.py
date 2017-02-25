class Player:
    def __init__(self, number, team, pic):
        self.number = number
        self.coords = []
        self.team = team
        self.pic = pic
        self.avg = (0. , 0.)



class Number:
    def __init__(self, number, frame, color, center, kuglica):
        self.number = number
        self.color = color
        self.center = center
        self.frame = frame
        self.kuglica = kuglica