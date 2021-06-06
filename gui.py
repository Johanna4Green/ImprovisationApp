# this is the MAIN file
# https://codeloop.org/pyqt5-drawing-rectangle-with-qpainter-class/
# this window class creates the gui with PyQt5
# it gets the midiInput from the Thread in the midiInput module/ class
# it calls the draw method of the Key module/ class and draws the piano


from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QInputDialog, QFileDialog, QComboBox
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

        self.mode = "Practice"
        self.current_practice_file = MIDIFILE
        # init buttons, keyboard, dropdown for LearnMode and window
        self.staff = Staff()
        self.init_buttons()
        self.init_droppingdown_crazy()
        self.init_keyboard(88)
        self.init_window()
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
    

    # dropdown menu fpr the learn mode to choose the lecture
    def init_droppingdown_crazy(self):
        self.cmbox = QComboBox(self)
        self.cmbox.addItem('1 - Pentatonik mit schwarzen Tasten')
        self.cmbox.addItem("2 - C-Dur Pentatonik")
        self.cmbox.addItem("3 - C-Dur Tonleiter mit Powerchords")
        self.cmbox.addItem("4 - C-Dur Tonleiter mit Dreiklängen")
        self.cmbox.addItem("5 - C-Dur Tonleiter mit Septakkorden")
        self.cmbox.addItem("6 - A-Moll-Tonleiter")
        self.cmbox.addItem("7 - Kirchentonarten (dorisch)")
        self.cmbox.resize(300,100)
        self.cmbox.move(400,37)
        self.cmbox.setVisible(False)
        index = self.cmbox.currentIndex()
        self.cmbox.currentIndexChanged.connect(self.on_dropdown_changed)    # returns index 0-6 dependent on choosen item 


   # explanation text box for the theory and instructions in the learn mode 
    def init_learn_text_label(self):
        self.learn_text_label = QLabel(self)
        self.learn_text_label.resize (1000, 130)
        self.learn_text_label.move(100, 540)
        self.learn_text_label.setWordWrap(True)
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
       

    # when in learn mode in dropdown something is changed, text is changed and midifile is changed, so gui components must be reset
    @pyqtSlot()
    def on_dropdown_changed(self):
        print('changed')
        index = self.cmbox.currentIndex()
        self.set_learn_text_label(index)
        self.set_path_for_learn_reset(index)
        self.set_special_learn_mode(index)
    
    # depending on choosen lecture in the learn mode, the midifile is changed and the gui components updated 
    def set_path_for_learn_reset(self, index):
        print(index)
        if index == 0:
            path = "sound_midis/1_pentatonik_fisdur.mid"
        elif index == 1:
            path = "sound_midis/2_pentatonik_cdur.mid"
        elif index == 2:
            path = "sound_midis/3_tonleiter_cdur_powerchords.mid"
        elif index == 3:
            path = "sound_midis/4_tonleiter_cdur_chords.mid"
        elif index == 4:
            path = "sound_midis/5_tonleiter_cdur_7chords.mid"
        elif index == 5:
            path = "sound_midis/6_tonleiter_amoll_chords.mid"
        elif index == 6:
            path = "sound_midis/7_cdur_dorisch.mid"
        self.reset_gui_components(path)

    # the text of the lecture text box is changed according to index (given from the dropdown change)
    def set_learn_text_label(self, index):    
        text_1_pentablack = "Die Pentatonik ist eine (penta = 5, griech.) – 5-Tonleiter. Im Gegensatz zur Dur/Moll-Tonleiter fehlen die Halbtonschritte. Scharfe Dissonanzen wie kleine Sekunden und große Septimen sind dadurch ausgeschlossen. Die Pentatonik besteht nur aus großen Sekunden und kleinen Terzen in dieser Reihenfolge: Große Sekunde - Große Sekunde - Kleine Terz - Große Sekunde.\nIn dieser 1. Lektion wird nun in der Fis-Dur-Pentatonik, welche aus den 5 Schwarzen Tasten besteht, improvisiert. Der Backing Track spielt im Wechsel Fis – Cis.\nImprovisiere nun auf den Schwarzen Tasten, spiele zuerst einfach irgendwie und irgendwas, und finde somit Tonfolgen, die dir besonders gefallen."
        text_2_penta_cdur = "In dieser Lektion gibt es immer noch die Pentatonik als Grundlage, nur wechseln wir von den Schwarzen Tasten (Fis-Dur) zu den weißen Tasten und der C-Dur-Pentatonik, welche aus C – D – E – G – A besteht. Der Backing Track spielt im Wechsel C und G.\nImprovisiere frei mit den 5 Tönen der C-Dur Pentatonik."
        text_3_cdur_powerchords = "Nun wird die Pentatonik durch die Heptatonik (griech. „Siebentönigkeit“) erweitert. Alle bekannten Moll- und Dur-Tonleitern sind Heptatoniken. Hier wird die C-Dur-Tonleiter verwendet, die alle 7 weißen Tasten als Tonmaterial bietet.\nVersuche nun ein 2-taktiges Motiv (wie zum Beispiel „Hänschen klein – ging allein“) zu spielen. Und versuche dieses, nach einigen Wiederholungen, rauf und runter, in unterschiedlichen Oktavhöhen zu spielen oder beispielsweise eine kleine Extranote als Vorhaltsnote oder zwischendrin als Extra einzubauen."
        text_4_cdur_chords = "Die C-Dur-Tonleiter als Tonmaterial bleibt, im Backing Track werden noch die Terzen hinzugefügt. Es wird also je Akkord nicht nur die Quinte gespielt C – G, sondern C – E – G.\nVersuche das zuvor gelernte Motiv nun auch in der Geschwindigkeit zu variieren und mit einem anderen Ton anzufangen, das Motiv also einige Halb-/Ganztonschritte zu verschieben. Höre genau hin und finde somit heraus, was dazu passt und was möglich ist."
        text_5_cdur_septakkorde = "Auch hier bleibt die C-Dur-Tonleiter als Tonmaterial, im Backing Track werden noch die Septimen hinzugefügt. „Septakkorde gelten in der traditionellen Harmonik als dissonant und auflösungsbedürftig. In der Jazzharmonik spielt der Septakkord in all seinen Formen eine zentrale Rolle und löst den Dreiklang als harmonisches ‚Basismaterial‘ ab.“  Es wird nur der große Durseptakkord C-E-G-H (mit einer großen Septime, also 11 Halbtonschritten von C nach H) und der Dominantseptakkord G-H-D-F, der kleiner Durseptakkord (mit nur eine kleine Septime, nur 10 Halbtonschritte, von G nach F) gespielt.\nHöre dir den Backing Track an und erkenne die hier gewünschten Dissonanzen, welche ein Lied interessanter machen können. Versuche auch hier mit dem Motiv zu arbeiten und achte auf die Wirkung des Septakkords. Du kannst auch selbst Dissonanzen erproben und probieren eine Sekunde, also zwei direkt nebeneinanderliegende weiße Tasten oder eine schwarze Note, welche nicht zur C-Dur-Tonleiter passt, zu spielen."
        text_6_moll = "Der Unterschied von Dur zu Moll liegt in der Unterschiedlichen Halb-/Ganzton Reihenfolge. Während bei Dur die Halbtonschritte zwischen der 3. und 4. sowie der 6. und 7. Stufe liegen, sind diese bei der Molltonleiter bei 2. und 3., sowie 5. und 6. Die Molltonleiter lässt das Gespielte melancholischer und trauriger klingen.\nHier verwenden wir die A-Moll Tonleiter. Diese bietet dasselbe Tonmaterial wie die C-Dur-Tonleiter, nur ist das A der Grundton. Der Backing Track spielt nun eine Kadenz. Das heißt er spielt die erste (Tonika), dann die vierte (Subdominante), dann die fünfte (Dominante), und schließlich wieder die erste Stufe.\nDein Motiv muss nun in A-Moll transponiert werden. (Transponieren bedeutet so viel wie in eine andere Tonart übertragen.) In diesem Fall ist das einfach, da man es nur verschieben muss. Schwarze Tasten braucht man auch hier nicht verwenden. Versuche dein Motiv nun in A-Moll zu spielen und erkenne den Stimmungswechsel."
        text_7_kirchentonarten = "„Man spricht von Modi bzw. Kirchentonarten, um diese Tonskalen von den heute gebräuchlichen 24 Tonarten (12 Dur- und 12-Molltonarten) zu unterscheiden. Außerdem sind die Kirchentonarten keine Tonleitern im modernen Sinn, sondern Skalenausschnitte, die das Tonmaterial von modellartig verwendeten Melodien enthalten. Man unterscheidet 7 modale Tonleitern, die sich durch die unterschiedliche Anordnung der Halbtonschritte voneinander unterscheiden:\nIonisch (c–c),   Dorisch (d–d),   Phrygisch (e–e),   Lydisch (f–f),   Mixolydisch (g–g),   Äolisch (a–a),   Lokrisch (h–h).“\nIn diesem Beispiel wird die 2. Skala verwendet. Bei C-Dur dorisch wird jeder Ton um eins nach oben verschoben. Versuche auch hier dein Motiv zu spielen und durch verschiedene Improvisationen abzuwandeln." 
       
        print(index)
        if index == 0:
            self.learn_text_label.setText(text_1_pentablack)
        elif index == 1:
            self.learn_text_label.setText(text_2_penta_cdur)
        elif index == 2:
            self.learn_text_label.setText(text_3_cdur_powerchords)
        elif index == 3:
            self.learn_text_label.setText(text_4_cdur_chords)
        elif index == 4:
            self.learn_text_label.setText(text_5_cdur_septakkorde)
        elif index == 5:
            self.learn_text_label.setText(text_6_moll)
        elif index == 6:
            self.learn_text_label.setText(text_7_kirchentonarten)


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
        elif index == 2:
            pass    
        elif index == 3:
            pass
        elif index == 4:
            pass
        elif index == 5:    # for the 6. Lecture A-Moll, nur C-Dur must be written
            self.labeling.reset_tonality_label("Tonart: A - Moll")
        elif index == 6:
            pass


    # practice mode is activated
    @pyqtSlot()
    def on_click_practice(self):
        print('practice mode activated')
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
        print('learn mode activated')
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
            self.current_practice_file = midi_path
            self.reset_gui_components(midi_path)
        except (IOError, OSError) as e:
            print(e.errno)
            print('in except')
            print('fail of upload')
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