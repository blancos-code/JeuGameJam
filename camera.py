class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0      
    


    def getXPosition(self):
        return self.x

    def getYPosition(self):
        return self.y

    def getPosition(self):
        return self.x, self.y;

    def setPosition(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos