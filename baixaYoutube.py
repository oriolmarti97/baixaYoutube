#Software gràfic per descarregar vídeos de plataformes de vídeo tals com pot ser YouTube
#(english license below)
#Copyright (C) 2019  Oriol Martí i Rodríguez

#Aquest programa és lliure; el podeu redistribuir i/o modificar
# d'acord amb els termes de la Llicència pública general de GNU tal 
# i com la publica la Free Software Foundation; tant se val la versió 3
# de la Llicència com (si ho preferiu) qualsevol versió posterior.


#Aquest programa es distribueix amb l'esperança que serà útil, 
#però SENSE CAP GARANTIA; ni tant sols amb la garantia de 
#COMERCIALITZABILITAT O APTITUD PER A PROPÒSITS DETERMINATS.  Vegeu
#la Llicència general pública de GNU per a més detalls. 


#Hauríeu d'haver rebut una còpia de la llicència pública general 
#de GNU amb aquest programa; si no, consulteu https://www.gnu.org/licenses/



#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QFileDialog, QLabel, QProgressBar, QCheckBox, QAction, QScrollArea, QComboBox
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt, QDir, QObject, QThread, pyqtSignal
import youtube_dl
import sys
import os
import re


class Descarregador(QMainWindow):
    def __init__(self):
        super().__init__()
        titol = 'Descarregador de vídeos de YouTube'
        self.setWindowTitle(titol)
        self.setMinimumSize(600, 600)
        self.layout = QVBoxLayout()
        self.centralWidget = QWidget(self)
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        self.lblTitol = QLabel(titol, self.centralWidget)
        self.lblTitol.setFont(QFont('Segoe UI Light', 14, QFont.Bold))
        self.layout.addWidget(self.lblTitol)

        self.lblTextExplicacio = QLabel(
            'Introdueix els enllaços dels vídeos que vols descarregar, separats per espais i/o salts de línia.\nTot el que hi hagi a partir del caràcter # serà ignorat.', self.centralWidget)
        self.layout.addWidget(self.lblTextExplicacio)

        self.layoutProces = QVBoxLayout()
        self.layoutProces.setSpacing(0)
        self.layout.addLayout(self.layoutProces)

        self.textEdit = QTextEdit(self.centralWidget)
        self.textEdit.textChanged.connect(
            lambda: self.botoDescarregar.setEnabled(self.textEdit.toPlainText() != ''))
        self.layout.addWidget(self.textEdit)

        self.layoutInferior = QHBoxLayout()
        self.layout.addLayout(self.layoutInferior)
        self.cbMP3 = QCheckBox('Descarrega només àudio', self)
        self.layoutInferior.addWidget(self.cbMP3)
        layoutThreads=QHBoxLayout()
        lblThreads=QLabel('Nombre de fils:')
        self.cbThreads=QComboBox(self.centralWidget)
        self.cbThreads.addItems([str(i) for i in range(1,QThread.idealThreadCount())])
        self.cbThreads.setCurrentIndex(self.cbThreads.count()-1)
        layoutThreads.addWidget(lblThreads)
        layoutThreads.addWidget(self.cbThreads)
        self.layoutInferior.addLayout(layoutThreads)
        self.layoutInferior.addStretch()
        self.botoDescarregar = QPushButton('Descarregar', self.centralWidget)
        self.botoDescarregar.setEnabled(False)
        self.layoutInferior.addWidget(self.botoDescarregar)
        self.botoDescarregar.clicked.connect(self.descarrega)
        self.defineixMenuBar()

    def defineixMenuBar(self):
        menubar = self.menuBar()
        arxiu = menubar.addMenu('Arxiu')
        # Més menús (si calen)

        actNou = QAction('Nou', self)
        actNou.setShortcuts(QKeySequence.New)
        actNou.setStatusTip('Crea una descàrrega nova')
        actNou.triggered.connect(lambda: self.textEdit.setText(''))

        actObrir = QAction('Obrir', self)
        actObrir.setShortcuts(QKeySequence.Open)
        actObrir.setStatusTip('Carrega una llista de vídeos per descarregar')
        actObrir.triggered.connect(self.obrir)

        actDesar = QAction('Desar', self)
        actDesar.setShortcuts(QKeySequence.Save)
        actDesar.setStatusTip('Desa la llista de vídeos per descarregar')
        actDesar.triggered.connect(self.desar)

        arxiu.addAction(actNou)
        arxiu.addAction(actObrir)
        arxiu.addAction(actDesar)

    def obrir(self):
        # filtrar per arxius de text (?)
        arxiu, _ = QFileDialog.getOpenFileName(
            self, 'Obrir...', QDir.homePath())
        with open(arxiu) as f:
            self.textEdit.setText(f.read())

    def desar(self):
        arxiu, _ = QFileDialog.getSaveFileName(
            self, 'Desar...', QDir.homePath())
        with open(arxiu, 'w') as f:
            f.write(self.textEdit.toPlainText())

    def arreglaText(self, text):
        '''Elimina tots els comentaris (que, bàsicament, comencen per # i fins al final de la línia. També substitueix espais i tabs per salts de línia
        '''
        text = re.sub('#.*', '', text)
        text = text.replace('\n', ' ')
        text = text.replace('\t', ' ')
        text = re.sub('\s\s+', '\s', text)
        text = text.strip()
        return text

    def descarrega(self):
        #Crea un mostrador de procés (bàsicament conté una label i una progress bar) per un dels threads. Tot penja d'un widget perquè així és més fàcil destruir-ho tot. S'elimina aquest i ja
        def mostradorProces():
            '''El mostrador serà un widget que contindrà un layout i, a dins d'aquest, una label i una progressbar. 
            La label indicarà quin vídeo estem descarregant, i la progressbar per on anem
            Podria fer-ho amb una subclasse de QWidget que fes això en el seu init, però no veig què m'aporta
            '''
            wid=QWidget(self.centralWidget)
            self.layoutProces.addWidget(wid)
            layout = QHBoxLayout()
            wid.setLayout(layout)
            lbl = QLabel(wid)
            lbl.setWordWrap(True)
            progressBar = QProgressBar(wid)
            progressBar.setFixedWidth(400)
            progressBar.setMinimum(0)
            progressBar.setValue(0)
            layout.addWidget(lbl)
            layout.addWidget(progressBar)
            return wid, lbl, progressBar
        self.textEdit.setEnabled(False) #Mentre descarreguem no volem deixar que ens toquin res
        # triar el directori de descàrrega
        directori = QFileDialog.getExistingDirectory(
            self.centralWidget, 'Desar a', QDir.homePath())
        try:
            os.chdir(directori)
        except:
            self.textEdit.setEnabled(True)
            return
        links = self.arreglaText(self.textEdit.toPlainText()).split(' ')
        #El títol de l'arxiu serà el titol del vídeo amb la seva extensió, sense timestamp. El programa serà silenciós, no mostrarà porqueries a la terminal
        opts = {'outtmpl': '%(title)s.%(ext)s', 'quiet': True}
        if self.cbMP3.isChecked():
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        numThreads=int(self.cbThreads.currentText())
        n=len(links)
        k=n//numThreads #k serà la quantitat de vídeos que descarrega cada fil
        k+= 1 if n%numThreads!=0 else 0
        #Convertim la llista en una sèrie de llistes de mida k
        #Com que n no necessàriament és múltiple de k, posem el mínim per no accedir a fora de la llista
        links_per_thread=[links[i:min(i+k,n)] for i in range(0,n,k)]
        mostradors=[]
        i=0
        self.per_acabar=k #Inicialment cap ha acabat, de manera que queden tots per acabar
        def acabat(i):
            self.per_acabar-=1
            if self.per_acabar==0:
                self.textEdit.setText('')
        for link in links_per_thread:
            mostradors.append(mostradorProces())
            def actualitza(titol,valor, valor_max, i):
                mostradors[i][1].setText(titol)
                mostradors[i][2].setValue(valor)
                mostradors[i][2].setMaximum(valor_max)
            def elimina(i):
                mostradors[i][0].hide()
                self.layoutProces.removeWidget(mostradors[i][0])
                self.per_acabar-=1
                if self.per_acabar==0:
                    self.textEdit.setText('')
                    self.textEdit.setEnabled(True)
            thread=DescarregaFil(opts, link, i)
            thread.actualitzaBarra.connect(actualitza)
            thread.finalitzat.connect(elimina)
            thread.start()
            i+=1


class DescarregaFil(QThread):
    #La senyal passarà un string (títol) i tres enters (valor, valor màxim i número de thread)
    actualitzaBarra=pyqtSignal(str,int,int,int)
    #Passa un enter, que és el número de thread
    finalitzat=pyqtSignal(int)
    def __init__(self, ydl_opts, links, num_thread):
        super().__init__()
        self.num_thread=num_thread
        def hook(d):
            try:
                self.actualitzaBarra.emit(d['filename'],d['downloaded_bytes'],d['total_bytes'],self.num_thread)
                #self.lbl.setText(d['filename'])
                #self.progressBar.setMaximum(d['total_bytes'])
                #self.progressBar.setValue(d['downloaded_bytes'])
            except:
                pass
        self.ydl_opts = {**ydl_opts}
        self.ydl_opts['progress_hooks'] = [hook]
        self.links = links

    def __del__(self):
        self.wait()

    def run(self):
        ydl = youtube_dl.YoutubeDL(self.ydl_opts)
        ydl.download(self.links)
        self.finalitzat.emit(self.num_thread)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Descarregador()
    window.show()
    app.exec()
