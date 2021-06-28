# this is the MAIN file
# https://codeloop.org/pyqt5-drawing-rectangle-with-qpainter-class/
# this window class creates the gui with PyQt5
# it gets the midiInput from the Thread in the midiInput module/ class
# it calls the draw method of the Key module/ class and draws the piano


from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QInputDialog, QFileDialog, QComboBox, QSpinBox, QLineEdit, QShortcut
from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QPixmap, QColor, QFont, QKeySequence
from PyQt5.QtCore import Qt, QTimer, pyqtSlot

import sys
import time
import os

from constants import *
from midiInput import MidiInput
from staff import Staff
from key import Key
from labeling import Labeling
from recording import Recording
from songExtracting import SongExtracting
from font import os_font


class Window(QMainWindow):

    print(os_font)

    def __init__(self):
        super().__init__()      # exended from class QMainWindow
        self.title = "Improvisation App"
        self.top = WINDOW_UPPER_LEFT_X
        self.left = WINDOW_UPPER_LEFT_Y
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.play_state = "Paused"
        self.play_state_for_recording = "Stopped"
        self.mode = "Practice"
        self.current_practice_file = MIDIFILE
        # init buttons, keyboard, dropdown for LearnMode and window
        self.staff = Staff()
        self.init_buttons()
        self.init_theory_dropdown()
        self.init_bpm_spinner()
        self.init_bmp_label()
        #self.init_countdown_label()
        self.init_keyboard(88)
        self.init_window()
        self.init_key_shortcuts()
        self.init_learn_text_label()
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
    
    # shortcuts for main functions
    # https://zetcode.com/pyqt/qshortcut/
    def init_key_shortcuts(self):
        self.quitSc = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.quitSc.activated.connect(QApplication.instance().quit)
        self.record_Sc = QShortcut(QKeySequence('Ctrl+R'), self)
        self.record_Sc.activated.connect(self.on_click_record)
        self.play_Sc = QShortcut(QKeySequence('Space'), self)
        self.play_Sc.activated.connect(self.on_click_space)
            
    # shortcut Space can be either used for play and pause of backing track, or, if recording, to stop the recording        
    @pyqtSlot()
    def on_click_space(self):
        if self.recording_state == True:
            self.on_click_record()
        else:
            if self.play_state == "Paused":
                self.on_click_play()
            else:
                self.on_click_pause()



    # dropdown menu fpr the learn mode to choose the lecture
    def init_theory_dropdown(self):
        lessons = []
        filelist = os.listdir('theory_files')
        for file in filelist:
            lessons.append(file.split('.')[0])
        self.unique_name_list = list(set(lessons))
        self.unique_name_list.sort()

        self.cmbox = QComboBox(self)
        for name in self.unique_name_list:
            self.cmbox.addItem(name)
       
        self.cmbox.resize(275,30)
        self.cmbox.move(412,70)
        self.cmbox.setVisible(False)
        index = self.cmbox.currentIndex()
        self.cmbox.currentIndexChanged.connect(self.on_dropdown_changed)    # returns index 0-6 dependent on choosen item 

    # bpm spinner to switch the bpm for the backing track from 10 - 200 beats per minute
    def init_bpm_spinner(self):
        self.bpm_spinner = QSpinBox(self)
        self.bpm_spinner.resize(45,30)
        self.bpm_spinner.setMinimum(10)
        self.bpm_spinner.setMaximum(220)
        self.bpm_spinner.setValue(120)
        self.bpm_spinner.move(700,70)
        self.bpm_spinner.setFont(QFont(os_font))
        bpm_number = self.bpm_spinner.value()
        self.bpm_spinner.valueChanged.connect(self.on_bpm_changed)

    def init_bmp_label(self):
        bpm_label = QLabel(self)
        bpm_label.setFont(QFont(os_font))
        bpm_label.move(750,70)
        bpm_label.setText("BPM")  

   # explanation text box for the theory and instructions in the learn mode 
    def init_learn_text_label(self):
        self.learn_text_label = QLabel(self)
        self.learn_text_label.resize (1000, 130)
        self.learn_text_label.move(100, 540)
        self.learn_text_label.setWordWrap(True)
        self.learn_text_label.setFont(QFont(os_font, 14))
        self.learn_text_label.setText("")
        self.learn_text_label.show()


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
        self.record_button = QPushButton('Record', self)
        self.record_button.setToolTip('to record your playing')
        self.record_button.move(757,280)
        self.record_button.resize(120,26)
        self.record_button.clicked.connect(self.on_click_record)
        # listen to recording
        self.listen_button = QPushButton('Play recording', self)
        self.listen_button.setToolTip('to listen to your recording')
        self.listen_button.resize(120,26)
        self.listen_button.move(887,280)
        self.listen_button.clicked.connect(self.on_click_listen)
        self.listen_button.setEnabled(False)
        # save recording
        self.save_recording_button = QPushButton('Save recording', self)
        self.save_recording_button.setToolTip('to save your recording')
        self.save_recording_button.resize(120,26)
        self.save_recording_button.move(1007,280)
        self.save_recording_button.clicked.connect(self.on_click_save_recording)
        self.save_recording_button.setEnabled(False)
        # upload button
        self.upload_button = QPushButton('Upload track', self)
        self.upload_button.setToolTip('to upload a backing track from your computer')
        self.upload_button.resize(120,26)
        self.upload_button.move(1007,70)
        self.upload_button.clicked.connect(self.on_click_upload_file)
        # practice button
        self.practice_button = QPushButton('Practice mode', self)
        self.practice_button.setToolTip('to switch to the practice mode')
        self.practice_button.resize(400,40)
        self.practice_button.move(650,10)
        self.practice_button.clicked.connect(self.on_click_practice)
        self.practice_button.setFocus()
        # learn button
        self.learn_button = QPushButton('Learn mode', self)
        self.learn_button.setToolTip('to switch to the learn mode course')
        self.learn_button.resize(400,40)
        self.learn_button.move(150,10)
        self.learn_button.clicked.connect(self.on_click_learn)
       
    # when the bpm is changed, the new bpm must be given to staff
    @pyqtSlot()
    def on_bpm_changed(self):
        bpm  = self.bpm_spinner.value()
        self.staff.change_bpm(bpm)
      

    # when in learn mode in dropdown something is changed, text is changed and midifile is changed, so gui components must be reset
    @pyqtSlot()
    def on_dropdown_changed(self):
        index = self.cmbox.currentIndex()
        self.set_learn_text_label(index)
        self.set_path_for_learn_reset(index)
        self.set_special_learn_mode(index)
    
    # depending on choosen lecture in the learn mode, the midifile is changed and the gui components updated 
    def set_path_for_learn_reset(self, index):
        path = 'theory_files/' + self.unique_name_list[index] + '.mid'
        self.reset_gui_components(path)
        
    # the text of the lecture text box is changed according to index (given from the dropdown change)
    def set_learn_text_label(self, index):   
        path = 'theory_files/' + self.unique_name_list[index] + '.txt'
        theory_text = open(path, 'r')
        theory_lines = theory_text.readlines()
        text = ""
        for line in theory_lines:
            text = text + line
        self.learn_text_label.setText(text)


    # special changes for only show pentatonic colored in 1. and 2. Lecture and write A-Moll in 6. Lecture
    def set_special_learn_mode(self, index):
        if index == 0:   # color only fis dur pentatonik -> black keys
            for key in WHITE_KEYS:
                key.reset_key_class('fis-penta')
            for key in BLACK_KEYS:
                key.reset_key_class('fis-penta')
        elif index == 1:    # color only c dur pentatonik -> c, d, e, g, a
            for key in WHITE_KEYS:
                key.reset_key_class('c-penta')
            for key in BLACK_KEYS:
                key.reset_key_class('c-penta')
        elif index == 5:    # for the 6. Lecture A-Moll, nur C-Dur must be written
            self.labeling.reset_tonality_label("Tonart: A - Moll")


    # practice mode is activated
    @pyqtSlot()
    def on_click_practice(self):
        self.mode = "Practice"
        self.upload_button.setVisible(True)
        self.cmbox.setVisible(False)
        self.learn_text_label.setVisible(False)
        self.learn_button.setFocus(False)
        self.practice_button.setFocus()
        self.reset_gui_components(self.current_practice_file)
    
    # learn mode is activated 
    @pyqtSlot()
    def on_click_learn(self):
        index = self.cmbox.currentIndex()
        self.set_learn_text_label(index)
        self.set_path_for_learn_reset(index)
        self.set_special_learn_mode(index)
        self.cmbox.setVisible(True)
        self.upload_button.setVisible(False)
        self.learn_text_label.setVisible(True)
        self.mode = "Learn"
        self.practice_button.setFocus(False)
        self.learn_button.setFocus() #setCheckable(True)


    # when record is clicked: 
    @pyqtSlot()
    def on_click_record(self):

        if self.recording_state == False: # if not recording yet -> start recording + playing backing track
            self.staff.stop_bt()
            if self.play_state_for_recording == "Stopped":
                pass
            else:
                time.sleep(2.1)
            self.recording_state = True
            self.record_button.setText('Stop recording')
            self.record_button.setToolTip('to stop the recording')
            self.save_recording_button.setEnabled(False)
            self.listen_button.setEnabled(False)
            self.staff.play_bt()    
        else: 
            self.stop_recording()
        self.recording.set_record_state()

    def stop_recording(self):
        self.recording_state = False # if already recording -> stop recording + backing track
        self.record_button.setText('Record')
        self.record_button.setToolTip('to record your playing')
        self.save_recording_button.setEnabled(True)
        self.listen_button.setEnabled(True)
        self.on_click_stop()

    # save recording WITHOUT backing track, only midi input   
    @pyqtSlot()
    def on_click_save_recording(self):

        file_to_save_as_midi = self.recording.create_midi_file_from_recording()
        try:
            filename = QFileDialog.getSaveFileName(self, "Save as midifile", "","Midi Files (*.mid)")
            save_path = filename[0]
            print(save_path)
            file_to_save_as_midi.save(save_path)   
        except FileNotFoundError:
            print("cancel")
            pass
        except (IOError, OSError) as e:
            print('failed to save the recording' + e.eerno)
            pass
        self.save_recording_button.setEnabled(False)
        self.listen_button.setEnabled(False)


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
        self.play_state = "Playing"
        self.play_state_for_recording = "Playing"
        self.staff.play_bt()

    @pyqtSlot()
    def on_click_pause(self):
        self.play_state = "Paused"
        self.play_state_for_recording = "Paused"
        self.staff.pause_bt()

    @pyqtSlot()
    def on_click_stop(self):
        self.play_state_for_recording = "Stopped"
        self.staff.stop_bt()

    # to upload a file as Backing Track: opens dialog box
    @pyqtSlot()
    def on_click_upload_file(self):
        self.open_dialog_box()

    # opens dialog box to choose the midi-file to upload as backing track
    def open_dialog_box(self):
        try:
            filename = QFileDialog.getOpenFileName()
            midi_path = filename[0]
            self.current_practice_file = midi_path
            self.reset_gui_components(midi_path)
        except FileNotFoundError:
            print("cancel")
            pass
        except (IOError, OSError) as e:
            print('fail of upload' + e.eerno)
            pass
    

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