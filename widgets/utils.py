__author__ = 'e.zarza'

import pyqtgraph as pg
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# import  PyQt4.uic
# PyQt4.uic.compileUiDir("D:\Escuela\!Work\MP3vsWAV")
import sqlite3 as sqlite
import os

class utils:
    def __init__(self):
        self.wavList0=[]

        # self.wavDictionary=["sounds wav vs mp3\\1_2.wav","sounds wav vs mp3\\1_4.wav","sounds wav vs mp3\\2_2.wav","sounds wav vs mp3\\3_4.wav",
        #                    "sounds wav vs mp3\\4_2.wav","sounds wav vs mp3\\5.wav","sounds wav vs mp3\\5_3.wav","sounds wav vs mp3\\6_3.wav",
        #                    "sounds wav vs mp3\\8.wav","sounds wav vs mp3\\8_2.wav","sounds wav vs mp3\\9.wav","sounds wav vs mp3\\9_2.wav",
        #                    "sounds wav vs mp3\\10_2.wav","sounds wav vs mp3\\12_2.wav","sounds wav vs mp3\\13.wav","sounds wav vs mp3\\13_2.wav",
        #                     "sounds wav vs mp3\\15_2.wav","sounds wav vs mp3\\16.wav","sounds wav vs mp3\\17.wav","sounds wav vs mp3\\19.wav",
        #                    "sounds wav vs mp3\\23.wav","sounds wav vs mp3\\Bufo empusus-Alta Habana.wav","sounds wav vs mp3\\Bufo empusus-Zapata.wav",
        #                    "sounds wav vs mp3\Bufo longinasus cajalbanensis.wav","sounds wav vs mp3\E atkinsi Canasi seleccion preferida.wav"
        #
        #                    ]
        self.wavDictionary = []
        for root, dirs, files in os.walk('data\\sounds wav vs mp3'):
            for name in files:
                if os.path.splitext(name)[1] == '.wav':
                    self.wavDictionary.append(os.path.join(root, name))

        self.limitUltraSound=48000

        self.defaultDiscreteColorGradientTicks = [(0, (0, 0, 0, 255)), (0.5, (0, 0, 0, 255)),
                                                  (0.5000001, (0, 127, 0, 255)), (0.6666666, (0, 127, 0, 255)),
                                                  (0.6666667, (255, 255, 0, 255)), (0.8333333, (255, 255, 0, 255)),
                                                  (0.8333334, (255, 0, 0, 255)), (1, (255, 0, 0, 255))]
        self.defaultContinuousColorGradientTicks = [(0, (0, 0, 0, 255)),
                                                    (0.6666666, (0, 0, 0, 255)),
                                                    (0.7777777, (185, 0, 0, 255)),
                                                    (0.8888888, (255, 220, 0, 255)),
                                                    (1, (255, 255, 255, 255))]
        self.gradientEpsilon = 1e-7  # 0.0000001


        # self.connection.execute("CREATE TABLE t(id PRIMARY KEY ASC ,name ,)")

    # def loadOriginalFiles(self):
    #     os.walk()


class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  ## data must have fields: time, open, close,type
        # self.WavMethod=Wav
        self.generatePicture()

    def generatePicture(self):
        ## pre-computing a QPicture object allows paint() to run much more quickly,
        ## rather than re-drawing the shapes every time.
        self.picture = QPicture()
        p = QPainter(self.picture)
        # p.setPen(pg.mkPen('w'))

        if len(self.data)>1:
            w = (self.data[1][0] - self.data[0][0]) / 3.
        else:
            w=0.5

        # if self.WavMethod:
        for (t, open, close,isWav) in self.data:
                # p.drawLine(QPointF(t, min), QPointF(t, max))
            if isWav:
                p.setBrush(pg.mkBrush('g'))
            else:
                p.setBrush(pg.mkBrush('r'))

            p.drawRect(QRectF(t-w, open, w*2, close-open))

        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QRectF(self.picture.boundingRect())

