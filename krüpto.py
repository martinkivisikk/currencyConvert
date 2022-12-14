import requests
from bs4 import BeautifulSoup

class Krüptod:
    
    def __init__(self):
        #Leiame veebilehelt vajalikud HTML tagid, kust info kätte saada.
        self.page = requests.get("https://crypto.com/price/showroom/most-watchlisted")
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.soup = self.soup.find_all("tr")
        self.väärtused = {}

    def getKrüptos(self):
        for rida in self.soup:
            vajalik = rida.get_text().split("$")
            if len(vajalik) > 1:
                #Salvestame krüptovaluuta nimetuse ja väärtuse sõnastikku.
                krüpto = vajalik[0].lstrip("0123456789")
                väärtus = float(vajalik[1].replace(",", ""))
                self.väärtused[krüpto] = väärtus

        return self.väärtused
