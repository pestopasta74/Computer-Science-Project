import random


class Colour:
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)
        self.cyan = (0, 255, 255)
        self.magenta = (127, 0, 255)
        self.pink = (255, 0, 255)
        self.darkGrey = (30, 30, 30)
        self.darkDarkGrey = (15,15,15)

    def getRandomColour(self) -> tuple[int]:
        colourList = [
            self.red,
            self.green,
            self.blue,
            self.cyan, # it was aqua why did you change it to cyan you meanie
            self.magenta,
            self.yellow,
            self.pink
        ]
        return random.choice(colourList)
