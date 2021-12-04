# This script does create a List of Lists and then "draws" a random path between two points.
# it is meant to be a "Lightning"

import random
import sys
import time
import utime

from machine import Pin
from neopixel import NeoPixel

# CLASSES # Function for corners, that need to be ignored, because they are not existing in real life (e.g. Corners of a room)

class point:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
    def drawthethingfunction(self, feld, thing):
        feld[self.y][self.x] = thing
    def getthething(self, feld):
        if self.x > spaltenanzahl-1 or self.y > zeilenanzahl-1 or (self.x < 0 or self.y < 0):
            return "#"
        return feld[self.y][self.x]

class box: 
    def __init__(self, upperleftcorner: point, lowerrightcorner: point):
        self.upperleftcorner = upperleftcorner
        self.lowerrightcorner = lowerrightcorner
    def drawtheboxfunction(self, feld, thing):
        for y in range(self.upperleftcorner.y, self.lowerrightcorner.y+1):
            for x in range(self.upperleftcorner.x, self.lowerrightcorner.x+1):
                p = point(x,y)
                p.drawthethingfunction(feld, thing)

#Table of constants

wall = "#"
spaltenanzahl = 126
zeilenanzahl = 16
upperleftcorner1 = point(116,9)
lowerrightcorner1 = point(125,15)
upperleftcorner2 = point(0,12)
lowerrightcorner2 = point(20,15)
box1 = box(upperleftcorner2, lowerrightcorner2)
box2 = box(upperleftcorner1, lowerrightcorner1)
pin = Pin(23, Pin.OUT)
np = NeoPixel(pin, 1863, bpp=3)


# Utill functions
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('reality_of_things', 'o@ij7Y}:<-i+}S]=#1..*ew{#,n6(n2$fa1aD&SK')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def start_webrepl():
    import webrepl
    webrepl.start(password='Toilet,.,')

# Creates a  "field" of  the size chosen by the user.
# There is a class and a function for creating "boxes" where there are no "lights" or functions are not allowed to go
    
def feldmachen(zeilenanzahl, spaltenanzahl):
    feld = []
    for i in range(0, zeilenanzahl):
        zeile = []
        for j in range(0, spaltenanzahl):
            zeile.append(" ")
        feld.append(zeile)
    return feld        

# prints the field.

def felddrucken(feld):
    for i, pixel in enumerate(feld_to_led(feld)):
        np[i] = pixel
    np.write()

# Chooses random Spawnpoint and turn it "On".

def spawnpointfunction(feld, zeilenanzahl, spaltenanzahl):
    print("y1: " + str(utime.ticks_ms()))
    y = random.randint(0, zeilenanzahl-1)
    print("y2: " + str(utime.ticks_ms()))
    x = random.randint(0, spaltenanzahl-1)
    spawnpoint = point(x,y)
    if spawnpoint.getthething(feld) == wall:
        return spawnpointfunction(feld, zeilenanzahl, spaltenanzahl)
    return spawnpoint


# Chooses random Goalpoint. That can't be Spawnpoint.

def goalpointfunction(feld, zeilenanzahl, spaltenanzahl, spawnpoint):
    goalpoint = spawnpoint
    while goalpoint == spawnpoint or goalpoint.getthething(feld) == wall:
        goalpoint = spawnpointfunction(feld, zeilenanzahl, spaltenanzahl)
    return goalpoint

# Turns all of the points it gets on.

def turnonfunction(feld, point: point):
    point.drawthethingfunction(feld, "0")

# This turns "on" the goalpoint with a X. It is like a tresure to find.

def markgoalpoint(feld, point: point):
    point.drawthethingfunction(feld,"X")

#  If Spawnpoint is next to Goal: EXPLOSION! BOOOOOM! Possibly will blind people. ¯\_(ツ)_/¯

def explosionfunction(feld, goalpoint: point, spawnpoint: point):
    testgoalpoint = point(goalpoint.x,goalpoint.y)
    testgoalpoint.x = testgoalpoint.x-spawnpoint.x
    testgoalpoint.y = testgoalpoint.y-spawnpoint.y
    if abs(testgoalpoint.x)*abs(testgoalpoint.y) == 1 or abs(testgoalpoint.x)+abs(testgoalpoint.y) == 1 :
        explosion = []
        for i in range(0, zeilenanzahl):
            expzeile = []
            for j in range(0, spaltenanzahl):
                expzeile.append("0")
            explosion.append(expzeile)
        felddrucken(explosion)
        print("EXPLOSION! BOOOOOOOOM \(x‿x)/")     
        sys.exit(0)
    else:
        print("Keine Explosion. Puh!")     


# in preparation of stepping-function, i define a "is the goalpoint next to the current position"-function

def closetogoalfunction(goalpoint, currentpoint):
    testgoalpoint = point(goalpoint.x,goalpoint.y)
    testgoalpoint.x = testgoalpoint.x-currentpoint.x
    testgoalpoint.y = testgoalpoint.y-currentpoint.y
    if abs(testgoalpoint.x)*abs(testgoalpoint.y) == 1 or abs(testgoalpoint.x)+abs(testgoalpoint.y) == 1 :
        return True
    else:
        return False

def yougotmecorneredfunction(feld):
    felddrucken(feld)
    print("You are cornered.")
    sys.exit(0)

# All 8 Points surrounding the currentpoint will be checked, wether they are options to go to.

def whereshouldigofromherefunction(feld, goalpoint: point, currentpoint: point):
    possiblepointupperleft = point(currentpoint.x-1, currentpoint.y-1)
    possiblepointuppermid = point(currentpoint.x-0, currentpoint.y-1)
    possiblepointupperright = point(currentpoint.x+1, currentpoint.y-1)
    possiblepointleft = point(currentpoint.x-1, currentpoint.y-0)
    possiblepointright = point(currentpoint.x+1, currentpoint.y)
    possiblepointlowerleft = point(currentpoint.x-1, currentpoint.y+1)
    possiblepointlowermid = point(currentpoint.x, currentpoint.y+1)
    possiblepointlowerright = point(currentpoint.x+1, currentpoint.y+1)
    initialdistancedictionary = {possiblepointupperleft : 0, possiblepointuppermid : 0, possiblepointupperright : 0, possiblepointleft : 0, possiblepointright : 0, possiblepointlowerleft : 0, possiblepointlowermid : 0, possiblepointlowerright : 0}
    # From here on, the distance to the target point is calculated for each point. This is collected in a dictionary.
    distancevaluedictionary = {}
    for p in initialdistancedictionary:
        if p.getthething(feld) == " ":
            distancevaluedictionary[p] = pythagorasfunction(proximitytogoalfunction(goalpoint, p))    
    if not distancevaluedictionary:
        yougotmecorneredfunction(feld)

    print("pointtogoto 1: " + str(utime.ticks_ms()))    
    pointtogoto = calculateprobabilitiesandchooseanextpositionfunction(distancevaluedictionary)
    print("pointtogoto 2: " + str(utime.ticks_ms()))  
    #print("Point to go to: (%d, %d)" % (pointtogoto.x, pointtogoto.y))
    return pointtogoto

# As a part of whereshouldigofunction it finds out how many fields on the x-axis and y-axis are between currentpoint and goalpoint.

def proximitytogoalfunction(goalpoint: point, pointinquestion: point):
    y = abs(pointinquestion.y - goalpoint.y)
    x = abs(pointinquestion.x - goalpoint.x)
    return point(x, y)
#    return a point and give it to pythagorasfunciton

# pythagoras. You know him... 

def pythagorasfunction(numberoffieldstogo: point):
    a = numberoffieldstogo.x
    b = numberoffieldstogo.y
    c = (a**2+b**2)**0.5
    return c
    #gib c zu Liste

# Identifies out of the given list the point with the biggest distance to the goalpoint.

def whohasgotthebiggestfunction(dictionary):
    biggestdistancepointvalue = 0
    for point in dictionary:
        if dictionary[point] > biggestdistancepointvalue:
            biggestdistancepointvalue = dictionary[point]
    return biggestdistancepointvalue

# Great loope-de-woop-fun for a dictionary-formed-points-around-currentpoint-list. Returns a next point to go to.

def calculateprobabilitiesandchooseanextpositionfunction(distancevaluedictionary):
    if len(distancevaluedictionary) == 1:
        return next(iter(distancevaluedictionary))
    biggestdistancepointvalue = whohasgotthebiggestfunction(distancevaluedictionary)
    # Subtract the largest value from the values of all points. This makes the farthest point = 0 and the next point has the largest negative value.
    for point in distancevaluedictionary:
        distancevaluedictionary[point] = distancevaluedictionary[point] - biggestdistancepointvalue
    # Create of all points the absolute value. This gives the point with the smallest distance to the goal the largest positive value.
    for point in distancevaluedictionary:
        distancevaluedictionary[point] = abs(distancevaluedictionary[point]) 
    # Take the values of all points to the power of 2 (or any other value), so that the weighting of the point with the smallest distance increases.   
    for point in distancevaluedictionary:
        distancevaluedictionary[point] = distancevaluedictionary[point]**1.2
    # jetzt muss von allen Punkten die Summe der Werte errechnet werden um dann damit für jeden Punkt seinen Prozentwert vom gesamten zu errechnen, um dass das als die "Wahrscheinlichkeit" der Auswahl dieses Punktes zu nutzen.
    sumofalldistances = 0
    for point in distancevaluedictionary:
        sumofalldistances = sumofalldistances + distancevaluedictionary[point]
    # jetzt die Prozentwerte errechnen.
    for point in distancevaluedictionary:
        distancevaluedictionary[point] = (distancevaluedictionary[point] * 100) / sumofalldistances
    # jetzt die Werte zu int runden und in den "Lostopf schmeißen"
    for point in distancevaluedictionary:
        distancevaluedictionary[point] = round(distancevaluedictionary[point])
    drawpot = []
    for point in distancevaluedictionary:
        while distancevaluedictionary[point] != 0:
            drawpot.append(point)
            distancevaluedictionary[point] = distancevaluedictionary[point] - 1
    # jetzt zufällig einen Punkt aus dem Lostopf ziehen.
    chosensteptopoint = random.choice(drawpot)
    return chosensteptopoint

def gotothenextpointandmakeitshinefunction(feld, goalpoint, currentpoint):
    nextpointtogoto = whereshouldigofromherefunction(feld, goalpoint, currentpoint)
    currentpoint = nextpointtogoto
    turnonfunction(feld,currentpoint)
    felddrucken(feld)
    return feld, currentpoint

def makealightningfunction(feld, goalpoint, spawnpoint):
    currentpoint = spawnpoint
    while closetogoalfunction(goalpoint, currentpoint) == False:        
#        time.sleep(0.02)
        feld, currentpoint = gotothenextpointandmakeitshinefunction(feld, goalpoint, currentpoint)
    else:
        turnonfunction(feld,goalpoint)
        felddrucken(feld)
        sys.exit(0)

def feld_to_led(feld):
    fb = []
    for i, row in enumerate(feld):
        if i % 2 == 1:
            row = reversed(row)
        for cell in row:
            if cell == wall:
                continue
            if cell == " ":
                fb.append((0,0,0))
            if cell == "0" or cell == "X":
                fb.append((255,255,255))
    return fb

# this is where the magic happens!

def main():
    #do_connect()
    #start_webrepl()

    feld = feldmachen(zeilenanzahl, spaltenanzahl)

    box1.drawtheboxfunction(feld, wall)
    box2.drawtheboxfunction(feld, wall)

    felddrucken(feld)

    spawnpoint = spawnpointfunction(feld, zeilenanzahl, spaltenanzahl)
    goalpoint = goalpointfunction(feld, zeilenanzahl, spaltenanzahl, spawnpoint)

    print("Der Startpunkt liegt bei " + str(spawnpoint.x) + "," + str(spawnpoint.y) + ".")
    print("Der Zielpunkt liegt bei " + str(goalpoint.x) + "," + str(goalpoint.y)  + ".")

    turnonfunction(feld,spawnpoint)
    markgoalpoint(feld, goalpoint)
    felddrucken(feld)

    explosionfunction(feld, goalpoint, spawnpoint)

    # this is practically the main function

    makealightningfunction(feld, goalpoint, spawnpoint)

#if __name__ == "__main__":
while True:
    main()
#    time.sleep(random.randint(2,4))

