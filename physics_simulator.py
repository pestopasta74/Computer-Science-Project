import pygame as pg
import sys
import numpy as np
import random
import math

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
G = 9.8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialize Pygame
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Physics Simulator")
clock = pg.time.Clock()