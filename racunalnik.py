#########################################################################
#                                                                       #
#                           Igralec računalnik                          #
#                                                                       #
#########################################################################

import threading
import minimax
import logging

class Racunalnik():
    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem  # algoritem, ki izračuna potezo
        self.mislec = None  # thread, ki razmišlja

    def a_si_ti_kompjuter():
        return True

    def igraj(self):
        """Igraj potezo, ki jo vrne algoritem."""
        # Naredimo vlakno, ki mu podamo kopijo igre (da ne zmede gui-ja).
        self.mislec = threading.Thread(
            target=lambda: self.algoritem.izracunaj_potezo(self.gui.logika.kopija()))

        # Poženemo vlakno:
        self.mislec.start()

        # Preverimo, če je bila najdena poteza:
        self.gui.plosca.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        """Vsakih 100ms preveri, če je algoritem že izračunal potezo."""
        if self.algoritem.poteza is not None:
            # Algoritem je našel potezo, če ni bilo prekinitve, jo naredi.
            self.gui.naredi_potezo(self.algoritem.poteza)
            # Vzporedno vlakno ni več aktivno, zato ga ne rabimo več.
            self.mislec = None
        else:
            # Algoritem še ni našel poteze, preveri še enkrat čez 100ms.
            self.gui.plosca.after(100, self.preveri_potezo)

    def prekini(self):
        """Prekine razmišljanje računalnika."""
        if self.mislec:
            logging.debug("Prekinjamo {0}".format(self.mislec))
            # Algoritmu sporočimo, da mora nehati z razmišljanjem.
            self.algoritem.prekini()
            # Počakamo, da se vlakno ustavi.
            self.mislec.join()
            self.mislec = None

    def klik(self, p):
        """Ignorira klike uporabnika med razmišljanjem računalnika."""
        pass
