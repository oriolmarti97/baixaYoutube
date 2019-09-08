from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QFileDialog, QLabel, QProgressBar, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import youtube_dl
import sys


class Descarregador(QMainWindow):
    def __init__(self):
        super().__init__()
        titol='Descarregador de vídeos de YouTube'
        self.setWindowTitle(titol)
        self.setMinimumSize(800,600)
        self.layout=QVBoxLayout()
        self.centralWidget=QWidget(self)
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        self.lblTitol=QLabel(titol,self.centralWidget)
        self.lblTitol.setFont(QFont('Segoe UI Light',14,QFont.Bold))
        self.layout.addWidget(self.lblTitol)

        self.lblTextExplicacio=QLabel('Introdueix els enllaços dels vídeos que vols descarregar, un per cada línia.',self.centralWidget)
        self.layout.addWidget(self.lblTextExplicacio)

        self.progres=QProgressBar(self.centralWidget)
        self.layout.addWidget(self.progres)
        self.progres.hide()


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

    def descarrega(self):
        #triar el directori de descàrrega
        directori=QFileDialog.getExistingDirectory(self.centralWidget)

        links=self.textEdit.toPlainText().split('\n')
        self.progres.show()
        self.progres.setMinimum(0)
        self.progres.setMaximum(len(links))
        self.progres.setValue(0)
        QApplication.processEvents()
        i=1
        self.setCursor(Qt.WaitCursor)
        opts={'outtmpl':'%(title)s.%(ext)s'}
        if self.cbMP3.isChecked():
            opts['postprocessors']=[{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        with youtube_dl.YoutubeDL(opts) as ydl:
            for x in links:
                ydl.download([x])
                self.progres.setValue(i)
                QApplication.processEvents()
                i+=1
            #ydl.download(links)
        self.textEdit.setText('')
        self.progres.hide()
        self.setCursor(Qt.ArrowCursor)


if __name__=='__main__':
    app=QApplication(sys.argv)
    window=Descarregador()
    window.show()
    app.exec()
