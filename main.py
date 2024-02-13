import sys
import traceback

from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QFrame, QLabel, QGridLayout, QVBoxLayout, QLineEdit, QGroupBox
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor, QFont
from StackClass import Stack


app = QApplication(sys.argv)

###############################################################
#
#                       Calculator Design
#
###############################################################

#Construct Window
window = QWidget()
window.setWindowTitle("Calculator")
window.setFixedSize(250, 380)
window.move(200, 200)
window.setStyleSheet("background: #000000;")

#Display Window
window.show()

#Create main layout
mainLayout = QVBoxLayout()

window.setLayout(mainLayout)

#Create text box display and add to main layout
outputDisplay = QLineEdit()

outputDisplay.setFixedHeight(50)
outputDisplay.setAlignment(QtCore.Qt.AlignRight)
outputDisplay.setReadOnly(True)
outputDisplay.setStyleSheet("background: #FFFFFF;")
outputDisplay.setFont(QFont('Times', 20))
outputDisplay.setText("0")

mainLayout.addWidget(outputDisplay)

#Create calculator buttons and add to buttons layout
buttonsLayout = QGridLayout()
buttons = {
    'C': (0,0),
    '<': (0,1),
    'Q': (0,2),
    '/': (0,3),
    '7': (1,0),
    '8': (1,1),
    '9': (1,2),
    '*': (1,3),
    '4': (2,0),
    '5': (2,1),
    '6': (2,2),
    '-': (2,3),
    '1': (3,0),
    '2': (3,1),
    '3': (3,2),
    '+': (3,3),
    '0': (4,0),
    '(': (4,1),
    ')': (4,2),
    '=': (4,3),
}

btnArray = [] #holds all calculator buttons

#Place calculator buttons in layout and store inside the array
for btnText, pos in buttons.items():
    buttons[btnText] = QPushButton(btnText)
    buttons[btnText].setFixedSize(53, 53)
    buttons[btnText].setFont(QFont('Times', 20))
    buttons[btnText].setStyleSheet("*{background-color: #e60000; color:000000;}" +
                                   "*:hover{background: '#f7ff0f'}")
    btnArray.append(buttons[btnText])
    buttonsLayout.addWidget(buttons[btnText], pos[0], pos[1])

cBtn = btnArray[0]
bsBtn = btnArray[1]
qBtn = btnArray[2]
divBtn = btnArray[3]
sevenBtn = btnArray[4]
eightBtn = btnArray[5]
nineBtn = btnArray[6]
multBtn = btnArray[7]
fourBtn = btnArray[8]
fiveBtn = btnArray[9]
sixBtn = btnArray[10]
subBtn = btnArray[11]
oneBtn = btnArray[12]
twoBtn = btnArray[13]
threeBtn = btnArray[14]
plusBtn = btnArray[15]
zeroBtn = btnArray[16]
openPar = btnArray[17]
closePar = btnArray[18]
equalBtn = btnArray[19]

#Add buttons layout to main layout
buttonsLayout.setAlignment(QtCore.Qt.AlignCenter)
mainLayout.addLayout(buttonsLayout)

#Initially disable operator buttons
divBtn.setEnabled(False)
multBtn.setEnabled(False)
subBtn.setEnabled(False)
plusBtn.setEnabled(False)

###########################################################
#
#                   Calculator Functions
#
###########################################################

infix = "" #will hold infix expression

#determine precedence of operators
def precedence(operator):
    if operator == "*" or operator == "/":
        return 2
    elif operator == "+" or operator == "-":
        return 1
    else:
        return 0

#perform an operation on part of the infix expression
def doOperation(num1, num2, operator):
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "*":
        return num1 * num2
    elif operator == "/":
        return num1 // num2

#display input character in the output display
def updateDisplay(text):
    global infix
    infix += text

    #prevent division by zero
    if text == "/":
        zeroBtn.setEnabled(False)
    else:
        zeroBtn.setEnabled(True)

    divBtn.setEnabled(True)
    multBtn.setEnabled(True)
    subBtn.setEnabled(True)
    plusBtn.setEnabled(True)
    
    outputDisplay.setText(infix)

#erase the last character of input in the output display
def backspace():
    global infix

    if not infix == "":
        infix = infix[:-1:]

    #prevent division by zero
    if len(infix)>0 and infix[-1] == "/":
        zeroBtn.setEnabled(False)
    else:
        zeroBtn.setEnabled(True)

    if len(infix) == 0:
        outputDisplay.setText("0")
    else:
        outputDisplay.setText(infix)

#evaluate infix expression
def evaluate(expression):
    global infix

    try:
        valueStack = Stack()
        operatorStack = Stack()

        i = 0

        while i<len(expression):

            #skip iteration if token is a blank space
            if expression[i] == " ":
                i += 1
                continue

            #add opening parenthesis to operator stack
            elif expression[i] == "(":
                operatorStack.push(expression[i])

            #infix expression token is a number
            elif expression[i].isdigit():
                val = 0

                #number in infix expression may have multiple digits
                while (i < len(expression) and expression[i].isdigit()):
                    val = (val * 10) + int(expression[i])
                    i += 1

                valueStack.push(val)

                i -= 1

            #if token is a closing parenthesis, solve expression between the opening and closing parentheses
            elif expression[i] == ")":

                while operatorStack.size() != 0 and operatorStack.peek() != "(":

                    val2 = valueStack.pop()
                    val1 = valueStack.pop()
                    operator = operatorStack.pop()

                    valueStack.push(doOperation(val1, val2, operator))

                operatorStack.pop()
                
            else:

                #test precedence of operators and apply operator at top of operator stack to top two values in value stack
                while (operatorStack.size() != 0 and precedence(operatorStack.peek()) >= precedence(expression[i])):
                    val2 = valueStack.pop()
                    val1 = valueStack.pop()
                    operator = operatorStack.pop()

                    valueStack.push(doOperation(val1, val2, operator))

                operatorStack.push(expression[i])

            i += 1

        #evaluate parsed infix expression
        while operatorStack.size() != 0:
            val2 = valueStack.pop()
            val1 = valueStack.pop()
            operator = operatorStack.pop()

            valueStack.push(doOperation(val1, val2, operator))

        result = str(valueStack.peek())
        infix = result
        outputDisplay.setText(result)

        if "//" in expression:
            raise ValueError
    except ZeroDivisionError:
        outputDisplay.setText("ERROR: Division by Zero")
        infix = ""
    except IndexError:
        traceback.print_exc()
        outputDisplay.setText("ERROR")
        infix = ""
    except:
        traceback.print_exc()
        outputDisplay.setText("ERROR")
        infix = ""

#wipe out all input in output display
def clearDisplay():
    global infix
    
    infix = ""
    outputDisplay.setText("0")

#close the calculator application
def closeCalc():
    sys.exit(app.exec())

    
#Button Clicked Events
btnArray[0].clicked.connect(lambda: clearDisplay())
btnArray[1].clicked.connect(lambda: backspace())
btnArray[2].clicked.connect(lambda: closeCalc())
btnArray[3].clicked.connect(lambda: updateDisplay("/"))
btnArray[4].clicked.connect(lambda: updateDisplay("7"))
btnArray[5].clicked.connect(lambda: updateDisplay("8"))
btnArray[6].clicked.connect(lambda: updateDisplay("9"))
btnArray[7].clicked.connect(lambda: updateDisplay("*"))
btnArray[8].clicked.connect(lambda: updateDisplay("4"))
btnArray[9].clicked.connect(lambda: updateDisplay("5"))
btnArray[10].clicked.connect(lambda: updateDisplay("6"))
btnArray[11].clicked.connect(lambda: updateDisplay("-"))
btnArray[12].clicked.connect(lambda: updateDisplay("1"))
btnArray[13].clicked.connect(lambda: updateDisplay("2"))
btnArray[14].clicked.connect(lambda: updateDisplay("3"))
btnArray[15].clicked.connect(lambda: updateDisplay("+"))
btnArray[16].clicked.connect(lambda: updateDisplay("0"))
btnArray[17].clicked.connect(lambda: updateDisplay("("))
btnArray[18].clicked.connect(lambda: updateDisplay(")"))
btnArray[19].clicked.connect(lambda: evaluate(infix))

#Terminate Window
sys.exit(app.exec())

