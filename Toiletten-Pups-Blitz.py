# This script does create a List of Lists and then "draws" a random path between two points.
# it is meant to be a "Lightning"

import random
import sys

# Creates a  "field" of  the size chosen by the user.

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
    for zeile in feld:
        print(zeile)
    print()

# Chooses random Spawnpoint and turn it "On".

def spawnpointfunction(zeilenanzahl, spaltenanzahl):
    x = random.randint(0, zeilenanzahl-1)
    y = random.randint(0, spaltenanzahl-1)
    spawnpoint = [x,y]
    return spawnpoint


# Chooses random Goalpoint. That can't be Spawnpoint.

def goalpointfunction(zeilenanzahl, spaltenanzahl, spawnpoint):
    goalpoint = spawnpoint
    while goalpoint == spawnpoint:
        goalpoint = spawnpointfunction(zeilenanzahl, spaltenanzahl)
    return goalpoint

# Turns all of the points it gets on.

def turnonfunction(feld, point):
    feld[point[0]][point[1]] = "0"

# This turns "on" the goalpoint with a X. It is like a tresure to find.

def markgoalpoint(feld, point):
    feld[point[0]][point[1]] = "X"

#  If Spawnpoint is next to Goal: EXPLOSION! BOOOOOM! Possibly will blind people. ¯\_(ツ)_/¯

def explosionfunction(feld, goalpoint, spawnpoint):
    testgoalpoint = goalpoint.copy()
    testgoalpoint[0] = testgoalpoint[0]-spawnpoint[0]
    testgoalpoint[1] = testgoalpoint[1]-spawnpoint[1]
    if abs(testgoalpoint[0])*abs(testgoalpoint[1]) == 1 or abs(testgoalpoint[0])+abs(testgoalpoint[1]) == 1 :
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
    testgoalpoint = goalpoint.copy()
    testgoalpoint[0] = testgoalpoint[0]-currentpoint[0]
    testgoalpoint[1] = testgoalpoint[1]-currentpoint[1]
    if abs(testgoalpoint[0])*abs(testgoalpoint[1]) == 1 or abs(testgoalpoint[0])+abs(testgoalpoint[1]) == 1 :
        return True
    else:
        return False


# The following two functions want to check if the currentpoint cannot continue because it is trapped between "walls" or already entered fields.

def getvaluefunction(feld, coordinate):
    if coordinate[0] > zeilenanzahl-1 or coordinate[1] > spaltenanzahl-1 or (coordinate[0] < 0 or coordinate[1] < 0):
        return "0"
    else:
        value = feld[coordinate[0]][coordinate[1]]
        return value

def yougotmecorneredfunction(feld):
    felddrucken(feld)
    print("You are cornered.")
    sys.exit(0)

# All 8 Points surrounding the currentpoint will be checked, wether they are options to go to.

def whereshouldigofromherefunction(feld, currentpoint):
    possiblepointupperleft = (currentpoint[0]-1, currentpoint[1]-1)
    possiblepointuppermid = (currentpoint[0]-1, currentpoint[1]-0)
    possiblepointupperright = (currentpoint[0]-1, currentpoint[1]+1)
    possiblepointleft = (currentpoint[0]-0, currentpoint[1]-1)
    possiblepointright = (currentpoint[0]-0, currentpoint[1]+1)
    possiblepointlowerleft = (currentpoint[0]+1, currentpoint[1]-1)
    possiblepointlowermid = (currentpoint[0]+1, currentpoint[1]-0)
    possiblepointlowerright = (currentpoint[0]+1, currentpoint[1]+1)
    initialdistancedictionary = {possiblepointupperleft : 0, possiblepointuppermid : 0, possiblepointupperright : 0, possiblepointleft : 0, possiblepointright : 0, possiblepointlowerleft : 0, possiblepointlowermid : 0, possiblepointlowerright : 0}
    # From here on, the distance to the target point is calculated for each point. This is collected in a dictionary.
    distancevaluedictionary = {}
    for point in initialdistancedictionary:
        if getvaluefunction(feld, point) != "0":
            distancevaluedictionary[point] = pythagorasfunction(howmanyfieldstogofunction(goalpoint, point))    
    if not distancevaluedictionary:
        yougotmecorneredfunction(feld)
        
    pointtogoto = calculateprobabilitiesandchooseanextpositionfunction(distancevaluedictionary)
    print("Point to go to: (%d, %d)" % (pointtogoto[0], pointtogoto[1]))
    return pointtogoto

# As a part of whereshouldigofunction it fiends out how many fields on the x-axis and y-axis are between currentpoint and goalpoint.

def howmanyfieldstogofunction(goalpoint, pointinquestion):
    y = abs(pointinquestion[1] - goalpoint[1])
    x = abs(pointinquestion[0] - goalpoint[0])
    numberoffieldstogotuple = (x , y)
    return numberoffieldstogotuple
#    return a, b Tupel and give it to pythagorasfunciton

# pythagoras. You know him... 

def pythagorasfunction(numberoffieldstogotuple):
    a = numberoffieldstogotuple[0]
    b = numberoffieldstogotuple[1]
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
        distancevaluedictionary[point] = distancevaluedictionary[point]**1.4
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

def gotothenextpointandmakeitshinefunction(feld, currentpoint):
    nextpointtogoto = whereshouldigofromherefunction(feld, currentpoint)
    currentpoint = nextpointtogoto
    turnonfunction(feld,currentpoint)
    felddrucken(feld)
    return feld, currentpoint

def makealightningfunction(feld, goalpoint, spawnpoint):
    currentpoint = spawnpoint
    while closetogoalfunction(goalpoint, currentpoint) == False:        
        input("Press Enter to continue...")
        feld, currentpoint = gotothenextpointandmakeitshinefunction(feld, currentpoint)
    else:
        turnonfunction(feld,goalpoint)
        felddrucken(feld)
        sys.exit(0)

# this is where the magic happens!

print()
zeilenanzahl = int(input("Wie viele Zeilen soll das Feld haben? "))
spaltenanzahl = int(input("Wie viele Spalten soll das Feld haben? "))
print()
print("Das Feld hat " + str(zeilenanzahl) + " Zeilen und " + str(spaltenanzahl) + " Spalten.")
print()
        
feld = feldmachen(zeilenanzahl, spaltenanzahl)
felddrucken(feld)

spawnpoint = spawnpointfunction(zeilenanzahl, spaltenanzahl)
goalpoint = goalpointfunction(zeilenanzahl, spaltenanzahl, spawnpoint)

print("Der Startpunkt liegt bei " + str(spawnpoint) + ".")
print("Der Zielpunkt liegt bei " + str(goalpoint) + ".")

turnonfunction(feld,spawnpoint)
markgoalpoint(feld, goalpoint)
felddrucken(feld)

explosionfunction(feld, goalpoint, spawnpoint)

# this is practically the main function

makealightningfunction(feld, goalpoint, spawnpoint)
