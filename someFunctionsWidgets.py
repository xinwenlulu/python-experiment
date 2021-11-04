import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from experiment import *
from os import listdir
from random import randint

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app = QApplication(sys.argv)

window = QMainWindow()
ui = Ui_experimentWindow()

# a function to assign condition and urnposition
def decideConditionUrnPosition():
    numberOFparticipants = 0
    numberOFconditions = 3
    filesINdirectory = listdir()

    if 'Experiment Result.csv' in filesINdirectory:
        resultFile = open('Experiment Result.csv', 'r')
        content = resultFile.read()
        content = content.split(',')

        for item in content:
            if '\n' in item:
                numberOFparticipants += 1

        conditionRemainder = numberOFparticipants % numberOFconditions
    else:
        conditionRemainder = 0

    # condition is determined by the number of participants already took part
    # the first participant will be assigned condition 2, the second condition 10 and the third condition 100.
    if conditionRemainder == 0:
        condition = 2
    elif conditionRemainder == 1:
        condition = 10
    else:  # conditionRemainder == 2:
        condition = 100

    # randomise urn position regardless of the number of participants already took part or assigned each urn position
    urnPosition = randint(0,1)

    return (condition,urnPosition)


# custom widget to interact with users
class Feedback(QLabel):

    # feedback function to display text label messages
    def feedback(self,contentString,time = 3500,size = 14,colourString = 'red',centreY = False,delay = False):
        self.setText(contentString)
        self.setFont(QFont('Arial', size))
        self.adjustSize()
        if centreY == True:
            self.setGeometry(window.width()/2 - self.width()/2 - 10,window.height()/2,self.width(),self.height())
        else:
            self.setGeometry(window.width()/2 - self.width() / 2, 500, self.width(), self.height())
        self.setAutoFillBackground(True)
        myPalette = self.palette()
        myPalette.setColor(QPalette.Window,QColor('white'))
        myPalette.setColor(QPalette.WindowText,QColor(colourString))
        self.setPalette(myPalette)

        # a timer to hide the feedback message after a set amount of time
        window.timer = QTimer()
        window.timer.timeout.connect(self.hide)
        window.timer.setSingleShot(True)

        if delay == True:
        # delaying the showing the label for 1000 ms; used when displaying the result in text
        # text result will be shown roughly when the animation has drawn the marble out of the urn and magnifies it)
            window.delayTimer = QTimer()
            window.delayTimer.timeout.connect(self.show)
            window.delayTimer.setSingleShot(True)
            window.delayTimer.start(1000)
            window.timer.start(time)
        else:
            self.show()
            window.timer.start(time)
#Potential probelm:
 # when displaying error messages, if user clicked next page again before the timer ends, the label remains on the window


    # a function to produce condition-and-urnPosition-specific instructions
    def instruction(self, urnPosition, condition):
        half = int(condition / 2)
        condition = str(condition)
        half = str(half)
        if urnPosition == 0:
            self.setText(' Urn A contains ' + half + ' red marbles and ' + half + ' blue marbles. Urn B contains '
                + condition + ' marbles in an unknown color\n ratio, from ' + condition + ' red marbles and 0 blue '
                'marbles to 0 red marbles and ' + condition + ' blue marbles. The mixture of\n red and blue marbles in '
                'Urn B has been decided by a computer generated random number between 0\n and ' + condition +
                '. This number has been used to determine the number of blue marbles to be put into Urn B, but\n you do '
                'not know the number. Every possible mixture of red and blue marbles in Urn B is equally likely.')
        else:  # urnPosition == 1
            self.setText(' Urn A contains ' + condition + ' marbles in an unknown colour ratio, from ' + condition +
                ' red marbles and 0 blue marbles to 0\n red marbles and ' + condition + ' blue marbles. Urn B contains '
                + half + ' red marbles and ' + half + ' blue marbles. The mixture of\n red and blue marbles in Urn A has'
                ' been decided by a computer generated random number between 0\n and ' + condition + '. This number has '
                'been used to determine the number of blue marbles to be put into Urn A, but\n you do not know the number. '
                'Every possible mixture of red and blue marbles in Urn A is equally likely.')
        self.setFont(QFont('Arial', 13))
        self.setGeometry(10, 74, 612, 80)
        self.show()

    # a function to display the result and marble-drawing in animation
    def showMarbleDrawn(self, marble,urnPosition,selectedUrn):

        if marble == 'red':
            self.setPixmap(QtGui.QPixmap('red-orb.png'))
        else:
            self.setPixmap(QtGui.QPixmap('5228055c3a0be6380d900f3321d7a206-blue-marble-ball-by-vexels.png'))

        window.resultTimer = QTimer()
        window.resultTimer.timeout.connect(self.animateMarble)

        # determine the starting geometry of the marble animatjion based on the chosen urn
        if (urnPosition == 0 and selectedUrn == 1) or (urnPosition == 1 and selectedUrn == 0):
            #drawing from left urn  - urn A
            self.setGeometry(120,400,22,22)
        else: #(urnPosition == 0 and selectedUrn == 0) or (urnPosition == 1 and selectedUrn == 1)
            self.setGeometry(470,400,18,18)

        self.setScaledContents(True)
        self.show()
        window.resultTimer.start(50)

    # a function that defines how the marble picture will move
    def animateMarble(self):
        currentX = self.x()
        currentY = self.y()
        currentW = self.width()
        currentH = self.height()
        if currentY > 180: # marble goes up before the marble reaches the top of the urn
            self.setGeometry(currentX, currentY - 10, currentW, currentH)
        else:
            if currentW < 100: # after getting out of the urn, marble gets bigger to make the result clearer
                self.setGeometry(currentX - 5, currentY, currentW + 10, currentH + 10)