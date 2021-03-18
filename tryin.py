# https://codeloop.org/pyqt5-drawing-rectangle-with-qpainter-class/
# this class draws a piano with 88 keys with PyQt5

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
import sys
#from keyboardInput import Midoinput

import pygame
import pygame.midi
import time
import mido
import threading


class Window(QMainWindow):
    def __init__(self):
        print('in __init__ before threading')
        self.midi_input = MidiInput()
        print('in __init__ AFTER threading')

        super().__init__()      # exended from class QMainWindow
 
        self.title = "Improvisation App"
        self.top = 10
        self.left = 10
        self.width = 1200
        self.height = 700

        self.InitWindow()


    def InitWindow(self):
        print('in InitWindow')
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


    # AS: ist jetzt in der MidiInput-Klasse
    #keyMainArray = []
    #for i in range(88):
    #    keyMainArray.append(False)


    # draw Piano keyboard with 88 keys
    def paintEvent(self, e):
        print('in def paintEvent')
  
        painter = QPainter(self)    # reated the object of QPainter class

        # AS: Hier liegt der Hund begraben. Du startest bei jedem Draw die getInput(), und in der ist eine Dauerschleife
        #Arrayyy = self.getInput()

        Arrayyy = MidiInput.getKeyArray(self)
        print('Arrayyy in paintEvent follows')
        print(Arrayyy)
        

        if Arrayyy == [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]:
            print('we are in paintEvent if ')
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # set pen to draw the outline of the key
            painter.setBrush(QBrush(Qt.white, Qt.SolidPattern)) # set brush to fill the key with color
        elif Arrayyy[0] == True: 
            print('we are in paintEvent else 0')
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # set pen to draw the outline of the key
            painter.setBrush(QBrush(Qt.red, Qt.SolidPattern)) # set brush to fill the key with color
        elif Arrayyy[2] == True:
            print('we are in paintEvent else 2')
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # set pen to draw the outline of the key
            painter.setBrush(QBrush(Qt.green, Qt.SolidPattern)) # set brush to fill the key with color
        elif Arrayyy[4] == True:
            print('we are in paintEvent else 4')
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # set pen to draw the outline of the key
            painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern)) # set brush to fill the key with color
        else:
            print('we are in paintEvent else all')
            painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))  # set pen to draw the outline of the key
            painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern)) # set brush to fill the key with color
        self.drawPianoKeys(painter)
        self.update()
        QApplication.processEvents()
        #QThread.msleep(1)

            
        
    def drawPianoKeys(self, painter):
        print('we are in def drawPiano')
 
        # drawing white keys
        x = 70
        for rect in range(52):
            painter.drawRect(x, 200, 20, 170)
            x = x + 20
            #print(x)
        
        # drawing black keys
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        #first black key
        test = painter.drawRect(84, 200, 12, 110)
        test
        # following 7 octaves of black keys
        x = 124 # 8 breit
        for rect in range(7):
            painter.drawRect(x, 200, 12, 110)
            painter.drawRect(x+20, 200, 12, 110)
            painter.drawRect(x+60, 200, 12, 110)
            painter.drawRect(x+80, 200, 12, 110)
            painter.drawRect(x+100, 200, 12, 110)
            x = x + 140 
        #print('in draw Piano before __init__call') 
        #self.__init__()
        #print('in draw Piano after __init__call') 

            



#==================================== Keyboard Input =====================================================

class MidiInput():
    keys = [False] * 88 # AS: Key Array kommt hier rein, um Model und View zu trennen

    def __init__(self):
        input_thread = threading.Thread(target=self.getInput)
        input_thread.start()

    def getKeyArray(self):
        return MidiInput.keys

    def getInput(self):
        print('in def getInput/ = THREAD')
        # AS: wir benutzen eine globale Variable
        #keyArray = []
        #keyArray = Window.keyMainArray

        inputs = mido.get_input_names() # hol dir eine Liste mit allen Midi-Geräten, die angeschlossen sind
        #print(inputs)

        with mido.open_input(inputs[0]) as p: # hier die [1] mit dem richtigen Gerät ersetzen
            # AS: das hier ist eine Dauerschleife, wir returnen da nix
            for msg in p:
                #print(msg) # gibt alle Midi-Events aus
                if not msg.is_meta:
                    #print(msg.note)
                    print('line 130')
                    print(msg.type)
                    if msg.type =='note_on':
                        #print("note ON is the type")
                        self.keys[msg.note - 36] = True
                        #print(keyArray)
                        #return keyArray
                        #self.__init__
                        #self.paintEvent()
                        #self.prepForDot(keyArray)
                    if msg.type == 'note_off':
                        #print("note OFF is the type")
                        self.keys[msg.note - 36] = False
                        #print(keyArray)
                        #return keyArray

# every PyQt5 application must create an application object
App = QApplication(sys.argv)
# enter the mainloop of the application. The event handling starts from this point
window = Window()
sys.exit(App.exec())