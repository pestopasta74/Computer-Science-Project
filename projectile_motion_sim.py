import pygame
from sys import exit
from colourBank import Colour
from projectile_physics import physics_sim
import math
import random


# Functions
def infoBarCreate(windowWidth, windowHeight,radAngle,inputVelocity,hVelocity,vVelocity,resolution):
    # Constant
    infoBarWidth = int(windowWidth)
    infoBarHeight = int(windowHeight / 3)
    infoBar = pygame.Surface((infoBarWidth, infoBarHeight))
    infoBar.fill(colours.darkGrey)
    borderLine = pygame.draw.line(infoBar, colours.white, (0, 0), (infoBarWidth, 0), 2)
    scaleLineLength = 30

    # Makes the scale
    for multiplier in range(1, int(windowWidth / 100)):
        lineXpos = infoBarWidth * multiplier / (windowWidth / 100)
        scaleLine = pygame.draw.line(infoBar, colours.white, (lineXpos, 0), (lineXpos, scaleLineLength), 2)
        measurement = (multiplier - int(windowWidth / 200)) * resolution
        scaleTextBox = baseFont.render(f"{str(measurement)} m", False, colours.white)
        scaleTextBoxRect = scaleTextBox.get_rect(midtop = (lineXpos, scaleLineLength + 10))
        infoBar.blit(scaleTextBox, scaleTextBoxRect)

    # Text subject to change
    textOffSet = 100

    degAngle = radAngle * 180 / math.pi
    displayDegAngle = math.floor(degAngle)
    angleBox = baseFont.render(f"Firing Angle: {displayDegAngle} Degrees", True, colours.white)
    angleBoxRect = angleBox.get_rect(midtop = (infoBarWidth / 6 * 1, 0 + textOffSet))
    infoBar.blit(angleBox, angleBoxRect)

    displayVelocity = math.floor(inputVelocity)
    velocityBox = baseFont.render(f"Input Velocity: {displayVelocity} m/s", True, colours.white)
    velocityBoxRect = velocityBox.get_rect(midtop = (infoBarWidth / 6 * 3, 0 + textOffSet))
    infoBar.blit(velocityBox, velocityBoxRect)

    horizontalRange, maxHeight = physics_sim(inputVelocity,degAngle)

    dislayMaxHeight = math.floor(maxHeight)
    maxHeightBox = baseFont.render(f"Max Height: {dislayMaxHeight} m", True, colours.white)
    maxHeightBoxRect = maxHeightBox.get_rect(midtop = (infoBarWidth / 6 * 5, 0 + textOffSet))
    infoBar.blit(maxHeightBox, maxHeightBoxRect)

    displayHorizontalRange = math.floor(math.sqrt(horizontalRange ** 2))
    xRangeBox = baseFont.render(f"Horizontal Range: {displayHorizontalRange} m", True, colours.white)
    xRangeBoxRect = xRangeBox.get_rect(midtop = (infoBarWidth / 6 * 1, infoBarHeight / 3 + textOffSet))
    infoBar.blit(xRangeBox, xRangeBoxRect)

    displayHVelocity = math.floor(math.sqrt(hVelocity ** 2))
    hvBox = baseFont.render(f"Horizontal Velocity: {displayHVelocity} m/s", True, colours.white)
    hvBoxRect = hvBox.get_rect(midtop = (infoBarWidth / 6 * 3, infoBarHeight / 3 + textOffSet))
    infoBar.blit(hvBox, hvBoxRect)

    displayVVelocity = math.floor(math.sqrt(vVelocity**2))
    vvBox = baseFont.render(f"Vertical Velocity: {displayVVelocity} m/s", True, colours.white)
    vvBoxRect = vvBox.get_rect(midtop = (infoBarWidth / 6 * 5, infoBarHeight / 3 + textOffSet))
    infoBar.blit(vvBox, vvBoxRect)

    return infoBar


def courtCreate(windowWidth, windowHeight, radius, radAngle):
    lineXOffSet, lineYOffSet = angleToCircumference(mouseAngle(circleCenter), radius)
    # Court
    courtWidth = int(windowWidth)
    courtHeight = int(windowHeight * 2 / 3)
    court = pygame.Surface((courtWidth, courtHeight))
    court.fill(colours.darkDarkGrey)

    # AngleCircle
    circleSurf = pygame.Surface((radius * 4, radius * 4))
    circleSurf.fill(colours.darkDarkGrey)
    pygame.draw.circle(circleSurf, colours.white, (radius * 2, radius * 2), radius, 2)
    pygame.draw.line(circleSurf, colours.white, (radius * 2,radius * 2), ((radius * 2) + lineXOffSet, (radius * 2) - lineYOffSet ), 2)

    # Angle text
    degAngle = math.floor(radAngle * 180 / math.pi)
    degAngleBox = baseFont.render(str(degAngle), False, colours.white)
    degAngleBoxRect = degAngleBox.get_rect(center = ((radius * 2 + lineXOffSet * 1.1), (radius * 2 - lineYOffSet * 1.1) - 10))
    circleSurf.blit(degAngleBox, degAngleBoxRect)

    #Final Court blit
    circleSurfRect = circleSurf.get_rect(center = (courtWidth / 2, courtHeight))
    court.blit(circleSurf, (circleSurfRect))

    return court


def trajectoryCreate(hVelocity, vVelocity, circleCenter, surface, windowHeight, resolution):
    x,y =  circleCenter
    vVelocity = vVelocity
    hVelocity = hVelocity
    gravity = 9.81 / resolution
    bounces = 0
    floor = windowHeight * 2 / 3

    while bounces < 6:
        if y > floor:
            y = floor - 1
            vVelocity = vVelocity * -0.7
            hVelocity = hVelocity * 0.7
            bounces += 1

        pygame.draw.circle(surface, colours.white, (x, y), 1)
        vVelocity -= gravity
        x += hVelocity
        y -= vVelocity

def mouseAngle(circleCenter):
    cursorX, cursorY = pygame.mouse.get_pos()
    centerX, centerY = circleCenter
    respectiveX = cursorX - centerX
    respectiveY = centerY - cursorY

    if respectiveY < 0:
        radAngle = 0
    else:
        if respectiveX == 0:
            radAngle = math.pi / 2
        elif respectiveX < 0:
            radAngle = math.pi + math.atan(respectiveY / respectiveX)
        elif respectiveX > 0:
            radAngle = math.atan(respectiveY / respectiveX)
    return radAngle


def angleToCircumference(radAngle, radius):
    y = radius * math.sin(radAngle)
    x = radius * math.cos(radAngle)
    return x, y


def inputVelocity(circleCenter):
    centerX, centerY = circleCenter
    cursorX, cursorY = pygame.mouse.get_pos()
    respectiveX = cursorX - centerX
    respectiveY = centerY - cursorY
    inputVelocity = math.sqrt((respectiveX ** 2) + (respectiveY ** 2))
    return inputVelocity / 15


# Framerate
frameRate = 60
clock = pygame.time.Clock()

# Stuff
colours = Colour()
windowWidth, windowHeight = 1200, 600
circleCenter = (windowWidth / 2, windowHeight * 2 / 3)
radius = 150
shooting = False
resolution = 10

# Screen Setup
pygame.init()
screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Projectile Motion Sim 3")

# Font
pygame.font.init()
baseFont = pygame.font.SysFont("helvetica", 20)

# Base objects and Surfaces
callum_planet = pygame.image.load("assets/Callum.png").convert_alpha()
preston_planet = pygame.image.load("assets/Preston.png").convert_alpha()


# Event Loop
while True:

    # Game ender
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Screen stuff
    hVelocity = inputVelocity(circleCenter) * math.cos(mouseAngle(circleCenter))
    vVelocity = inputVelocity(circleCenter) * math.sin(mouseAngle(circleCenter))
    infoBar = infoBarCreate(windowWidth, windowHeight, mouseAngle(circleCenter), inputVelocity(circleCenter), hVelocity, vVelocity, resolution)
    court = courtCreate(windowWidth, windowHeight, radius, mouseAngle(circleCenter))
    trajectory = trajectoryCreate(hVelocity, vVelocity, circleCenter, court, windowHeight, resolution)

    # Ball shooter
    if pygame.mouse.get_pressed() == (True, False, False) and shooting == False:
        # Planet Selector and general initialisation
        current_planet = random.choice([callum_planet, preston_planet])
        x,y =  circleCenter
        ballVVelocity = vVelocity * 1
        ballHVelocity = hVelocity * 1
        gravity = 9.81 / resolution
        bounces = 0
        floor = windowHeight / 3 * 2
        shooting = True

    #Movement
    if shooting:
        if y > floor:
            y = floor
            ballVVelocity = ballVVelocity * -0.7
            ballHVelocity = ballHVelocity * 0.7
            bounces += 1

        if bounces < 6:
            ballVVelocity -= gravity
            x += ballHVelocity
            y -= ballVVelocity

        else:
            shooting = False
            math.floor(ballVVelocity)

        # Drawing
        current_planet = pygame.transform.scale(current_planet, (30, 30))
        current_planetRect = current_planet.get_rect(midbottom = (x, y))
        court.blit(current_planet, current_planetRect)

    # Blitting to screen
    screen.blit(infoBar, (0, windowHeight * 2 / 3))
    screen.blit(court, (0, 0))

    # Updates and tickrate
    pygame.display.update()
    clock.tick(frameRate)
