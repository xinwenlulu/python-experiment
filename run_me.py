import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from experiment import *
from someFunctionsWidgets import *
from random import *

#######################################################################################################################

                # Written with a PyQt 5 Interface on an 11-inch MacBook Air with 1366 x 768 pixel display (135 ppi)
                # formatting and sizing issues may exist on different monitors
                # Apart from this file, it also requires experiment.py, someFunctionsWidgets.py, 589412.jpg,
                # 35704.svg, red-orb.png and 5228055c3a0be6380d900f3321d7a206-blue-marble-ball-by-vexels.png
                # to be in the same directory (the same PyCharm Project)
                # someFunctionsWidgets.py contains functions to decide condition and urn positions and custom widgets
                # An error state will be caused by attempting to move to the next page without providing all the
                # information required for the current page (e.g. consent, demographics, urn choice)
                # Written by YZBN6

                # To add more condition: e.g. 200 marbles in each urn
                    # go to someFunctionsWidgets.py
                    # find the function ---- decideConditionUrnPosition()
                    # change the variable numberOFconditions to 4 (2,10,100,200)
                    # change an elif conditionRemainder == 2 situation, and make condition == 100 in this situation
                    # change the condition assignment from 100 to 200 in the else condition
                    # do not need to change the visual: condition 100 and 200 all the marbles will be shown
                    # instructions and marble-drawing from 50:50 or random distributions will change automatically

                # This file might not be flexible enough to easily modify
                    # experimental design(to within participant)
                    # number of urns (absolute geomtry for visualising conditions and urnpositions)
                    # due to the use of only one experiment page and
                    # the button for next page has already been connected to a complicated function (check)

#######################################################################################################################

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app = QApplication(sys.argv)

window = QMainWindow()

ui = Ui_experimentWindow()
ui.setupUi(window)


def previouspage():
    currentIndex = ui.stackedPages.currentIndex()
    previousIndex = currentIndex - 1
    ui.stackedPages.setCurrentIndex(previousIndex)


def nextpage():
    currentIndex = ui.stackedPages.currentIndex()
    nextIndex = currentIndex + 1
    ui.stackedPages.setCurrentIndex(nextIndex)


# returns whether the selected urn is the 50:50 one or the random one
# returns also whether the user got a blue or a red marble
def choiceAndMarble(condition, urnPosition):
    if (ui.urnA.isChecked() == True and urnPosition == 0) or (ui.urnB.isChecked() == True and urnPosition == 1):
    # (urn A (50:50) chosen & random urn on the right as urn B) or (urn B (50:50) chosen & random urn on the left as urn A)
        selected = 1  # when the 50:50 urn chosen, write 1
        urn = []
        halfMarbles = int(condition / 2)
        # create 50:50 distribution based on the condition
        for i in range(halfMarbles):  # 0 = red marble, 1 = blue marble
            urn.append(1)
            urn.append(0)
    else:  # (ui.urnA.isChecked() == True and urnPosition == 1) or (ui.urnB.isChecked() == True and urnPosition == 0)
    # (urn A(random) chosen & random urn on the left as urnA) or (urn B(random) chosen & random urn on the right as urnB)
        selected = 0  # when the random urn chosen, write 0
        ratio = randint(0,condition)  #generate a random number to decide the number of blue marbles in the random urn
        urn = []
        for i in range(ratio):
            urn.append(1)  # append a number(ratio) of 1s to represent blue marbles
        for i in range(condition - ratio):
            urn.append(0)  # append remaining number of marbles and 0 represent red marbles

    shuffle(urn)  # shuffle 1s(blue marble) and 0s(red marble) in the urn list
    drawMarble = choice(urn)  # randomly draw one item from the list of 1s and 0s representing the chosen urn

    if drawMarble == 1:
        return (selected, 'blue')
    else:  # drawmarble == 0
        return (selected, 'red')


# function to write the result in to the csv file
def saveResult():
    resultFile = open('Experiment Result.csv', 'a')
    form = '{0},{1},{2},{3},{4},{5},{6}\n'
    # age,gender,education,condition,urnPosition,selectedUrn,marbleDrawn
    age = ui.age.text()

    if ui.male.isChecked() == True:
        gender = 'male'
    elif ui.female.isChecked() == True:
        gender = 'female'

    education = ui.education.currentText()

    result = choiceAndMarble(window.condition, window.urnPosition)
    window.selectedUrn = result[0]
    window.marble = result[1]

    data = form.format(age, gender, education, window.condition, window.urnPosition, window.selectedUrn, window.marble)
    resultFile.write(data)
    resultFile.close()


# to change instruction and visible marbles based on the condition and urn position
def visual(urnPosition, condition):
    # create and display condition-specific instruction label on the Experiment Page
    lblInstruction = Feedback(ui.experimentPage)
    lblInstruction.instruction(urnPosition, condition)

    # getting the geometry of the container of marble pictures for urn A and urn B
    urnAlocation = ui.known.geometry()  # known 50:50 marbles were defaulted in urn A using QtDesigner
    urnBlocation = ui.random.geometry()  # random marbles were defaulted in urn B using QtDesigner

    # visualise the condition by moving and hiding marble pictures contained in QWidgets
    if urnPosition == 1:
        ui.random.setGeometry(urnAlocation)  # moving the random marbles to urn A
        ui.known.setGeometry(urnBlocation)  # moving the known (50:50) marbles to urn B
    if condition == 2:
        ui.known90.hide()
        ui.known8.hide()
        ui.random90.hide()
        ui.random8.hide()
    elif condition == 10:
        ui.known90.hide()
        ui.random90.hide()
    # else: hide nothing ----  all the marbles will be shown when condition == 100


def showResult():
    lblMarbleDrawn = Feedback(ui.experimentPage) # create a custom label to display result in picture and animation
    lblResult = Feedback(ui.experimentPage)  # create a custom label to display the result in words

    # displaying marble-drawing process and result by animating marble picture
    lblMarbleDrawn.showMarbleDrawn(window.marble, window.urnPosition, window.selectedUrn)
    # displaying the result in text
    if window.marble == 'red':
        lblResult.feedback(' Oops, your marble is red! ', 4000, 18, 'green', True, True)
    else:
        lblResult.feedback("    Congratulations! It's a blue marble! \n"
                           " You'll be entered into a £30 lottery draw! ", 4000,18,'green', True, True)


# Check whether required fields are complete before the user can proceed
def check():

    # create custom labels to use inside this function
    lblError = Feedback(window)      # create a feedback label to display error message when any required field is empty

    if ui.stackedPages.currentIndex() == 0: # when on the Consent Page

        if ui.name.text() != '' and all(checkbox.isChecked() == True for checkbox in ui.checkContainer.children()) == True:
            # name entered and all checkbox checked
            nextpage()
            ui.progress.setValue(33)        # update the progress bar
        else: # if any required field on the consent page is empty
            if ui.name.text() == '':        # name is not entered
                if any(checkbox.isChecked() == False for checkbox in ui.checkContainer.children()) == True:
                # any checkbox is not checked
                    lblError.feedback(' ERROR: Please enter your name! \n'
                                      ' ERROR: Please give your consent by checking the boxes in front of all statements! \n'
                                      ' Please complete the consent form before taking part in this experiment! ')
                else: # name not entered and all checkbox checked
                    lblError.feedback(' ERROR: Please enter your name! \n'
                                      ' Please complete the consent form before taking part in this experiment! ')
            else:                           # name entered and any checkbox not checked
                lblError.feedback(' ERROR: Please give your consent by checking the boxes in front of all statements! \n'
                                  ' Please complete the consent form before taking part in this experiment!')

    elif ui.stackedPages.currentIndex() == 1: # when on the Demographics Page

        if ui.age.text() != '0' and (ui.male.isChecked() == True or ui.female.isChecked() == True) and ui.education.currentIndex() != 0:
            # all demographics information entered
            visual(window.urnPosition, window.condition)    # to display instructions and marble pictures based on the condition and urnposition
            ui.next.setText('Submit')                       # change the next page button to submit when user gets to the experiment page
            ui.progress.setValue(66)  # update the progress bar again
            nextpage()
        else:  # if any demographics information not entered - display relevant error message based on the error
            if ui.age.text() == '0':
                if ui.male.isChecked() == False and ui.female.isChecked() == False and ui.education.currentIndex() == 0:
                    lblError.feedback(' ERROR: Please enter your age! \n'
                                      ' ERROR: Please select your gender! \n'
                                      ' ERROR: Please select your education level! \n'
                                      ' Demographic questions need to be completed before moving on to the next page!')
                elif ui.education.currentIndex() == 0:
                    lblError.feedback(' ERROR: Please enter your age! \n'
                                      ' ERROR: Please select your education level! \n'
                                      ' Demographic questions need to be completed before moving on to the next page!')
                elif ui.male.isChecked() == False and ui.female.isChecked() == False:
                    lblError.feedback(' ERROR: Please enter your age! \n'
                                      ' ERROR: Please select your gender! \n'
                                      ' Demographic questions need to be completed before moving on to the next page!')
                else:
                    lblError.feedback('ERROR: Please enter your age! \n'
                                      ' Demographic questions need to be completed before moving on to the next page!')
            elif ui.female.isChecked() == False and ui.male.isChecked() == False:
                if ui.education.currentIndex() == 0:
                    lblError.feedback(' ERROR: Please select your gender! \n'
                                      ' ERROR: Please select your education level! \n'
                                      ' Demographic questions need to be completed before moving on to the next page!')
                else:
                    lblError.feedback(' ERROR: Please select your gender! \n'
                                      ' Demographic questions need to be completed before moving on to the next page!')
            else: #ui.education.currentIndex == 0:
                lblError.feedback(' ERROR: Please select your education level! \n'
                                  '  Demographic questions need to be completed before moving on to the next page! ')

    elif ui.stackedPages.currentIndex() == 2: # when on the Experimental Page

        if ui.urnA.isChecked() == True or ui.urnB.isChecked() == True: # user made a choice btw Urn A and Urn B
            ui.next.hide()
            ui.previous.hide()
            ui.progress.setValue(100)   # progress bar reaches 100%!
            saveResult()                # save the result in the csv file using the function saveResult()
            showResult()                # display the result using the function showResult()

            # a timer for the result display time before moving to the debrief page
            resultTimer = QTimer(window)
            resultTimer.timeout.connect(nextpage)
            resultTimer.setSingleShot(True)
            resultTimer.start(4000)

        else:
            lblError.feedback(' Error: Please make a choice between urn A and urn B! ',2500)


ui.date.setDate(QtCore.QDate.currentDate())     # fetch the system time as default --- user don't need to enter the date
ui.stackedPages.setCurrentIndex(0)              # starts from the first page - consent page
ui.progress.setValue(0)                         # default the progress bar value
ui.previous.clicked.connect(previouspage)       # connect the function previouspage to the button previous

# connect the button next page to a check function to make sure the user completed relevant fields
# if all required field completed, a nextpage function will be call inside the check function
ui.next.clicked.connect(check)

# make condition and urnPosition a variable of the window to access throughout this file in different functions
conditionUrn = decideConditionUrnPosition()
window.condition = conditionUrn[0]
window.urnPosition = conditionUrn[1]


window.show()
sys.exit(app.exec_())
