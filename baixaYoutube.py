from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QFileDialog, QLabel, QProgressBar, QCheckBox, QAction
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt, QDir, QObject, QThread
import youtube_dl
import sys
import os
import re


class Descarregador(QMainWindow):
    def __init__(self):
        super().__init__()
        titol='Descarregador de vídeos de YouTube'
        self.setWindowTitle(titol)
        self.setMinimumSize(600,600)
        self.layout=QVBoxLayout()
        self.centralWidget=QWidget(self)
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        self.lblTitol=QLabel(titol,self.centralWidget)
        self.lblTitol.setFont(QFont('Segoe UI Light',14,QFont.Bold))
        self.layout.addWidget(self.lblTitol)

        self.lblTextExplicacio=QLabel('Introdueix els enllaços dels vídeos que vols descarregar, separats per espais i/o salts de línia.\nTot el que hi hagi a partir del caràcter # serà ignorat.',self.centralWidget)
        self.layout.addWidget(self.lblTextExplicacio)

        self.widgetProces=QWidget(self.centralWidget)
        self.layout.addWidget(self.widgetProces)


        self.textEdit=QTextEdit(self.centralWidget)
        self.textEdit.textChanged.connect(lambda: self.botoDescarregar.setEnabled(self.textEdit.toPlainText()!=''))
        self.layout.addWidget(self.textEdit)

        self.layoutInferior=QHBoxLayout()
        self.layout.addLayout(self.layoutInferior)
        self.cbMP3=QCheckBox('Descarrega només àudio',self)
        self.layoutInferior.addWidget(self.cbMP3)
        self.layoutInferior.addStretch()
        self.botoDescarregar=QPushButton('Descarregar',self.centralWidget)
        self.botoDescarregar.setEnabled(False)
        self.layoutInferior.addWidget(self.botoDescarregar)
        self.botoDescarregar.clicked.connect(self.descarrega)
        self.defineixMenuBar()
    def defineixMenuBar(self):
        menubar=self.menuBar()
        arxiu=menubar.addMenu('Arxiu')
        #Més menús (si calen)

        actNou=QAction('Nou',self)
        actNou.setShortcuts(QKeySequence.New)
        actNou.setStatusTip('Crea una descàrrega nova')
        actNou.triggered.connect(lambda: self.textEdit.setText(''))

        actObrir=QAction('Obrir',self)
        actObrir.setShortcuts(QKeySequence.Open)
        actObrir.setStatusTip('Carrega una llista de vídeos per descarregar')
        actObrir.triggered.connect(self.obrir)

        actDesar=QAction('Desar',self)
        actDesar.setShortcuts(QKeySequence.Save)
        actDesar.setStatusTip('Desa la llista de vídeos per descarregar')
        actDesar.triggered.connect(self.desar)


        arxiu.addAction(actNou)
        arxiu.addAction(actObrir)
        arxiu.addAction(actDesar)
    def obrir(self):
        #filtrar per arxius de text (?)
        arxiu,_=QFileDialog.getOpenFileName(self,'Obrir...',QDir.homePath())
        print(arxiu)
        with open(arxiu) as f:
            self.textEdit.setText(f.read())
    def desar(self):
        arxiu,_=QFileDialog.getSaveFileName(self,'Desar...',QDir.homePath())
        with open(arxiu,'w') as f:
            f.write(self.textEdit.toPlainText())
        pass
    def arreglaText(self,text):
        '''Elimina tots els comentaris (que, bàsicament, comencen per # i fins al final de la línia. També substitueix espais i tabs per salts de línia
        '''
        text=re.sub('#.*','',text)
        text=text.replace('\n',' ')
        text=text.replace('\t',' ')
        text=re.sub('\s\s+','\s',text)
        text=text.strip()
        print(text)
        return text
        pass
    def descarrega(self):
        #triar el directori de descàrrega
        directori=QFileDialog.getExistingDirectory(self.centralWidget,'Desar a',QDir.homePath())
        try:
            os.chdir(directori)
        except:
            os.chdir(QDir.homePath())
        links=self.arreglaText(self.textEdit.toPlainText()).split(' ')
        opts={'outtmpl':'%(title)s.%(ext)s'}
        if self.cbMP3.isChecked():
            opts['postprocessors']=[{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        self.threads=[]
        self.wids=[]
        self.layoutProces=QVBoxLayout()
        self.widgetProces.setLayout(self.layoutProces)
        for link in links:
            self.wids.append(QWidget(self.widgetProces))
            self.layoutProces.addWidget(self.wids[-1])
            print('Anem a declarar el thread')
            self.threads.append(DescarregaFil(opts,link,self.wids[-1]))
            self.threads[-1].start()
        #ydl.download(links)
        self.textEdit.setText('')
class DescarregaFil(QThread):
    def __init__(self,ydl_opts,link,widget):
        print('Comencem la init')
        super().__init__()
        print('Fem la init')
        def hook(d):
            if not hasattr(self,'maxim'):
                self.maxim=True
                self.progressBar.setMaximum(d['total_bytes'])
            self.progressBar.setValue(d['downloaded_bytes'])
            QApplication.processEvents()
            print(d)
        self.ydl_opts={**ydl_opts}
        self.ydl_opts['progress_hooks']=[hook]
        self.link=link
        self.widget=widget
        self.layout=QHBoxLayout()
        self.widget.setLayout(self.layout)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta=ydl.extract_info(link,download=False)
            #print(meta)
            titol=meta['title']
        self.lbl=QLabel(titol)
        self.lbl.setWordWrap(True)
        self.progressBar=QProgressBar(self.widget)
        self.progressBar.setMinimum(0)
        #self.progressBar.setMaximum(num_bytes)
        self.progressBar.setValue(0)
        self.layout.addWidget(self.lbl)
        self.layout.addWidget(self.progressBar)
        print(link)
        print('Init feta')
    def __del__(self):
        self.wait()
        pass
    def run(self):
        print('Anem a declarar el descarregador')
        ydl=youtube_dl.YoutubeDL(self.ydl_opts)
        print('Començarem a descarregar')
        ydl.download([self.link])
        self.widget.hide()


if __name__=='__main__':
    app=QApplication(sys.argv)
    window=Descarregador()
    window.show()
    app.exec()
