import pygame
import init


class Carta:
    ListaBriscola = ["bastone", "coppa", "denaro", "spada"]
    ListaValore = ["None", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    ListaPunteggio = [None, 11, 0, 10, 0, 0, 0, 0, 2, 3, 4]

    def __init__(self, briscola=0, valore=0):
        self.briscola = briscola
        self.valore = valore
        self.punti = self.ListaPunteggio[self.valore]

        fronte = pygame.image.load(f"{init.perc}{self.ListaBriscola[briscola]}{self.ListaValore[valore]}.png")
        self.fronte = pygame.transform.smoothscale(fronte, (init.CARDWIDTH, init.CARDHEIGHT))
        retro = pygame.image.load(f"{init.perc}retro.png")
        self.retro = pygame.transform.smoothscale(retro, (init.CARDWIDTH, init.CARDHEIGHT))

        rect = self.fronte.get_rect()
        self.rect = rect.move(init.WINWIDTH - init.MARG_R_MAZZO,
                              (init.WINHEIGHT - init.CARDHEIGHT) // 2)  # inizializza la posizione delle carte

    def __str__(self):
        return f"{self.ListaValore[self.valore]} di {self.ListaBriscola[self.briscola]}"

    def __eq__(self, other):
        try:
            if self.briscola == other.briscola and self.valore == other.valore:
                return True
            else:
                return False
        except AttributeError:
            return False

    def __cmp__(self, other):
        if self.valore > other.valore:
            return 1
        else:
            return -1
