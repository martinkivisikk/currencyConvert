from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import requests
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5 import QtCore
import datetime

class Valuutad:

    def __init__(self) -> None:
        #Saame andmed lehelt floatrates.com sõnastiku kujul.
        self.url = "http://www.floatrates.com/daily/usd.json"
        self.response = requests.get(self.url)
        self.data = self.response.json()
    #Tagastab sõnastiku, kus võtmeks on valuuta nimi, väärtuseks suhe USA dollariga.
    def tee_sõnastik(self):
        self.sõnastik = {
            "USD": 1.0
        }
        
        for key in self.data:
            rida = self.data[key]    
            #self.sõnastik[rida["name"]] = float(rida["rate"])
            self.sõnastik[rida["code"]] = float(rida["rate"])

        return self.sõnastik
    #Tagastab aja, millest kursid pärit on.
    def getDate(self):
        self.kuupäev = self.data["eur"]["date"]

        return self.kuupäev

class Graafik(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graafik")
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.pen = pg.mkPen(color=(255, 0, 0), width=2, style=QtCore.Qt.SolidLine)
        self.graphWidget.setBackground('w')

        #pealkiri, teljed
        self.graphWidget.setTitle("Viimase 7 päeva kurss", color="b", size="15pt")
        self.graphWidget.setLabel('left', 'Kurss')
        self.graphWidget.setLabel('bottom', 'Kuupäev')
        
        self.lastweek = self.getLastWeek()
        print(self.lastweek)

        #andmed ja x,y telg, praegu lihtsalt suvalised nr
        self.hour = [1,2,3,4,5,6,7,8]
        self.temperature = [30,32,34,32,33,31,29,99]
        self.graphWidget.plot(self.hour, self.temperature, pen=self.pen)
        
    def getLastWeek(self):
        self.viimane_nädal = []

        for i in range(0,7):
            self.today = datetime.date.today()
            self.ago = self.today - datetime.timedelta(days=i)
            self.viimane_nädal.append(self.ago)

            self.viimane_nädal.reverse()
        
        return self.viimane_nädal

class GUI(QMainWindow): 

    def __init__(self):
        #Sama, mis QMainWindow.__init__(self). Meie klass GUI on klassi QMainWindow alamklass.
        super().__init__()
        #Pealkiri, mõõtmed ja taustavärv.
        self.pealkiri = "Valuutakursside kalkulaator"
        self.laius = 640
        self.kõrgus = 120
        self.setWindowTitle(self.pealkiri)
        self.setGeometry(10, 10, 0, 0)
        self.setFixedWidth(self.laius)
        self.setFixedHeight(self.kõrgus)
        self.setStyleSheet("background-color: mintcream;")
        self.initGUI()

    def initGUI(self):
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        self.grid = QGridLayout()
        self.wid.setLayout(self.grid)

        #Võtame kuupäeva ja näitame seda ekraanil.
        self.date = Valuutad().getDate()
        self.date_label = QLabel(f"Valuutakursid on ajast {self.date}")

        #Loome sõnastiku.
        self.valuutakursid = Valuutad().tee_sõnastik()
        
        #Menüüd, kust saab soovitud valuutad valida.
        self.vasak_valikukast = QComboBox(self)
        self.parem_valikukast = QComboBox(self)
        self.vasak_valikukast.resize(150, 25)
        self.parem_valikukast.resize(150, 25)

        #Kastid, kuhu saab sisestada ja vastust näha.
        self.vasak_input = QLineEdit(self)
        self.parem_output = QLineEdit(self)
        self.vasak_input.resize(50, 25)
        self.vasak_input.setPlaceholderText("Sisesta")
        self.parem_output.resize(50, 25)
        self.parem_output.setEnabled(False)

        #Nupp, mida vajutades rakendatakse arvuta() funktsiooni.
        self.nupp = QPushButton("Arvuta", self)
        self.nupp.resize(50, 25)
        self.nupp.clicked.connect(self.arvuta)

        self.graafikNupp = QPushButton("Graafik", self)
        self.graafikNupp.resize(50,25)
        self.graafikNupp.clicked.connect(self.graafikuaken)

        #Lisame kõik nupud, kastid ekraanile.
        self.grid.addWidget(self.date_label,0,2,2,2)

        self.grid.addWidget(self.vasak_valikukast,2,0)
        self.grid.addWidget(self.parem_valikukast,2,4)

        self.grid.addWidget(self.vasak_input,3,0)
        self.grid.addWidget(self.parem_output,3,4)

        self.grid.addWidget(self.nupp,1,2,2,2)
        self.grid.addWidget(self.graafikNupp,2,2,2,2)
        
        #QIcon on ikoon kursi kõrvale, key on vastava riigi valuuta nimetus.
        for key in self.valuutakursid:
            self.vasak_valikukast.addItem(QIcon('ikoonid/EU.png'), key)
            self.parem_valikukast.addItem(QIcon('ikoonid/EU.png'), key)
    
    #Paneb parempoolse kasti väärtuseks õige väärtuse.
    def arvuta(self):
        #Sisend on vasakpoolsest kastist.
        self.input_väärtus = self.vasak_input.text()
        self.vasak_valuutakurss = self.valuutakursid[self.vasak_valikukast.currentText()]
        self.parem_valuutakurss = self.valuutakursid[self.parem_valikukast.currentText()]

        try:
            if self.vasak_valikukast.currentText() != "U.S Dollar":
                #Teisendame alguses dollariks, seejärel soovitud valuutaks.
                self.to_usd = float(self.input_väärtus) / self.valuutakursid[self.vasak_valikukast.currentText()]
                self.vastus = str(round(float(self.to_usd * self.parem_valuutakurss), 3))
                self.parem_output.setText(self.vastus)
            else:
                #Teisendame otse.
                self.vastus = str(round(float(self.input_väärtus) * self.parem_valuutakurss, 3))
                self.parem_output.setText(self.vastus)
        #Juhul, kui sisend on vigane.   
        except:
            print("error")

    def graafikuaken(self):
        self.w = Graafik()
        self.w.show()
        #self.hide() peidab esialgse akna nuppu vajutades ära.
        #self.hide()

def rakendus():
    #sys.argv on järjend, mis sisaldab käsurea argumente, võiks panna ka [].
    app = QApplication(sys.argv)
    #Kuvame rakenduse ekraanil.
    kasutajaliides = GUI()
    kasutajaliides.show()
    #Rakendus käib, kuni vajutatakse ristist kinni.
    sys.exit(app.exec_())

rakendus()
