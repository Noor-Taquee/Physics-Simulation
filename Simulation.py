from tkinter import Tk,Frame,Canvas,Label,Button,Entry,NSEW,N,S,E,W
from turtle import TurtleScreen,RawTurtle
from math import radians,cos,sin


#CLASSES=========================
class body:
    charge = 0
    mass = 0
    size = 0
    position = [0,0]
    color = "white"
    shape = "circle"
    velocity = 0
    dirOfVel = 0
    Yvelocity = 0
    Xvelocity = 0
    acceleration = 0
    dirOfAcc = 0
    Yacceleration = 0
    Xacceleration = 0
    cSin = 0
    cCos = 0
    defaultMass = 0
    defaultcharge = 0
    defaultPosition = [0,0]
    defaultVelocity = 0
    defaultDirOfVel = 0



#VARIABLES=======================
K = 9*(10**9)
G = 6.67/(10**11)

xCorrection = None
yCorrection = None

cOrientation = "portrait"
aOrientation = ""

duration = 0
timePrecision = 0.001

started = False
stopped = True
collided = False
updated = False
showPath = True
collision = True

electrostatics = False
gravitation = True

Celectrostatics = False
Cgravitation = True
tmp_g = False
tmp_e = False
Gforce = Kforce = 0

screenColor = "black"

infoSize = 7
infoFont = "arial"
infoLabelbg = "white"


entryLabelSize = 7
entryLabelFont = "arial"
entryLabelbg = "white"

entrySize = 6
entryWidth = 14
entryFont = "arial"

toggleSize = 5
toggleHeight = 1
toggleWidth = 1
toggleFont = "arial"

buttonSize = 10
buttonHeight = 1
buttonWidth = 1
buttonFont = "arial"

body1 = body()
body1.defaultcharge = 0
body1.defaultMass = 999999999999999
body1.defaultPosition = [250,0]
body1.defaultVelocity = 5000
body1.defaultDirOfVel = 90
body1.color = "orange"
body1.size = 1

body2 = body()
body2.defaultcharge = 0
body2.defaultMass = 99999999999999999999
body2.defaultPosition = [0,0]
body2.defaultVelocity = 0
body2.defaultDirOfVel = 0
body2.color = "yellow"
body2.size = 1

collisionDistance = 17
currentDistance = None

bodies = {}



#FUNCTIONS=========================
def createWindow():
    global window
    window = Tk()

def initiateTurtle():
    global screen,pen1,pen2,bodies
    screen = TurtleScreen(simArea)
    screen.bgcolor(screenColor)
    pen1 = RawTurtle(screen)
    pen1.hideturtle()
    pen2 = RawTurtle(screen)
    pen2.hideturtle()
    bodies = {body1:pen1,body2:pen2}

def checkOrientation(event = None):
    global cOrientation
    window.update_idletasks()
    height = window.winfo_height()
    width = window.winfo_width()
    if height > width:
        cOrientation = "portrait"
    else:
        cOrientation = "landscape"
    if cOrientation != aOrientation:
        changeLayout()

def changeLayout():
    global aOrientation,screenFrame,sidePanel,infoPanel,simulationPanel,controlPanel,entryPanel,buttonPanel
    for widget in window.winfo_children():
        widget.destroy()
    if cOrientation == "portrait":
        screenFrame = Frame(window)
        screenFrame.columnconfigure(0,weight = 1)
        screenFrame.rowconfigure(0,weight = 1)
        screenFrame.rowconfigure(1,weight = 40)
        screenFrame.rowconfigure(2,weight = 1)
        infoPanel = Frame(screenFrame,bg = "white")
        infoPanel.columnconfigure(0,weight = 1)
        infoPanel.columnconfigure(1,weight = 1)
        infoPanel.rowconfigure(0,weight = 1)
        infoPanel.rowconfigure(1,weight = 1)
        infoPanel.rowconfigure(2,weight = 1)
        simulationPanel = Frame(screenFrame,bg = "black")
        simulationPanel.columnconfigure(0,weight = 1)
        simulationPanel.rowconfigure(0,weight = 1)
        controlPanel = Frame(screenFrame,bg = "white")
        controlPanel.columnconfigure(0,weight = 1)
        controlPanel.rowconfigure(0,weight = 1)
        controlPanel.rowconfigure(1,weight = 1)
        buttonPanel = Frame(controlPanel,bg = "white")
        buttonPanel.columnconfigure(0,weight = 1)
        buttonPanel.columnconfigure(1,weight = 1)
        buttonPanel.columnconfigure(2,weight = 1)
        buttonPanel.columnconfigure(3,weight = 1)
        buttonPanel.rowconfigure(0,weight = 1)
        buttonPanel.rowconfigure(1,weight = 1)
        entryPanel = Frame(controlPanel,bg = "white")
        entryPanel.columnconfigure(0,weight = 1)
        entryPanel.columnconfigure(1,weight = 1)
        entryPanel.columnconfigure(2,weight = 1)
        entryPanel.rowconfigure(0,weight = 1)
        entryPanel.rowconfigure(1,weight = 1)
        entryPanel.rowconfigure(2,weight = 1)
        entryPanel.rowconfigure(3,weight = 1)
        entryPanel.rowconfigure(4,weight = 1)
        entryPanel.rowconfigure(5,weight = 1)
        #PLACEMENT
        screenFrame.pack(fill = "both",expand = True)
        infoPanel.grid(column = 0,row = 0,sticky = NSEW)
        simulationPanel.grid(column = 0,row = 1,sticky = NSEW)
        controlPanel.grid(column = 0,row = 2,sticky = NSEW)
        buttonPanel.grid(column = 0,row = 0,sticky = NSEW)
        entryPanel.grid(column = 0,row = 1,sticky = NSEW)
    else:
        screenFrame = Frame(window)
        screenFrame.columnconfigure(0,weight = 10)
        screenFrame.columnconfigure(1,weight = 1)
        screenFrame.rowconfigure(0,weight = 1)
        simulationPanel = Frame(screenFrame,bg = "black")
        simulationPanel.columnconfigure(0,weight = 1)
        simulationPanel.rowconfigure(0,weight = 1)
        sidePanel = Frame(screenFrame,bg = "white")
        sidePanel.columnconfigure(0,weight = 1)
        sidePanel.rowconfigure(0,weight = 1)
        sidePanel.rowconfigure(1,weight = 8)
        sidePanel.rowconfigure(2,weight = 5)
        infoPanel = Frame(sidePanel,bg = "white")
        infoPanel.columnconfigure(0,weight = 1)
        infoPanel.columnconfigure(1,weight = 1)
        infoPanel.rowconfigure(0,weight = 1)
        infoPanel.rowconfigure(1,weight = 1)
        infoPanel.rowconfigure(2,weight = 1)
        entryPanel = Frame(sidePanel,bg = "white")
        entryPanel.columnconfigure(0,weight = 1)
        entryPanel.columnconfigure(1,weight = 1)
        entryPanel.columnconfigure(2,weight = 1)
        entryPanel.rowconfigure(0,weight = 1)
        entryPanel.rowconfigure(1,weight = 1)
        entryPanel.rowconfigure(2,weight = 1)
        entryPanel.rowconfigure(3,weight = 1)
        entryPanel.rowconfigure(4,weight = 1)
        entryPanel.rowconfigure(5,weight = 1)
        buttonPanel = Frame(sidePanel,bg = "white")
        buttonPanel.columnconfigure(0,weight = 1)
        buttonPanel.columnconfigure(1,weight = 1)
        buttonPanel.columnconfigure(2,weight = 1)
        buttonPanel.columnconfigure(3,weight = 1)
        buttonPanel.rowconfigure(0,weight = 1)
        buttonPanel.rowconfigure(1,weight = 1)
        #PLACEMENT
        screenFrame.pack(fill = "both",expand = True)
        simulationPanel.grid(column = 0,row = 0,sticky = NSEW)
        sidePanel.grid(column = 1,row = 0,sticky = NSEW)
        infoPanel.grid(column = 0,row = 0,sticky = NSEW)
        entryPanel.grid(column = 0,row = 1,sticky = NSEW)
        buttonPanel.grid(column = 0,row = 2,sticky = NSEW)
    #CANVAS==========
    global simArea
    simArea = Canvas(simulationPanel)


    #MESSAGES========
    global body1Name,body1Vel,body2Name,body2Vel,distanceMeter,name1Entry,name2Entry,massEntry,velEntry,dirEntry,posEntry,timeDisplay
    #body1
    body1Name = Label(infoPanel,text = "BODY-I",font = (infoFont,infoSize),bg = infoLabelbg)
    body1Mass = Label(infoPanel,text = f"mass:{body1.mass}",font = (infoFont,infoSize),bg = infoLabelbg)
    body1Vel = Label(infoPanel,text = f"vel:{body1.velocity}",font = (infoFont,infoSize),bg = infoLabelbg)
    #body2
    body2Name = Label(infoPanel,text = "BODY-II",font = (infoFont,infoSize),bg = infoLabelbg)
    body2Mass = Label(infoPanel,text = f"mass:{body2.mass}",font = (infoFont,infoSize),bg = infoLabelbg)
    body2Vel = Label(infoPanel,text = f"vel:{body2.velocity}",font = (infoFont,infoSize),bg = infoLabelbg)
    
    distanceMeter = Label(infoPanel,text = f"distance: {currentDistance}",font = (infoFont,infoSize),bg = infoLabelbg)
    
    timeDisplay = Label(simArea,text = f"time: {round(duration,ndigits = 2)}",font = (infoFont,infoSize),bg = infoLabelbg)
    #entryLebels
    name1Entry = Label(entryPanel,text = "BODY-I",font = (entryLabelFont,entryLabelSize),bg = entryLabelbg)
    name2Entry = Label(entryPanel,text = "BODY-II",font = (entryLabelFont,entryLabelSize),bg = entryLabelbg)
    chargeEntry = Label(entryPanel,text = "charge:",font = (entryLabelFont,entryLabelSize),bg = entryLabelbg)
    massEntry = Label(entryPanel,text = "mass:",font = (entryLabelFont,entryLabelSize),bg = entryLabelbg)
    velEntry = Label(entryPanel,text = "velocity:",font = (entryLabelFont,entryLabelSize),bg = entryLabelbg)
    dirEntry = Label(entryPanel,text = "direction:",font = (entryLabelFont,entryLabelSize),bg = entryLabelbg)
    posEntry = Label(entryPanel,text = "X , Y:",font = (entryLabelFont,entryLabelSize),bg = entryLabelbg)

    #ENTRIES=========
    global charge1Entry,charge2Entry,mass1Entry,mass2Entry,vel1Entry,vel2Entry,dir1Entry,dir2Entry,x1Entry,x2Entry,y1Entry,y2Entry
    #body1
    charge1Entry = Entry(entryPanel,font = (entryFont,entrySize),width = entryWidth)
    mass1Entry = Entry(entryPanel,font = (entryFont,entrySize),width = entryWidth)
    vel1Entry = Entry(entryPanel,font = (entryFont,entrySize),width = entryWidth)
    dir1Entry = Entry(entryPanel,font = (entryFont,entrySize),width = entryWidth)
    x1Entry = Entry(entryPanel,font = (entryFont,entrySize),width = 1+entryWidth//2)
    y1Entry = Entry(entryPanel,font = (entryFont,entrySize),width = 1+entryWidth//2)
    #body2
    charge2Entry = Entry(entryPanel,font = (entryFont,entrySize),width = entryWidth)
    mass2Entry = Entry(entryPanel,font = (entryFont,entrySize),width = entryWidth)
    vel2Entry = Entry(entryPanel,font = (entryFont,entrySize),width = entryWidth)
    dir2Entry = Entry(entryPanel,font = (entryFont,entrySize),width = entryWidth)
    x2Entry = Entry(entryPanel,font = (entryFont,entrySize),width = 1+entryWidth//2)
    y2Entry = Entry(entryPanel,font = (entryFont,entrySize),width = 1+entryWidth//2)

    #BUTTONS=========
    global bn_stop,bn_start,bn_update,bn_G,bn_E
    bn_G = Button(buttonPanel,text = "• Gravitational Force",font = (toggleFont,toggleSize),fg = "black",height = toggleHeight,width = toggleWidth,bg = "white",command = f_G)
    bn_E = Button(buttonPanel,text = "  Electrostatic Force",font = (toggleFont,toggleSize),fg = "black",height = toggleHeight,width = toggleWidth,bg = "white",command = f_E)

    bn_stop = Button(buttonPanel,text = "STOP",font = (buttonFont,buttonSize),height = buttonHeight,width = buttonWidth,bg = "red",command = f_stop)
    bn_start = Button(buttonPanel,text = "START",font = (buttonFont,buttonSize),height = buttonHeight,width = buttonWidth,bg = "green",command = f_start)
    bn_update = Button(buttonPanel,text = "UPDATE",font = (buttonFont,buttonSize),height = buttonHeight,width = buttonWidth,bg = "orange",command = f_update)
    #==============PLACEMENT===============
    #Canvas
    simArea.grid(column = 0,row = 0,columnspan = 10,rowspan = 10,sticky = NSEW)
    #Messages
    body1Name.grid(column = 0,row = 0,sticky = NSEW)
    body1Vel.grid(column = 0,row = 1,sticky = NSEW)
    body2Name.grid(column = 1,row = 0,sticky = NSEW)
    body2Vel.grid(column = 1,row = 1,sticky = NSEW)
    distanceMeter.grid(column = 0,row = 2,columnspan = 2,sticky = NSEW)
    name1Entry.grid(column = 1,row = 0,sticky = NSEW)
    name2Entry.grid(column = 2,row = 0,sticky = NSEW)
    chargeEntry.grid(column = 0,row = 1,sticky = NSEW)
    massEntry.grid(column = 0,row = 2,sticky = NSEW)
    velEntry.grid(column = 0,row = 3,sticky = NSEW)
    dirEntry.grid(column = 0,row = 4,sticky = NSEW)
    posEntry.grid(column = 0,row = 5,sticky = NSEW)
    timeDisplay.grid(column = 0,row = 0,pady = 10,padx = 10,sticky = NSEW)
    #Entries
    charge1Entry.grid(column = 1,row = 1,sticky = NSEW)
    mass1Entry.grid(column = 1,row = 2,sticky = NSEW)
    vel1Entry.grid(column = 1,row = 3,sticky = NSEW)
    dir1Entry.grid(column = 1,row = 4,sticky = NSEW)
    x1Entry.grid(column = 1,row = 5,sticky = N+S+E)
    y1Entry.grid(column = 1,row = 5,sticky = N+S+W)
    charge2Entry.grid(column = 2,row = 1,sticky = NSEW)
    mass2Entry.grid(column = 2,row = 2,sticky = NSEW)
    vel2Entry.grid(column = 2,row = 3,sticky = NSEW)
    dir2Entry.grid(column = 2,row = 4,sticky = NSEW)
    x2Entry.grid(column = 2,row = 5,sticky = N+S+E)
    y2Entry.grid(column = 2,row = 5,sticky = N+S+W)
    #Buttons
    bn_stop.grid(column = 0,row = 0,sticky = NSEW)
    bn_start.grid(column = 1,row = 0,columnspan = 2,sticky = NSEW)
    bn_update.grid(column = 3,row = 0,sticky = NSEW)
    bn_G.grid(column = 0,row = 1,columnspan = 2,sticky = NSEW)
    bn_E.grid(column = 2,row = 1,columnspan = 2,sticky = NSEW)
    aOrientation = cOrientation
    correctCordinates()
    initiateTurtle()
    stopped = True
    f_update()

def correctCordinates():
    global xCorrection,yCorrection
    if aOrientation == "portrait":
        xCorrection = 270
        yCorrection = -180
    else:
        xCorrection = -50
        yCorrection = -50

def setTurtle():
    for i in bodies:
        bodies[i].speed(0)
        bodies[i].color(i.color)
        bodies[i].shape(i.shape)
        bodies[i].up()
        bodies[i].goto(i.position[0]+xCorrection,i.position[1]+yCorrection)
        bodies[i].showturtle()
        if showPath:
            bodies[i].down()

def restoreDefault():
    for i in bodies:
        i.mass = i.defaultMass
        i.velocity = i.defaultVelocity
        i.position = i.defaultPosition
        i.dirOfVel = i.defaultDirOfVel

def collide():
    global collided,stopped
    stopped = True
    explosion = RawTurtle(screen)
    explosion.hideturtle()
    pen1.clear()
    pen1.hideturtle()
    pen2.clear()
    pen2.hideturtle()
    explosion.shape("circle")
    explosion.speed(0)
    explosion.up()
    x = (body1.position[0]+body2.position[0])/2
    y = (body1.position[1]+body2.position[1])/2
    explosion.goto(x+xCorrection,y+yCorrection)
    explosion.showturtle()
    for size in range(1,100,5):
        tr = 1-(size/100)
        explosion.shapesize(size/10)
        explosion.color((1.0*tr,0.5*tr,0.0*tr))
    explosion.hideturtle()
    collided = True

def startPhysics():
    for i in bodies:
        i.Xvelocity = i.velocity*cos(radians(i.dirOfVel))
        i.Yvelocity = i.velocity*sin(radians(i.dirOfVel))

def updateVariables():
    global currentDistance,stopped,duration
    x1,y1 = body1.position
    x2,y2 = body2.position
    currentDistance = (((x1-x2)**2)+((y1-y2)**2))**0.5
    perp = y2-y1
    base = x2-x1
    hypo = ((perp**2)+(base**2))**0.5
    try:
        body1.cSin = perp/hypo
    except ZeroDivisionError:
        body1.cSin = 0
    try:
        body1.cCos = base/hypo
    except ZeroDivisionError:
        body1.cCos = 1
    body2.cCos = -body1.cCos
    body2.cSin = -body1.cSin
    if currentDistance > 3000:
        stopped = True
    elif currentDistance < collisionDistance:
        if collision and not collided and not stopped:
            collide()
        else:
            changeForce("disable")
    else:
        changeForce("enable")
    
    duration += timePrecision
    timeDisplay.config(text = f"time: {round(duration,ndigits = 2)}")
    distanceMeter.config(text = f"distance: {round(currentDistance,ndigits = 2)}")
    body1.velocity = (((body1.Xvelocity)**2)+((body1.Yvelocity)**2))**0.5
    body2.velocity = (((body2.Xvelocity)**2)+((body2.Yvelocity)**2))**0.5
    body1Vel.config(text = f"vel: {round(body1.velocity,ndigits = 2)}")
    body2Vel.config(text = f"vel: {round(body2.velocity,ndigits = 2)}")

def changeForce(order):
    global gravitation,electrostatics,tmp_g,tmp_e
    if order == "disable":
        if gravitation:
            gravitation = False
            tmp_g = True
        if electrostatics:
            electrostatics = False
            tmp_e = True
    else:
        if tmp_g:
            gravitation = True
            tmp_g = False
        if tmp_e:
            electrostatics = True
            tmp_e = False

def animate():
    global Gforce,Kforce
    updateVariables()
    if not stopped:
        if gravitation:
            Gforce = G*(body1.mass)*(body2.mass)/((currentDistance)**2)
        else:
            Gforce = 0
        if electrostatics:
            Kforce = -K*(body1.charge)*(body2.charge)/(currentDistance)**2
        else:
            Kforce = 0
        force = Gforce+Kforce
        for i in bodies:
            i.acceleration = force/i.mass
            i.Xacceleration = (i.cCos)*(i.acceleration)
            i.Yacceleration = (i.cSin)*(i.acceleration)
            i.Xvelocity += (i.Xacceleration)*timePrecision
            i.Yvelocity += (i.Yacceleration)*timePrecision
            i.position[0] += (i.Xvelocity)*timePrecision
            i.position[1] += (i.Yvelocity)*timePrecision
            bodies[i].goto(i.position[0]+xCorrection,i.position[1]+yCorrection)
        window.after(1,animate)



#BUTTON FUNCTIONS===================
def f_E():
    global Celectrostatics
    if not Celectrostatics:
        Celectrostatics = True
        bn_E.config(text = "• Electrostatic Force")
    else:
        bn_E.config(text = "  Electrostatic Force")
        Celectrostatics = False

def f_G():
    global Cgravitation
    if not Cgravitation:
        bn_G.config(text = "• Gravitational Force")
        Cgravitation = True
    else:
        bn_G.config(text = "  Gravitational Force")
        Cgravitation = False

def f_start():
    global stopped,started,collided
    if not started:
        if not updated:
            f_update()
        started = True
        startPhysics()
    if stopped or collided:
        stopped = False
        collided = False
    animate()

def f_stop():
    global stopped,pauseTime
    stopped = True

def f_update():
    global gravitation,electrostatics,updated,duration,collided
    if stopped:
        pen1.clear()
        pen2.clear()
        restoreDefault()
        duration = 0
        updated = True
        collided = False
        electrostatics = Celectrostatics
        gravitation = Cgravitation
        startPhysics()
        updateVariables()
        setTurtle()



#==============GUI==================
createWindow()
checkOrientation()
setTurtle()
window.bind("<Configure>",checkOrientation)
window.mainloop()
