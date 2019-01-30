from widgets import nonPlayer, existPlayerDialog, db_stuff, utils, ultraSoundMesseges, exitDialog, mp3VSwav, \
    deletePlayer

__author__ = 'e.zarza'

from colorScaleStuff.DiscreteColorRangeSelectorDialog import DiscreteColorRangeSelectorDialog
from colorScaleStuff.GradientColorSelectorDialog import GradientColorSelectorDialog
import sys
import pyqtgraph as pg
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import duetto.audio_signals.AudioSignalPlayer as audioPlayer
from duetto.audio_signals.audio_signals_stream_readers.FileManager import FileManager, Format
import numpy.random as random
from datetime import datetime

try:
    _fromUtf8 = PyQt4.QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class NonPlayer(QDialog, nonPlayer.Ui_nonChoosePlayer_qdialog):
    def __init__(self):
        super(NonPlayer, self).__init__()
        self.setupUi(self)
        self.connect(self.ok_btn, SIGNAL("clicked()"), self.accept)

class DeletePlayer(QDialog, deletePlayer.Ui_deletePlayer_qdialog):
    def __init__(self):
        super(DeletePlayer, self).__init__()
        self.setupUi(self)
        self.connect(self.ok_btn, SIGNAL("clicked()"), self.accept)
        self.connect(self.cancel_btn, SIGNAL("clicked()"), self.reject)

class Exit(QDialog, exitDialog.Ui_exit_qdialog):
    def __init__(self):
        super(Exit, self).__init__()
        self.setupUi(self)
        self.connect(self.ok_btn, SIGNAL("clicked()"), self.accept)
        self.connect(self.cancel_btn, SIGNAL("clicked()"), self.reject)

class PlayerExists(QDialog, existPlayerDialog.Ui_existPlayer_qdialog):
    def __init__(self):
        super(PlayerExists, self).__init__()
        self.setupUi(self)
        self.connect(self.ok_btn, SIGNAL("clicked()"), self.accept)

class UltraSoundSignal(QDialog, ultraSoundMesseges.Ui_ultraSound_qdialog):
    def __init__(self):
        super(UltraSoundSignal, self).__init__()
        self.setupUi(self)
        self.connect(self.ok_btn, SIGNAL("clicked()"), self.accept)

class MainWindow(QMainWindow, mp3VSwav.Ui_MainWindow):
    playingEnd = pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setupUi(self)
        #outside classes
        self.utils= utils.utils()
        self.db= db_stuff.DB_Manager("dataBase.db")
        #class members
        self.wavAddress=self.utils.wavDictionary
        self.tempWavAddres=[]
        self.selected=[False for x in range(len(self.wavAddress))]
        self.quality=self.quality_cBox.currentIndex()
        self.qualityResults_lbl.setText(str(self.quality+1))
        self.count=int(self.spinBox.value())
        self.currentCount=0
        self.original=self.originalSignal_tab
        self.mp3Count=0
        self.wavCount=0
        self.isWavList=[False for x in range(self.count)]
        self.originalSignal=None
        self.compressedSignal=None
        self.fig = Figure()
        self.widget = FigureCanvasQTAgg(self.fig)
        self.playersList=[]
        self.currentPlayer=-1
        self.originalPlayer=audioPlayer.AudioSignalPlayer(self.originalSignal)
        self.originalPlayer.playingDone.connect(self.originalStop)
        self.compressedPlayer=audioPlayer.AudioSignalPlayer(self.compressedSignal)
        self.compressedPlayer.playingDone.connect(self.compressedStop)
        self.lastUserName=""
        # lines de los reproductores
        self.playerLineOscOriginal = pg.InfiniteLine()
        self.playerLineSpecOriginal = pg.InfiniteLine()
        self.playerLineOscOriginal1 = pg.InfiniteLine()
        self.playerLineSpecOriginal1 = pg.InfiniteLine()
        self.playerLineOscCompressed = pg.InfiniteLine()
        self.playerLineSpecCompressed = pg.InfiniteLine()
        # gradiente de colores
        self.discreteColorScale = self.discreteRadioButton.isChecked()
        self.discreteColorGradientTicks = self.utils.defaultDiscreteColorGradientTicks
        self.continuousColorGradientTicks = self.utils.defaultContinuousColorGradientTicks
        # tabs
        self.battleTab=self.battle_tab
        self.options=self.options_tab
        self.statics=self.statics_tab
        self.endTestTab=self.end_tab
        self.research=self.Research_tab
        self.about=self.about_tab
        self.main=self.main_tab
        self.players=self.player_tab
        # additional visual confing
        self.label_12.setText("Rigth :")
        self.label_10.setText("Wrong :")
        self.label_14.setText("Rigth :")
        self.label_15.setText("Wrong :")
        self.totalCountStatics_lbl.setText("0")
        self.mp3CountStatics_lbl.setText("0")
        self.percentStatics_lbl.setText("0%")
        self.wavCountStatics_lbl.setText("0")
        self.welcome_lbl.setHidden(True)
        self.audioFiles_listWidget.addItems(self.wavAddress)
        self.groupBox.setTitle("")
        self.next_btn.setHidden(True)
        # removiendo tabs
        self.tabWidget.removeTab(1)
        self.tabWidget.removeTab(1)
        self.tabWidget.removeTab(1)
        self.tabWidget.removeTab(1)
        self.tabWidget.removeTab(1)
        self.tabWidget.removeTab(1)
        self.tabWidget.removeTab(1)
        self.tabWidget.removeTab(1)
        # ver volumen
        self.horizontalSlider.setHidden(True)
        self.horizontalSlider_2.setHidden(True)
        self.horizontalSlider_3.setHidden(True)
        self.label_24.setHidden(True)
        self.label_25.setHidden(True)
        self.label_21.setHidden(True)
        self.groupBox_10.setMaximumWidth(160)
        self.groupBox_11.setMaximumWidth(160)
        self.groupBox_8.setMaximumWidth(160)
        # plot widgets confing
        self.total_pw.setLabel('bottom', "Signals")
        self.total_pw.setMouseEnabled(x=False, y=False)
        self.total_pw.setMenuEnabled(False)
        # flags
        self.chooseOrAdd=False
        self.signal1IsWave=True
        self.choosen=False
        self.isDelete=False
        self.playerComboBoxChang=False
        self.playersListWidgetChange=False
        self.isUltraSound=False

        # self.horizontalSlider_2.setValue(50)
        # self.horizontalSlider.setValue(50)
        # self.horizontalSlider_3.setValue(50)
        self.volumen=self.horizontalSlider.value()
        self.volumenS1=self.horizontalSlider_2.value()
        self.volumenS2=self.horizontalSlider_3.value()
         #init methods
        self.loadPlayersDB()
        if len(self.playersList)==0:
            self.removePlayer_btn.setHidden(True)
        # connecting events
        self.start_btn.clicked.connect(self.start_event)
        self.start_btn_2.clicked.connect(self.start2_event)
        self.select1_btn.clicked.connect(self.selectSignal1)
        self.select2_btn.clicked.connect(self.selectSignal2)
        self.next_btn.clicked.connect(self.start_event)
        self.options_btn.clicked.connect(self.options_event)
        self.statics_btn.clicked.connect(self.statics_event)
        self.research_btn.clicked.connect(self.research_event)
        self.okOptions_btn.clicked.connect(self.OkOptions_evnt)
        self.about_btn.clicked.connect(self.about_event)
        self.backStatics_btn.clicked.connect(self.Ok_evnt)
        self.cancel_btn.clicked.connect(self.Ok_evnt)
        self.back_btn.clicked.connect(self.Ok_evnt)
        self.aboutBack_btn.clicked.connect(self.Ok_evnt)
        self.backPlayer_btn.clicked.connect(self.Ok_players_event)
        self.play1_btn.clicked.connect(self.play1_event)
        self.pause1_btn.clicked.connect(self.pause1_event)
        self.stop1_btn.clicked.connect(self.stop1_event)
        self.play2_btn.clicked.connect(self.play2_event)
        self.pause2_btn.clicked.connect(self.pause2_event)
        self.stop2_btn.clicked.connect(self.stop2_event)
        self.originalPlay_btn.clicked.connect(self.originalPlay)
        self.originalPause_btn.clicked.connect(self.originalPause)
        self.originalStop_btn.clicked.connect(self.originalStop)
        self.toolButton.clicked.connect(self.chooseFile)
        self.addFiles_tb.clicked.connect(self.addFiles)
        self.backOriginal_btn.clicked.connect(self.resetValues_event)
        self.backEnd_btn.clicked.connect(self.resetValues_event)
        self.endTestOrigianl_btn.clicked.connect(self.endTestOriginal)
        self.players_btn.clicked.connect(self.player_event)
        self.addPlayer_btn.clicked.connect(self.addPlayer_event)
        self.horizontalSlider.valueChanged.connect(self.volumen_event)
        self.horizontalSlider_2.valueChanged.connect(self.volumen_signal1_event)
        self.horizontalSlider_3.valueChanged.connect(self.volumen_signal2_event)
        self.addNewPlayer_btn_2.clicked.connect(self.addNewPlayer_event)
        self.cancelAddPlayer_btn.clicked.connect(self.cancelNewPlayer_event)
        self.players_cBox.currentIndexChanged.connect(self.playerChange_ComboBox_event)
        self.player_listWidget.currentItemChanged.connect(self.choosePlayerList_event)
        self.player_listWidget.itemClicked.connect(self.choosePlayerList_event)
        self.removePlayer_btn.clicked.connect(self.removePlayer_evetn)
        self.qualityStatics_cb.currentIndexChanged.connect(self.getGeneralStatics)

    def initializeParams(self):
        # falgs
        self.signal1IsWave=True
        self.choosen=False
        self.isDelete=False
        self.playerComboBoxChang=False
        self.playersListWidgetChange=False
        self.isUltraSound=False
        self.chooseOrAdd=False
        self.count=int(self.spinBox.value())
        self.currentCount=0
        self.original=self.originalSignal_tab
        self.mp3Count=0
        self.wavCount=0
        self.discreteColorScale = self.discreteRadioButton.isChecked()
        self.quality=self.quality_cBox.currentIndex()
        self.qualityResults_lbl.setText(str(self.quality+1))
        self.selected=[False for x in range(len(self.wavAddress))]
        self.isWavList=[False for x in range(self.count)]
        self.originalSignal=""
        self.compressedSignal=""
        self.widget.figure.clear()
        self.fig.clear()
        self.widget.setHidden(True)
        self.tempWavAddres=[]
        self.db.close()
        self.db._connect("dataBase.db")

    def start_event(self):
        if self.currentPlayer!=-1:
            if self.currentCount>0:
                self.originalStop()
                self.compressedStop()

            if self.currentCount<self.count:

                self.tabWidget.removeTab(0)
                self.tabWidget.addTab(self.original,"Original WAV")
                self.choosen=False

                r=random.randint(0,len(self.wavAddress))
                #if self.currentCount < self.count:
                while self.selected[r]:
                    r=random.randint(0,len(self.wavAddress))

                self.currentSignal=r
                self.selected[r]=True

                m = FileManager()
                self.originalSignal=m.read(self.wavAddress[self.currentSignal])

                self.isUltraSound=self.originalSignal.samplingRate>self.utils.limitUltraSound

                ##signal.open()

                self.oscilogram_pw.signal=self.originalSignal
                self.oscilogram_pw.graph()
                self.spectogram_pw.signal=self.originalSignal
                self.spectogram_pw.graph()

                self.spectogram_pw.histogram.gradient.restoreState({'mode': 'rgb',
                                                                    'ticks': self.discreteColorGradientTicks
                                                                             if self.discreteColorScale
                                                                             else self.continuousColorGradientTicks})
                self.spectogram_pw.histogram.region.setRegion((-120, 0))


                m.write(self.originalSignal,"data\\MP3\\signalMP3.mp3",Format.MP3,q=self.quality)
                self.compressedSignal=m.read("data\\MP3\\signalMP3.mp3")

                #creando los reproductors
                self.originalPlayer=audioPlayer.AudioSignalPlayer(self.originalSignal)

                self.originalPlayer.playingDone.connect(self.originalStop)

                self.compressedPlayer=audioPlayer.AudioSignalPlayer(self.compressedSignal)
                self.compressedPlayer.playingDone.connect(self.compressedStop)


                self.removePlayerLine()
                self.add_player_line(0, self.originalSignal.length-1,self.oscilogram_pw,self.spectogram_pw,self.playerLineOscOriginal,self.playerLineSpecOriginal)
                self.originalPlayer.playing.connect(lambda frame: self.update_playing_line(frame, self.spectogram_pw,self.playerLineOscOriginal,self.playerLineSpecOriginal))

                r=random.randint(0,2)

                if r==0:
                    self.oscilogram1_pw.signal=self.originalSignal
                    self.spectogram1_pw.signal=self.originalSignal
                    self.oscilogram1_pw.graph()
                    self.spectogram1_pw.graph()

                    self.oscilogram2_pw.signal= self.compressedSignal
                    self.spectogram2_pw.signal= self.compressedSignal
                    self.oscilogram2_pw.graph()
                    self.spectogram2_pw.graph()
                    self.signal1IsWave=True

                    self.add_player_line(0, self.originalSignal.length-1,self.oscilogram1_pw,self.spectogram1_pw,self.playerLineOscOriginal1,self.playerLineSpecOriginal1)
                    self.originalPlayer.playing.connect(lambda frame: self.update_playing_line(frame, self.spectogram1_pw,self.playerLineOscOriginal1,self.playerLineSpecOriginal1))

                    self.add_player_line(0, self.compressedSignal.length-1,self.oscilogram2_pw,self.spectogram2_pw,self.playerLineOscCompressed,self.playerLineSpecCompressed)
                    self.compressedPlayer.playing.connect(lambda frame: self.update_playing_line(frame, self.spectogram2_pw,self.playerLineOscCompressed,self.playerLineSpecCompressed))


                else:
                    self.oscilogram2_pw.signal=self.originalSignal
                    self.spectogram2_pw.signal=self.originalSignal
                    self.oscilogram2_pw.graph()
                    self.spectogram2_pw.graph()

                    self.oscilogram1_pw.signal= self.compressedSignal
                    self.spectogram1_pw.signal= self.compressedSignal
                    self.oscilogram1_pw.graph()
                    self.spectogram1_pw.graph()
                    self.signal1IsWave=False

                    self.add_player_line(0, self.compressedSignal.length-1,self.oscilogram1_pw,
                                         self.spectogram1_pw,self.playerLineOscCompressed,self.playerLineSpecCompressed)

                    self.compressedPlayer.playing.connect(lambda frame: self.update_playing_line
                    (frame, self.spectogram1_pw,self.playerLineOscCompressed,self.playerLineSpecCompressed))


                    self.add_player_line(0, self.originalSignal.length-1,self.oscilogram2_pw,self.spectogram2_pw
                                         ,self.playerLineOscOriginal1,self.playerLineSpecOriginal1)

                    self.originalPlayer.playing.connect(lambda frame: self.update_playing_line
                    (frame, self.spectogram2_pw,self.playerLineOscOriginal1,self.playerLineSpecOriginal1))


                self.spectogram1_pw.histogram.gradient.restoreState({'mode': 'rgb',
                                                                     'ticks': self.discreteColorGradientTicks
                                                                              if self.discreteColorScale
                                                                              else self.continuousColorGradientTicks})
                self.spectogram1_pw.histogram.region.setRegion((-120, 0))

                self.spectogram2_pw.histogram.gradient.restoreState({'mode': 'rgb',
                                                                     'ticks': self.discreteColorGradientTicks
                                                                              if self.discreteColorScale
                                                                              else self.continuousColorGradientTicks})
                self.spectogram2_pw.histogram.region.setRegion((-120, 0))


            else:
                self.endTest()
        else:
            q= NonPlayer()
            q.exec_()

    def start2_event(self):
        self.originalStop()

        self.tabWidget.removeTab(0)
        self.label.hide()
        self.next_btn.setHidden(True)
        self.tabWidget.addTab(self.battleTab,"Choose the Original Signal")

    def selectSignal1(self):
        if not self.choosen:
            self.label.setHidden(False)
            self.next_btn.setHidden(False)
            self.currentCount+=1
            if self.signal1IsWave:
                # self.label.setText("WAV")
                self.label.setPixmap(QPixmap("data\\images\goodd.png"))
                self.wavCount+=1
                self.isWavList[self.currentCount-1]=True

            else:
                self.label.setPixmap(QPixmap("data\\images\wrongg.png"))
                self.mp3Count+=1
                self.isWavList[self.currentCount-1]=False

            self.choosen=True

    def selectSignal2(self):
        if not self.choosen:
            self.label.setHidden(False)
            self.next_btn.setHidden(False)

            if not self.signal1IsWave:
                self.label.setPixmap(QPixmap("data\\images\goodd.png"))
                self.wavCount+=1
                self.isWavList[self.currentCount]=True

            else:
                self.label.setPixmap(QPixmap("data\\images\wrongg.png"))
                self.mp3Count+=1
                self.isWavList[self.currentCount]=False

            self.choosen=True
            self.currentCount+=1

    # region Reproduction Methods
    def play1_event(self):
        if self.signal1IsWave:
            self.originalPlay()
        else:
            self.compressedPlay()
    def play2_event(self):
        if not self.signal1IsWave:
            self.originalPlay()
        else:
            self.compressedPlay()


    def pause1_event(self):
        if self.signal1IsWave:
            self.originalPause()
        else:
            self.compressedPause()
    def pause2_event(self):
        if not self.signal1IsWave:
            self.originalPause()
        else:
            self.compressedPause()

    def stop1_event(self):
        if self.signal1IsWave:
            self.originalStop()
            self.playerLineOscOriginal1.setValue(0)
            self.playerLineSpecOriginal1.setValue(0)
        else:
            self.compressedStop()
    def stop2_event(self):
        if not self.signal1IsWave:
            self.originalStop()
            self.playerLineOscOriginal1.setValue(0)
            self.playerLineSpecOriginal1.setValue(0)
        else:
            self.compressedStop()


    #Metodos que hacen que la reproduccion de la sennal
    def originalPlay(self):
        if self.isUltraSound:
            q= UltraSoundSignal()
            q.exec_()
            self.originalPlayer.signal.samplingRate=self.utils.limitUltraSound

        self.originalPlayer.play()
    def compressedPlay(self):
        if self.isUltraSound:
            q= UltraSoundSignal()
            q.exec_()
            self.compressedPlayer.signal.samplingRate=self.utils.limitUltraSound
        self.compressedPlayer.play()


    #Metodos que pausan la reproduccion  de la sennal
    def originalPause(self):
        self.originalPlayer.pause()
    def compressedPause(self):
        self.compressedPlayer.pause()


    #Metodos que detienen la reproduccion  de la sennal
    def originalStop(self):

        self.originalPlayer.stop()
        self.playingEnd.emit()
        self.playerLineOscOriginal.setValue(0)
        self.playerLineSpecOriginal.setValue(0)

        self.playerLineOscOriginal1.setValue(0)
        self.playerLineSpecOriginal1.setValue(0)


    def compressedStop(self):
        self.compressedPlayer.stop()
        self.playingEnd.emit()
        self.playerLineOscCompressed.setValue(0)
        self.playerLineSpecCompressed.setValue(0)
    # endregion

    @pyqtSlot()
    def on_discreteConfigureButton_clicked(self):
        dialog = DiscreteColorRangeSelectorDialog(self, self.discreteColorGradientTicks)
        if dialog.exec_():
            self.discreteColorGradientTicks = dialog.getGradientTicks()

    @pyqtSlot()
    def on_continuousConfigureButton_clicked(self):
        dialog = GradientColorSelectorDialog(self, self.continuousColorGradientTicks)
        if dialog.exec_():
            self.continuousColorGradientTicks = dialog.getGradientTicks()

    def options_event(self):
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.options,"Options")

    def research_event(self):
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.research,"Resarch")

    def about_event(self):
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.about,"About")

    def statics_event(self):
        if self.currentPlayer!=-1:
            self.tabWidget.removeTab(0)
            self.tabWidget.addTab(self.statics,"Statics")
            self.getGeneralStatics()
        else:
            q= NonPlayer()
            q.exec_()

    def getGeneralStatics(self):
        self.totalStatics_pw.plotItem.clear()
        sessionsList = self.db.get_all_sessions_of_user_quality(str(self.playersList[self.currentPlayer]),self.qualityStatics_cb.currentIndex())

        ey=[]
        totalRigth=0
        totalWrong=0

        for x in range(len(sessionsList)):
            rigth,wrong,date,quality= sessionsList[x]
            if rigth+wrong>0:
                ey.append(100*rigth/(rigth+wrong))
            else:
                ey.append(0)
            totalRigth+=rigth
            totalWrong+=wrong
        ex=[x+1 for x in range(len(ey))]

        self.totalStatics_pw.plotItem.plot(ex,ey,symbol='o', symbolSize=8,antialias=True,pen=pg.mkPen({'color': "w", 'width': 3}))
        self.totalCountStatics_lbl.setText(str(totalRigth+totalWrong))
        self.wavCountStatics_lbl.setText(str(totalRigth))
        self.mp3CountStatics_lbl.setText(str(totalWrong))
        if totalWrong+totalRigth!=0:
            self.percentStatics_lbl.setText(str((100*totalRigth)/(totalRigth+totalWrong))+"%")
        else:
            self.percentStatics_lbl.setText(str(0)+"%")
        self.totalStatics_pw.getAxis("bottom").setTicks([[(x+1,str(x+1))for x in range(len(sessionsList)+1)]])
        self.totalStatics_pw.setLabel('bottom', "Sessions")
        self.totalStatics_pw.setLabel('left', "Percent")

    def Ok_evnt(self):
        if self.chooseOrAdd:
            self.audioFiles_listWidget.clear()
            self.audioFiles_listWidget.addItems(self.wavAddress)
            self.initializeParams()

        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.main,"Main")

    def Ok_players_event(self):
        self.db.close()
        self.db._connect("dataBase.db")
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.main,"Main")

    def resetValues_event(self):
        self.initializeParams()
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.main,"Main")

    def OkOptions_evnt(self):
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.main,"Main")
        if self.chooseOrAdd:
            self.wavAddress=self.tempWavAddres
        if int(self.spinBox.value()) >len(self.wavAddress):
            self.spinBox.setValue(len(self.wavAddress))

        self.initializeParams()

    def endTest(self):
        self.mp3Count_lbl.setText(str(self.mp3Count))
        self.wavCount_lbl.setText(str(self.wavCount))
        self.totalCount_lbl.setText(str(self.count))
        self.percent_lbl.setText(str(100*self.wavCount/self.count)+"%")

        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.endTestTab,"Results")
        self.results()

    def results(self):
        data = [  ## fields are (time, open, close, min, max).

            (x+1,1,0,self.isWavList[x]) for x in range(self.count)

         ]
        self.total_pw.clear()
        self.total_pw.setXRange(0.2,self.count+1)
        self.total_pw.setYRange(0,1)
        item = utils.CandlestickItem(data)
        self.total_pw.addLegend()
        self.total_pw.addItem(item)#,name='WAV')
        self.total_pw.getAxis("left").setTicks([])
        self.total_pw.getAxis("bottom").setTicks([[(x+1,str(x+1))for x in range(self.currentCount)]])

        self.db.insert_session_quality(str(self.playersList[self.currentPlayer]),self.wavCount,self.mp3Count,datetime.now(),self.quality)

        c1 = self.total_pw.plot([0], pen=pg.mkPen({'color': "g", 'width': 3}), name='  Good')
        c2 = self.total_pw.plot([0],pen=pg.mkPen({'color': "r", 'width': 3}), name='  Wrong')

        self.widget=FigureCanvasQTAgg(self.fig)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout_9.addWidget(self.widget, 1, 0, 1, 1)
        self.widget.setMaximumSize(QSize(800, 250))
        self.pieChart(self.wavCount, self.mp3Count)

    def chooseFile(self):
        self.tempWavAddres=[]
        self.chooseOrAdd=True
        filenames = QFileDialog().getOpenFileNames(self, "Wav Files", '', str("Wav (*.wav)"))
        for file in filenames:
            self.tempWavAddres.append(str(file))
        self.audioFiles_listWidget.clear()
        self.audioFiles_listWidget.addItems(self.tempWavAddres)

    def addFiles(self):
        if len(self.tempWavAddres)==0:
            self.tempWavAddres=self.wavAddress

        self.chooseOrAdd=True
        filenames = QFileDialog().getOpenFileNames(self, "Wav Files", '', str("Wav (*.wav)"))
        for file in filenames:
            if not self.tempWavAddres.__contains__(file):
                self.tempWavAddres.append(str(file))
                self.audioFiles_listWidget.addItem(str(file))
                self.chooseOrAdd=True

    def endTestOriginal(self):
        self.mp3Count_lbl.setText(str(self.mp3Count))
        self.wavCount_lbl.setText(str(self.wavCount))
        self.totalCount_lbl.setText(str(self.currentCount))
        if self.currentCount!=0:
            self.percent_lbl.setText(str(100*self.wavCount/self.currentCount)+"%")
        else:
            self.percent_lbl.setText("0")

        self.tabWidget.addTab(self.endTestTab,"Results")
        self.tabWidget.removeTab(0)
        self.partial_results()

    def partial_results(self):

        data = [  ## fields are (time, open, close, min, max).
            (x+1,1,0,self.isWavList[x]) for x in range(self.currentCount)
         ]

        self.total_pw.clear()
        self.total_pw.setXRange(0.2,self.currentCount+1)
        self.total_pw.setYRange(0,1)
        item = utils.CandlestickItem(data)
        self.total_pw.addLegend()
        self.total_pw.addItem(item)
        self.total_pw.getAxis("left").setTicks([])
        self.total_pw.getAxis("bottom").setTicks([[(x+1,str(x+1))for x in range(self.currentCount)]])

        self.db.insert_session_quality(str(self.playersList[self.currentPlayer]),self.wavCount,self.mp3Count,datetime.now(),self.quality)

        c1 = self.total_pw.plot([0], pen=pg.mkPen({'color': "g", 'width': 3}), name='  Good')
        c2 = self.total_pw.plot([0],pen=pg.mkPen({'color': "r", 'width': 3}), name='  Wrong')

        if self.wavCount!=0 or self.mp3Count!=0:
            self.widget=FigureCanvasQTAgg(self.fig)
            self.widget.setObjectName(_fromUtf8("widget"))
            self.gridLayout_9.addWidget(self.widget, 1, 0, 1, 1)
            self.widget.setMaximumSize(QSize(800, 250))
            self.pieChart(self.wavCount, self.mp3Count)

    def pieChart(self,good,wrong):
        self.widget.setHidden(False)
        self.widget.axes = self.fig.add_subplot(111)

        if(good==0):
            self.widget.axes.pie([wrong],labels=['Wrong'],colors=['r'])
        elif(wrong==0):
            self.widget.axes.pie([good],labels=['Rigth'],colors=['g'])
        else:
            self.widget.axes.pie([good,wrong],labels=['Rigth','Wrong'],colors=['g','r'],explode=[0.01,0.01],autopct='%1.1f%%')

    def player_event(self):
        self.tabWidget.removeTab(0)
        self.tabWidget.addTab(self.players,"Players")
        self.addPlayer_GB.setHidden(True)
        if len(self.playersList)==0:
            self.addPlayer_btn.setText("Create Player")

    def addPlayer_event(self):
        self.addPlayer_GB.setHidden(False)

    def volumen_event(self):
        self.volumen=self.horizontalSlider.value()
        self.originalPlayer._volume=self.volumen

    def volumen_signal1_event(self):
        self.volumenS1=self.horizontalSlider_2.value()
        if self.signal1IsWave:
            self.originalPlayer._volume=self.volumenS1
        else:
            self.compressedPlayer._volume=self.volumenS1

    def volumen_signal2_event(self):
        self.volumenS2=self.horizontalSlider_3.value()
        if  not self.signal1IsWave:
            self.originalPlayer._volume=self.volumenS1
        else:
            self.compressedPlayer._volume=self.volumenS1

    def newPlayerAccion(self):
            self.addPlayer_GB.setHidden(True)
            self.namePlayer_lineEdit.clear()

    def addNewPlayer_event(self):
        if self.namePlayer_lineEdit.text()!="":
            if len(self.playersList)==0:
                self.removePlayer_btn.setHidden(False)

            if self.playersList.__contains__(str(self.namePlayer_lineEdit.text())):
                q=PlayerExists()
                q.exec_()
                return

            self.currentPlayer=len(self.playersList)
            self.playersList.append(str(self.namePlayer_lineEdit.text()))
            self.db.insert_user(str(self.playersList[self.currentPlayer]))
            self.players_cBox.addItem(self.playersList[self.currentPlayer])
            self.player_listWidget.addItem(self.namePlayer_lineEdit.text())
            self.players_cBox.setCurrentIndex(self.currentPlayer)
            self.addPlayer_btn.setText("Add New Player")
            self.playerResults_lbl.setText("Player: "+str(self.playersList[self.currentPlayer]))
            self.playerStatics_lbl.setText("Player: "+str(self.playersList[self.currentPlayer]))

        self.newPlayerAccion()

    def playerChange_ComboBox_event(self):
        if not self.isDelete and not self.playersListWidgetChange:
            self.playerComboBoxChang=True
            self.currentPlayer=self.players_cBox.currentIndex()
            self.player_listWidget.setCurrentRow(self.currentPlayer)
            self.playerChange()
            self.playerComboBoxChang=False

    def cancelNewPlayer_event(self):
        self.newPlayerAccion()

    def choosePlayerList_event(self):
        if not self.isDelete and not self.playerComboBoxChang :
            self.playersListWidgetChange=True
            self.currentPlayer=self.player_listWidget.currentRow()
            self.players_cBox.setCurrentIndex(self.currentPlayer)
            self.playerChange()
            self.playersListWidgetChange=False

    def playerChange(self):
        self.setPlayer()
        self.db.delete_lastUser(str(self.lastUserName))
        self.db.insert_lastUser(self.db.get_user_id(str(self.playersList[self.currentPlayer])), str(self.playersList[self.currentPlayer]),self.currentPlayer)

    def setPlayer(self):
        self.playerResults_lbl.setText("Player: "+str(self.playersList[self.currentPlayer]))
        self.playerStatics_lbl.setText("Player: "+str(self.playersList[self.currentPlayer]))
        self.welcome_lbl.setHidden(False)
        self.welcome_lbl.setText("Welcome "+str(self.playersList[self.currentPlayer]+" !!!"))

    def removePlayer_evetn(self):
        if len(self.playersList)>0:
            qdialog=DeletePlayer()
            if qdialog.exec_():
                self.isDelete=True
                item=self.players_cBox.currentIndex()
                self.player_listWidget.takeItem(item)
                self.players_cBox.removeItem(item)
                self.db.delete_user(self.playersList[item])
                # remove at
                temp=[]
                for x in range(item):
                    temp.append(self.playersList[x])
                for x in range(item+1,len(self.playersList)):
                    temp.append(self.playersList[x])
                self.playersList=temp
                self.isDelete=False

                if len(self.playersList)>0:
                    self.players_cBox.setCurrentIndex(item-1)

                else:
                    self.removePlayer_btn.setHidden(True)
                    self.currentPlayer=-1
                    self.addPlayer_btn.setText("Create Player")
                    self.welcome_lbl.setHidden(True)

    def loadPlayersDB(self):
        self.playersList=self.db.get_all_user_names()
        self.players_cBox.addItems(self.playersList)
        self.player_listWidget.addItems(self.playersList)

        if(len(self.playersList)>0):
            playerName,pos=self.db.get_lastUser_name_position()
            self.currentPlayer=pos
            self.lastUserName=playerName
            self.players_cBox.setCurrentIndex(pos)
            self.player_listWidget.setCurrentRow(self.currentPlayer)
            self.setPlayer()

    def update_playing_line(self, frame,spectogram,playerLineOsc,playerLineSpec):
        # draw the line in the axes
        if frame < self.playerLineEnd:
            playerLineOsc.setValue(frame)
            playerLineSpec.setValue(self.from_osc_to_spec(spectogram,frame))

    def removePlayerLine(self):
        # self._playerLineTimer.stop()

        if self.playerLineOscOriginal in self.oscilogram_pw.getPlotItem().getViewBox().addedItems:
            self.oscilogram_pw.getPlotItem().getViewBox().removeItem(self.playerLineOscOriginal)

        if self.playerLineSpecOriginal in self.spectogram_pw.viewBox.addedItems:
            self.spectogram_pw.viewBox.removeItem(self.playerLineSpecOriginal)

        # if self.signal1IsWave:
        if self.playerLineOscOriginal1 in self.oscilogram1_pw.getPlotItem().getViewBox().addedItems:
            self.oscilogram1_pw.getPlotItem().getViewBox().removeItem(self.playerLineOscOriginal1)

        if self.playerLineSpecOriginal1 in self.spectogram1_pw.viewBox.addedItems:
            self.spectogram1_pw.viewBox.removeItem(self.playerLineSpecOriginal1)

        if self.playerLineOscCompressed in self.oscilogram2_pw.getPlotItem().getViewBox().addedItems:
            self.oscilogram2_pw.getPlotItem().getViewBox().removeItem(self.playerLineOscCompressed)

        if self.playerLineSpecCompressed in self.spectogram2_pw.viewBox.addedItems:
            self.spectogram2_pw.viewBox.removeItem(self.playerLineSpecCompressed)

    # else:
        if self.playerLineOscOriginal1 in self.oscilogram2_pw.getPlotItem().getViewBox().addedItems:
            self.oscilogram2_pw.getPlotItem().getViewBox().removeItem(self.playerLineOscOriginal1)

        if self.playerLineSpecOriginal1 in self.spectogram2_pw.viewBox.addedItems:
            self.spectogram2_pw.viewBox.removeItem(self.playerLineSpecOriginal1)

        if self.playerLineOscCompressed in self.oscilogram1_pw.getPlotItem().getViewBox().addedItems:
            self.oscilogram1_pw.getPlotItem().getViewBox().removeItem(self.playerLineOscCompressed)

        if self.playerLineSpecCompressed in self.spectogram1_pw.viewBox.addedItems:
            self.spectogram1_pw.viewBox.removeItem(self.playerLineSpecCompressed)

    def add_player_line(self, initial_value, end_value,oscillogram,spectogram,playerLineOsc,playerLineSpec):
        """
        create the line to show on widgets osc and spec when the signal is been played
        as a way to know what section of the signal is been listened.
        The line (two lines, one for each widget) is added into every widget
        and updated it's value while the sound is played.
        :param initial_value: the initial value of the line in signal data indexes.
        (osc coordinates) the initial value of where the play start.
        :return:
        """
        if not isinstance(initial_value, int):
            raise Exception("value can't be of type different of int")

        self.playerLineEnd = end_value
        #  set the values of the lines for every widget
        playerLineOsc.setValue(initial_value)
        playerLineSpec.setValue(self.from_osc_to_spec(spectogram,initial_value))

        #  add the lines to the widgets if there aren't
        if playerLineOsc not in oscillogram.getViewBox().addedItems:
            oscillogram.getViewBox().addItem(playerLineOsc)

        if playerLineSpec not in spectogram.viewBox.addedItems:
            spectogram.viewBox.addItem(playerLineSpec)

    def from_osc_to_spec(self, spectogram,x):
        return spectogram.specgramHandler.from_osc_to_spec(x)

    def from_spec_to_osc(self, spectogram,x):
        return spectogram.specgramHandler.from_spec_to_osc(x)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()