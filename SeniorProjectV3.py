import serial #Import pyserial Library
import numpy
import matplotlib.pyplot as plt
from drawnow import *
from graphics import *
from Button import *
import time
from numpy import mean
    

def makeGaitFig(): #Creates a function that makes the updated figure
    
    
    ax1=figG.add_subplot(121)
    ax2=figG.add_subplot(122)

    ax1.plot(FSR1, 'ro-', label="Left")
    ax1.plot(FSR2, "bo-", label = "Right")
    ax1.plot(FSR3, 'go-', label = "Heel")
    ax1.plot(FSR4, 'yo-',label= "Bridge")
    ax1.legend(loc="upper left")
    ax1.set_ylim(0,1050)
    ax1.set_title('FSR Sensor Data')
    #plt.grid(True)
    ax1.set_ylabel("voltage")

    ax2.plot(accelX,'ro-',label="X Rotation")
    ax2.plot(accelY,'bo-',label="Y Rotation")
    ax2.plot(accelZ,'go-',label="Z Rotation")
    ax2.legend(loc="upper left")
    #ax2.set_ylim(Min,Max)
    ax2.set_title('Accelerometer Data')
    ax2.set_ylabel("")
    
    
    #plt.plot(FSR3, 'g-', label = 'FSR3')
#FSR1 is on the inside of the foot (big toe)
#FSR2 is on the outside of the foot (pinky toe)
#FSR3 is on the heel
 #Infinite Loop

def drawGraph(FSR1,FSR2,FSR3,accelX,accelY,accelZ,arduinoSerialData,cnt,fig):
    
    drawnow(makeFig)
    #plt.pause(.000001)
    cnt = cnt+1
    if (cnt>100):
        FSR1.pop(0)
        FSR2.pop(0)
        FSR3.pop(0)
        FSR4.pop(0)
        accelX.pop(0)
        accelY.pop(0)
        accelZ.pop(0)
    return cnt


def avgStandScore():
    #finds standing score using all previous data
    #finds the weight on each side of the foot, uses averaging to find a more accurate value. 
    FSR1A=0
    FSR2A=0
    FSR4A=0
    
    count=0
    for val in FSR1:
        FSR1A+=val
        count+=1
    FSR1A=FSR1A/count
    #print("FSR1",FSR1A)

    count=0
    for val in FSR2:
        FSR2A+=val
        count+=1
    FSR2A=FSR2A/count
    #print("FSR2",FSR2A)

    count=0
    for val in FSR4:
        FSR4A+=val
        count+=1
    FSR4A=FSR4A

    avgSupin=FSR2A+FSR4A
    avgSupin=avgSupin/2
    
    totalPressure=FSR1A+avgSupin
    #print("totalpressure",totalPressure)
    pronationScore=FSR1A/totalPressure
    #print("pronationScore",pronationScore)
    pronationScore=(pronationScore*10)
    #print("pronationScore",pronationScore)
    pronationScore=pronationScore-5
    pronationScore=round(pronationScore)
    return pronationScore

def instantStandScore():
    #finds stand score with the last 10 values
    #IV=instant values
    #I=list of the last 10 values
    FSR1IV=0
    FSR2IV=0
    FSR3IV=0
    FSR4IV=0
    FSR1I=FSR1[-50:-1]
    FSR2I=FSR2[-50:-1]
    FSR3I=FSR3[-50:-1]
    FSR4I=FSR4[-50:-1]
    
    count=0
    for val in FSR1I:
        FSR1IV+=val
        count+=1
    FSR1IV=FSR1IV/count
    #print("FSR1",FSR1A)

    count=0
    for val in FSR2I:
        FSR2IV+=val
        count+=1
    FSR2IV=FSR2IV/count
    #print("FSR2",FSR2A)

    count=0
    for val in FSR4I:
        FSR4IV+=val
        count+=1
    FSR4IV=FSR4IV/count

    avgSupin=FSR2IV+FSR4IV
    avgSupin=avgSupin/2
    
    totalPressure=FSR1IV+avgSupin
    #print("totalpressure",totalPressure)
    pronationScore=FSR1IV/totalPressure
    #print("pronationScore",pronationScore)
    pronationScore=(pronationScore*10)
    #print("pronationScore",pronationScore)
    pronationScore=pronationScore-5
    pronationScore=round(pronationScore)
    return pronationScore  

#Startup/Setup GUI
#Gets user input on what they want: Gait or Standing Imbalance Analysis. Also a Quit Button if possible.
#After getting one of these two responses, it will return a string "Gait Analysis" or "Standing Imbalance Analysis". This could be the name of the button and simply returning the label of the button.
#If time, maybe we can even use tkinker to put some animations.
def start(): 
    startWin=GraphWin("Start",800,450)
    startWin.setBackground('white')
    #Styling:
        #Set the window color to white
        #Change the font of all the text
        #second line under Welcome: change to regular, not bold. Shorten the message.
        #Buttons: change the color and font of the text. Perhaps make it bolded as well.
    footImage=Image(Point(400,225),"foot-pic.gif")
    footImage.draw(startWin)
    introLine = Text(Point(400,50),"Select 'Gait Analysis' or 'Standing Imbalance Score':").draw(startWin)
    introLine.setSize(16)
    introLine.setStyle("bold")
    introLine.setFace('helvetica')
    standingButton=Button(startWin,Point(200,250), 220,110,"Standing Imbalance Score")
    standingButton.activate()
    standingButton.setFill("dark blue")
    standingButton.setFace("helvetica")
    standingButton.setTextColor('white')
    standingButton.setStyle('bold')
    standingButton.setOutline('white')

    gaitButton=Button(startWin,Point(600,250),220,110,"Gait Analysis")
    gaitButton.activate()
    gaitButton.setFill("dark green")
    gaitButton.setTextColor('white')
    gaitButton.setStyle('bold')
    gaitButton.setOutline('white')

    whiteRect=Rectangle(Point(300,400),Point(500,350)).draw(startWin)
    whiteRect.setFill('white')
    whiteRect.setOutline('white')

    rCirc=Circle(Point(370,185),10).draw(startWin)
    rCirc.setFill('red')

    lCirc=Circle(Point(420,190),10).draw(startWin)
    lCirc.setFill('blue')

    bCirc=Circle(Point(420,240),10).draw(startWin)
    bCirc.setFill('yellow')

    hCirc=Circle(Point(395,295),10).draw(startWin)
    hCirc.setFill('green')

    pt=startWin.getMouse()
    while not (standingButton.clicked(pt) or gaitButton.clicked(pt)):
        pt=startWin.getMouse()
    if standingButton.clicked(pt):
        startWin.close()
        return "S"

    else:
        startWin.close()
        return "G"
    

def calibrateGait():
    #GUI
    accelY=[]
    calWin=GraphWin("Calibration",800,450)
    calLine1=Text(Point(400,50),"Please calibrate before continuing").draw(calWin)
    calLine1.setSize(18)
    calButton=Button(calWin,Point(400,225),300,200,"Calibrate")
    calButton.activate()
    pt=calWin.getMouse()
    #get button click
    while not calButton.clicked(pt):
        pt=calWin.getMouse()
    calButton.deactivate()
    #get the data, put a countdown timer
    calLine2=Text(Point(400,100),"4").draw(calWin)
    #calibrate y accel direction - finding the average y accel for a baseline. May need to also find the average fsr values.
    while len(accelY)<41:
        if (arduinoSerialData.inWaiting()==0): #Only continue if data in the serial port
            pass
        myData = arduinoSerialData.readline() #reading the Serial port data as a string
        #print ((myData))
        myData = str(myData)
        myData = myData.split(",") #convert myData from string to list
        #print(myData)
        del myData[-1]
        del myData[0]
        accelYV = float(myData[4])
        accelY.append(accelYV)
        n=len(accelY)
        if (n>0) and (n%4==0):
            calLine2.setText(str(int((10-(n/4)))))
    calLine2.setText("")
        #Find the average acceleration in Y direction, and close out of window. Return the average accel
##    avgAccelY=0
##    count=0
##    print(accelY)
##    for val in accelY:
##        avgAccelY+=val
##        count+=1
    avgAccelY=mean(accelY)
    accelY=[]

    #now do walking calibration (finding the min and max values of accelerometer)
    calLine1.setText("Please take three steps. Press 'Start' to begin, and 'Stop' after three steps.")
    calButton.setLabel("Start")
    calButton.setFill("green")
    calButton.activate()
    pt=calWin.getMouse()
    while not calButton.clicked(pt):
        pt=calWin.getMouse()
    calButton.setLabel("Stop")
    calButton.setFill("Red")
    while True:#will keep going until the user presses stop.
        pt=calWin.checkMouse()
        if pt!=None:
            if calButton.clicked(pt):
                break
        if (arduinoSerialData.inWaiting()==0): #Only continue if data in the serial port
            pass
        myData = arduinoSerialData.readline() #reading the Serial port data as a string
        #print ((myData))
        myData = str(myData)
        myData = myData.split(",") #convert myData from string to list
        #print(myData)
        del myData[-1]
        del myData[0]
        accelYV = float(myData[4])
        accelY.append(accelYV)

    #Finding the average min and max of the three steps. 
    maxYlst=[]
    for i in range(3):
        maxYlst.append(max(accelY))
        accelY.remove(max(accelY))

    avgMaxY=mean(maxYlst)

    minYlst=[]
    for i in range(3):
        minYlst.append(min(accelY))
        accelY.remove(min(accelY))
        
    avgMinY=mean(minYlst)
    
    
    calWin.close()
    
    
    return avgAccelY,avgMaxY,avgMinY
    

def convertGaitData(FSR1,FSR2,FSR3,FSR4,accelY): #converts lists into another form    
    stepDataLst=[]
    for i in range(len(accelY)):
        stepData=[]
        for lst in [FSR1,FSR2,FSR3,FSR4,accelY]:
            stepData.append(lst[i])
        stepDataLst.append(stepData)
        
    return stepDataLst
        
    
    

def graphGait(): #draws graphs of both the accelerometer and FSR data
    global cnt
    
    drawnow(makeGaitFig)
    #plt.pause(.000001)
    cnt = cnt+1
    if (cnt>100):
        FSR1.pop(0)
        FSR2.pop(0)
        FSR3.pop(0)
        FSR4.pop(0)
        accelX.pop(0)
        accelY.pop(0)
        accelZ.pop(0)
    return cnt
    
def collectData(FSR1,FSR2,FSR3,FSR4,accelX,accelY,accelZ): #converts the Arduino data into lists. Returns the lists
    if (arduinoSerialData.inWaiting()==0): #Only go inside if there is data waiting on the serial port
        pass
    myData = arduinoSerialData.readline() #reading the Serial port data as a string
    print ((myData),"break")
    myData = str(myData)
    myData = myData.split(",") #convert myData from string to list
    #print(myData)
    del myData[-1]
    del myData[0]
    #print(myData) #myData has now been converted to just its values
    FSR1V = float(myData[0]) #convert string to float
    FSR2V = float(myData[1])
    FSR3V = float(myData[2])
    FSR4V = float(myData[6])
    accelXV = float(myData[3])
    accelYV = float(myData[4])
    accelZV = float(myData[5])
    FSR1.append(FSR1V) #building a list of FSR1 float values
    FSR2.append(FSR2V) #building a list of FSR2 float values
    FSR3.append(FSR3V)
    FSR4.append(FSR4V)
    accelX.append(accelXV)
    accelY.append(accelYV)
    accelZ.append(accelZV)
    #print(FSR1)
    #print(FSR2)
    #print(FSR3)
    #print(accelX)

    return FSR1,FSR2,FSR3,FSR4,accelX,accelY,accelZ
    
def calcGaitScore(avgAccelY,FSR1,FSR2,FSR3,FSR4,accelY,avgMaxY,avgMinY):
    #convert y acceleration into a decimal
    #as Y goes higher:
        #FSR1 will increase proportionately (yPct: max at 100%, min at 0%) - range from .07-60%
        #FSR2 will increase until flat foot (midpoint) and then decrease (yPct: max at 50%, min at 0%) - range .07-.30-
        #FSR3 is at its max at lowest (yPct: max at 0%, min at 100%)
        #FSR4 looks similar to FSR2 (yPct: max at 50%, min at 100%)
    #All FSR values should be converted to a percentage of the total force at that point
    rangeY=avgMaxY-avgMinY
    fsr1Strike=[]
    fsr1Lift=[]
    fsr1Flat=[]
    fsr2Strike=[]
    fsr2Lift=[]
    fsr2Flat=[]
    fsr3Strike=[]
    fsr3Lift=[]
    fsr3Flat=[]
    fsr4Strike=[]
    fsr4Lift=[]
    fsr4Flat=[]
    for i in range(len(FSR1)):
        yPctAccel=(accelY[i]-avgMinY)
        #calculating percent acceleration
        yPctAccel=yPctAccel/rangeY
        #print("ypctaccel",yPctAccel)
        #calculating ideal fsr values in percentage
        x=yPctAccel
        fsr1Ideal=(0.44*(x**2))+(0.04*x)+0.04
        #print('fsr1ideal',fsr1Ideal)
        fsr2Ideal=(0.12*(x**2)) + (0.04*x) + 0.23
        fsr3Ideal=(-0.34*(x**2)) - (0.23*x) + 0.58
        fsr4Ideal=(-0.2*(x**2)) + (0.14*x)+0.15
        #convert lists into percentages
        totalForce=0
        for lst in [FSR1,FSR2,FSR3,FSR4]:
            totalForce+=lst[i]
        #print('totalforce',totalForce)
        fsr1v=FSR1[i]/totalForce
        #print('fsr1v',fsr1v)
        fsr2v=FSR2[i]/totalForce
        fsr3v=FSR3[i]/totalForce
        fsr4v=FSR4[i]/totalForce
        #Index each list and create a score
        fsr1Score=fsr1v-fsr1Ideal
        #print('fsr1score',fsr1Score)
        fsr2Score=fsr2v-fsr2Ideal
        fsr3Score=fsr3v-fsr3Ideal
        fsr4Score=fsr4v-fsr4Ideal
        #after giving it a numerical score, group it into heel strike, roll, and heel off
        if yPctAccel<0.25:
            #Group into heel strike
            fsr1Strike.append(fsr1Score)
            fsr2Strike.append(fsr2Score)
            fsr3Strike.append(fsr3Score)
            fsr4Strike.append(fsr4Score)
        elif yPctAccel>0.75:
            #Group into heel lift
            fsr1Lift.append(fsr1Score)
            fsr2Lift.append(fsr2Score)
            fsr3Lift.append(fsr3Score)
            fsr4Lift.append(fsr4Score)
        else:
            #Group into flat foot 
            fsr1Flat.append(fsr1Score)
            fsr2Flat.append(fsr2Score)
            fsr3Flat.append(fsr3Score)
            fsr4Flat.append(fsr4Score)
            #create a list of lists for each position. append the scores to its corresponding list
            #find the average score for each sensor at each position
        #avgStrikeScore is a list of the averages for each sensor at that location
        avgStrikeScore=[]
        for lst in [fsr1Strike,fsr2Strike,fsr3Strike,fsr4Strike]:
            avgStrikeScore.append(mean(lst))
        avgLiftScore=[]
        for lst in [fsr1Lift,fsr2Lift,fsr3Lift,fsr4Lift]:
            avgLiftScore.append(mean(lst))
        avgFlatScore=[]
        for lst in [fsr1Flat,fsr2Flat,fsr3Flat,fsr4Flat]:
            avgFlatScore.append(mean(lst))
        #average scores for each position in different lists.
            #[fsr1,fsr2,fsr3,fsr4]
    
    #convert these average scores into text (outside of for loop)
    #first do analysis of heel strike
    lstStrikeOutputs=[]
    lstLiftOutputs=[]
    lstFlatOutputs=[]
    #print('avgstrike',avgStrikeScore,'avgflat',avgFlatScore,'avglift1',avgLiftScore)
    for i in range(len(avgStrikeScore)):
        if avgStrikeScore[i]<-0.05:
            #print('here1')
            lstStrikeOutputs.append("more pressure")
        elif avgStrikeScore[i]>0.05:
            lstStrikeOutputs.append("less pressure")
        else:
            lstStrikeOutputs.append("great!")
    for i in range(len(avgLiftScore)):
        if avgLiftScore[i]<-0.05:
            lstLiftOutputs.append('more pressure')
        elif (avgLiftScore[i]>0.05):
            #print("here2")
            lstLiftOutputs.append('less pressure')
        else:
            #print(3)
            lstLiftOutputs.append("great!")#continue with empy string, then do the same thing for flatscore
    for i in range(len(avgFlatScore)):
        if avgFlatScore[i]<-0.05:
            lstFlatOutputs.append('more pressure')
        elif avgFlatScore[i]>0.05:
            lstFlatOutputs.append("less pressure")
        else:
            lstFlatOutputs.append('great!')
    return [lstStrikeOutputs,lstFlatOutputs,lstLiftOutputs]
        

def displayGaitResults(resultLst,fig): #display the results and ask user if he wants to re-test or exit
    resultWinG=GraphWin("Results",800,450)
    resultLine1G=Text(Point(400,50),"Here are your results: ").draw(resultWinG)
    finalResultLst=["Right Side: ","Left Side: ","Bridge: ","Heel: ","Right Side: ","Left Side: ","Bridge: ","Heel: ","Right Side: ","Left Side: ","Bridge: ","Heel: "]
    #creating a list: first it is heel strike, then flat foot, then lift heel
    for i in range(3):
        for val in resultLst[i]:
            finalResultLst.append(val+'\n')
    cnt=0
    identifierLst=["\nHeel Strike:\n","\nFlat Foot:\n","\nHeel Lift:\n"]
    resultstr=''
    headerLst=[]
    
    for i in range(3):
        headerLst.append(Text(Point(200+200*i,100),identifierLst[i]).draw(resultWinG))
    
    string=''
    strLst=['','','']
    
    #converting list into an easier form to turn into Text
    #print(len(finalResultLst))
    for i in range(int(len(finalResultLst)/2)):
        strLst[i//4]=strLst[i//4]+finalResultLst[i]+finalResultLst[i+12]+'\n'
       
    textObjLst=[]
    
    for i in range(3):
        textObjLst.append(Text(Point(200+200*i,200),strLst[i]).draw(resultWinG))

    exitB=Button(resultWinG,Point(300,300),200,50,"Exit")
    exitB.activate()
    testAgainB=Button(resultWinG,Point(500,300),200,50,"Test Again")
    testAgainB.activate()
    pt=resultWinG.getMouse()
    while not (exitB.clicked(pt) or testAgainB.clicked(pt)):
        pt=win.getMouse()
    resultWinG.close()
    if exitB.clicked(pt):
        #close out of current window and out of matplotlib
        plt.close()
        return True
    else:
        #re-run the program starting from after the calibration
        return False
        
        
def standBeginMessage():#displays a message asking user to stay still while data is being collected. calls the collectdata() function inside to get the data points. exits after a certain number of data points.
    #GUI
    
    calWin=GraphWin("Standing Data Collection",800,450)
    calWin.setBackground('white')
    calLine1=Text(Point(400,50),"Press 'Begin' to start").draw(calWin)
    calLine1.setSize(17)
    calLine1.setStyle('bold')
    calLine1.setFace('helvetica')
    calButton=Button(calWin,Point(400,225),300,200,"Begin")
    calButton.setFace('helvetica')
    calButton.setLabelSize(14)
    calButton.setStyle('bold')
    calButton.activate()
    pt=calWin.getMouse()
    #get button click
    while not calButton.clicked(pt):
        pt=calWin.getMouse()
    calWin.close()
    
def graphStand():
    global cnt
    
    drawnow(makeStandFig)
    #plt.pause(.000001)
    cnt = cnt+1
    if (cnt>100):
        FSR1.pop(0)
        FSR2.pop(0)
        FSR3.pop(0)
        FSR4.pop(0)
        accelX.pop(0)
        accelY.pop(0)
        accelZ.pop(0)
    return cnt

def makeStandFig():    
    plt.plot(FSR1, 'ro-', label = 'Right')
    plt.plot(FSR2, 'bo-', label = 'Left')
    plt.plot(FSR3, 'go-', label = 'Bridge')
    plt.plot(FSR4, 'yo-', label = 'Heel')
    plt.legend(loc="upper left")
    plt.ylim(0,1050)
    plt.title('FSR Sensor Data')
    plt.grid(True)
    plt.ylabel("voltage")
#FSR1 is on the inside of the foot (big toe)
#FSR2 is on the outside of the foot (pinky toe)
#FSR3 is on the heel
#Infinite Loop


def displayStandResults(score,figS): #displays the result on a chart, asks user to exit or re-test.
    resultWin=GraphWin("Results",800,450)
    txt1=Text(Point(400,100),("Your score is: "+str(score))).draw(resultWin)
    outRect=Rectangle(Point(250,200),Point(550,250)).draw(resultWin)
    outRect.setFill('grey')
    inRectX=400+(30*score)
    inRect=Rectangle(Point(400,200),Point(inRectX,250)).draw(resultWin)
    inRect.setFill('orange')
    exitB=Button(resultWin,Point(300,350),200,50,"Exit")
    exitB.activate()
    testAgainB=Button(resultWin,Point(500,350),200,50,"Test Again")
    testAgainB.activate()
    txt2=Text(Point(250,275),"-5 \n(Most Supinated)").draw(resultWin)
    txt3=Text(Point(550,275),"5 \n(Most Pronated)").draw(resultWin)
    txt4=Text(Point(400,275),"0 \n(Balanced)").draw(resultWin)
    line=Line(Point(400,200),Point(400,250)).draw(resultWin)
    pt=resultWin.getMouse()
    while not (exitB.clicked(pt) or testAgainB.clicked(pt)):
        pt=resultWin.getMouse()
    resultWin.close()
    if exitB.clicked(pt):
        #close out of current window and out of matplotlib
        plt.close()
        return True
    else:
        #re-run the program starting from after the calibration
        return False
    

 
#Main program begins here
arduinoSerialData = serial.Serial("com7", 9600) #This variable is connected to the Serial port COM7, 9600 Baud
plt.ion()

while True: #not quitButton.clicked(pt)
    FSR1 = []
    FSR2 = []
    FSR3 = []
    FSR4 = []
    accelX = []
    accelY = []
    accelZ = []
    
    #Startup
    mode=start()
    exitB=False
    if mode=="G": #G for gait
    #display the calibration screen. Wait for user to begin the calibration before doing it
        avgAccelY,avgMaxY,avgMinY=calibrateGait()
        x=1
            #while user is calibrating, display a timer to wait a few seconds
            #Calibrate the acceleromter - find what is the average value
        figG=plt.figure(figsize=(12,6))
        plt.style.use('fivethirtyeight')
        cnt=0
        while not exitB: #notExitButton.clicked(pt)
            cnt+=1
            FSR1,FSR2,FSR3,FSR4,accelX,accelY,accelZ=collectData(FSR1,FSR2,FSR3,FSR4,accelX,accelY,accelZ)
            #print(FSR1,FSR2,FSR3,FSR4,accelX,accelY,accelZ)
            
        #After calibration is over, display the graphs - display one of all the FSRs and one of the accelerometer.
            graphGait()
            if cnt>60:
                lst=calcGaitScore(avgAccelY,FSR1,FSR2,FSR3,FSR4,accelY,avgMaxY,avgMinY)
                print(lst)
                exitB=displayGaitResults(lst,figG)
                cnt=0
                #seeing if exit button was clicked or not. If it isn't, then will loop back.
                #exitB clicked, then close the matplotlib window and return to home.
                

    if mode == "S": #S for Standing
        #Display a message telling the user to wait for the results to be calculated
        standBeginMessage()
        figS=plt.figure(figsize=(12,6))
        plt.style.use('seaborn-darkgrid')
        
        cnt=0
        while not exitB:
            #Show a graph with only the FSR data since accelerometer doesn't matter here
            cnt+=1
            FSR1,FSR2,FSR3,FSR4,accelX,accelY,accelZ=collectData(FSR1,FSR2,FSR3,FSR4,accelX,accelY,accelZ)
        #After the results are calculated, close matplotlib and show the score
            graphStand()
            if cnt>150:
                score=instantStandScore()
                exitB=displayStandResults(score,figS)
                cnt=0
            

    
               
    
