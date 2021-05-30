# this is the MAIN file
# https://codeloop.org/pyqt5-drawing-rectangle-with-qpainter-class/
# this window class creates the gui with PyQt5
# it gets the midiInput from the Thread in the midiInput module/ class
# it calls the draw method of the Key module/ class and draws the piano

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QInputDialog, QFileDialog
from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QPixmap, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSlot

import sys
import time

from constants import *
from midiInput import MidiInput
from staff import Staff
from key import Key
from labeling import Labeling
from recording import Recording
from songExtracting import SongExtracting

class Window(QMainWindow):

    

    def __init__(self):
        super().__init__()      # exended from class QMainWindow
        self.title = "Improvisation App"
        self.top = WINDOW_UPPER_LEFT_X
        self.left = WINDOW_UPPER_LEFT_Y
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        # init buttons, keyboard and window
        self.staff = Staff()
        self.init_buttons()
        self.init_keyboard(88)
        self.init_window()
        # set up midifile
        #self.midifile = self.get_midifile()
        # instance of staff
        self.recording = Recording()
        self.labeling = Labeling()
        self.labeling.init_label(self)
        self.recording_state = False
        # timer to update the application
        self.update_timer = QTimer(self)
        self.update_timer.setInterval(10)
        self.update_timer.setSingleShot(False)
        self.update_timer.timeout.connect(self.update)
        self.update_timer.start()

    # initalizing the gui window itself
    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    # creating the keyboard with colors and dots 
    def init_keyboard(self, num_keys):
        self.keys = []
        for i in range(num_keys):
            self.keys.append(Key(i, self.staff)) # self.staff as a parameter to draw dots on the keys live played by backing track 

    # creating all buttons needed for the UI
    def init_buttons(self):
        # play
        play_button = QPushButton('Play', self)
        play_button.setToolTip('to start playing the Backing Track')
        play_button.move(100,70)
        play_button.clicked.connect(self.on_click_play)
        # pause
        pause_button = QPushButton('Pause', self)
        pause_button.setToolTip('to pause the Backing Track')
        pause_button.move(200,70)
        pause_button.clicked.connect(self.on_click_pause)
        # stop
        stop_button = QPushButton('Stop', self)
        stop_button.setToolTip('to stop the Backing Track')
        stop_button.move(300,70)
        stop_button.clicked.connect(self.on_click_stop)
        # record
        record_button = QPushButton('Record', self)
        record_button.setToolTip('to record your playing')
        record_button.move(787,280)
        record_button.clicked.connect(self.on_click_record)
        # listen to recording
        listen_button = QPushButton('Play recording', self)
        listen_button.setToolTip('to listen to your recording')
        listen_button.resize(120,26)
        listen_button.move(887,280)
        listen_button.clicked.connect(self.on_click_listen)
        # save recording
        save_recording_button = QPushButton('Save recording', self)
        save_recording_button.setToolTip('to save your recording')
        save_recording_button.resize(120,26)
        save_recording_button.move(1007,280)
        save_recording_button.clicked.connect(self.on_click_save_recording)
        # upload button
        upload_button = QPushButton('Upload track', self)
        upload_button.setToolTip('to upload a backing track from your computer')
        upload_button.resize(120,26)
        upload_button.move(1007,70)
        upload_button.clicked.connect(self.on_click_upload_file)
        # countdown labels
        #self.create_countdown_label()


    '''    
    def create_countdown_label(self):   #, text):
        self.countdown_label = QtWidgets.QLabel(self)
        self.countdown_label.resize(18,30)
        #self.countdown_label.setStyleSheet("background-color: lightgreen")
        self.countdown_label.move(510,300)
        self.countdown_label.setText('')
        self.countdown_label.setFont(QFont('Georgia', 30))
        self.countdown_label.show()
        self.countdown_label.setVisible(True)
    

    def update_countdown(self, i):
        print('called')
        print(i)
        self.countdown_label.setText(i)
        self.countdown_label.show()
    '''

    # when record is clicked: 
    @pyqtSlot()
    def on_click_record(self):
       
        #if self.export_button == disabled:
        #    self.export_button.hide()
        if self.recording_state == False: # if not recording yet -> start recording + playing backing track
            #self.cre
            #i = 4
            #counts = ['4', '3', '2', '1'] 
            #for x in counts:
            #    print(x)
            #    self.countdown_label.setText(x)
            #    self.countdown_label.show()
            #    #self.update_countdown(x)
            #    time.sleep(1.0)
        
            #for i in range(4): 
            #    count_num = str(i)
            #    print(count_num)
                #self.countdown_label.setText(count_num)
                #self.update_countdown(count_num)

                #time.sleep(1.0)
                #i -= 1
            self.recording_state = True
            self.staff.play_bt()    
        else: 
            self.recording_state = False # if already recording -> stop recording + backing track
            self.staff.stop_bt()
        self.recording.set_record_state()

    # save recording WITHOUT backing track, only midi input   
    @pyqtSlot()
    def on_click_save_recording(self):

        file_to_save_as_midi = self.recording.create_midi_file_from_recording()
        print(file_to_save_as_midi)
        try:
            print('in try')
            filename = QFileDialog.getSaveFileName(self, "Save as midifile", "","Midi Files (*.mid)")
            save_path = filename[0]
            print(save_path)
            file_to_save_as_midi.save(save_path)   
        except (IOError, OSError) as e:
            print(e.errno)
            print('in except')
            print('fail of upload')
            pass




    # play latest recording 
    @pyqtSlot()
    def on_click_listen(self):

        self.staff.stop_bt()
        self.recording.start_listening_to_recording_thread()
        self.staff.play_bt()
        while self.recording.get_playing_recording_state() == True:
            continue
        self.staff.stop_bt()


    @pyqtSlot()
    def on_click_play(self):
        self.staff.play_bt()

    @pyqtSlot()
    def on_click_pause(self):
        self.staff.pause_bt()

    @pyqtSlot()
    def on_click_stop(self):
        self.staff.stop_bt()

    # to upload a file as Backing Track: opens dialog box
    @pyqtSlot()
    def on_click_upload_file(self):
        print('upolad file')
        self.open_dialog_box()

    # opens dialog box to choose the midi-file to upload as backing track
    def open_dialog_box(self):
        try:
            print('in try')
            filename = QFileDialog.getOpenFileName()
            midi_path = filename[0]
            self.reset_gui_components(midi_path)
        except (IOError, OSError) as e:
            print(e.errno)
            print('in except')
            print('fail of upload')
            pass
        #finally:
            #print('in finally')
            # reset key, staff and labeling when new file is uploaded
    '''        
    def set_midifile(self, midifile): 
        self.staff.set_midifile(midifile)
        self.labeling.set_midifile(midifile)
        for key in WHITE_KEYS:
            key.set_midifile(midifile)
        for key in BLACK_KEYS:
            key.set_midifile(midifile)
    '''

    # reset key, staff and labeling
    def reset_gui_components(self, midi_path):
        midi_path = midi_path
        self.staff.stop_bt()
        this_tonality = song_extracting.getTonality(midi_path)
        self.labeling.reset_labeling_class(midi_path)
        self.staff.reset_staff_class(midi_path)
        self.recording.reset(midi_path)
        for key in WHITE_KEYS:
            key.reset_key_class(this_tonality)
        for key in BLACK_KEYS:
            key.reset_key_class(this_tonality)


    # draw Piano keyboard with 88 keys
    def paintEvent(self, e):
        painter = QPainter(self)    # create the object of QPainter class
        # draw Notelines from staff.py
        self.staff.draw(painter)
        # draw recording bobble
        self.recording.draw(painter)
        # draw keyboard and marker from key.py
        for key in WHITE_KEYS:
            key.draw(painter)
        for key in BLACK_KEYS:
            key.draw(painter)
        return

# every PyQt5 application must create an application object
App = QApplication(sys.argv)
# enter the mainloop of the application. The event handling starts from this point
window = Window()
midi_input = MidiInput()
song_extracting = SongExtracting()

sys.exit(App.exec())
