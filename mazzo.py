from carta import Carta
import init
import random
import pygame

class Mazzo:
    def __init__(self):

        self.maz = []
        self.pcarta = 0
        for brisc in range(0, 4):
            for val in range(1, 11):
                self.maz.append(Carta(brisc, val))
                # print(brisc, val)

        for c in self.maz:  # posiziona tutta le carte del mazzo
            c.rect.x = init.WINWIDTH - init.MARG_R_MAZZO
            c.rect.y = (init.WINHEIGHT - init.CARDHEIGHT) // 2

    def mostramazzo(self):
        if not self.mazzovuoto():
            c = self.maz[-1]  # mostra il retro dell'ultima carta del mazzo
            init.screen.blit(c.retro, c.rect)

    def primacarta(self):
        self.pcarta = self.maz.pop(0)   # pesca la prima carta dal mazzo
        self.pcarta.rect.x = init.WINWIDTH - init.MARG_R_PCARTA          # inizializza posizione della prima carta
        self.pcarta.rect.y = (init.WINHEIGHT - init.MARG_B_PCARTA) // 2
        return self.pcarta

    def mostraCarteRimanenti(self):
        font = pygame.font.Font(init.fontBold, 32)
        text = font.render(f'{len(self.maz) + 1}', True, init.WHITE)  # +1 -> tiene conto anche della prima carta
        textRect = text.get_rect()
        textRect.center = (init.WINWIDTH - init.MARG_R_MAZZO, init.WINHEIGHT // 4)

        if len(self.maz) > 0:
            # self.text = self.font.render(f'{len(self.maz) + 1}', True, GREEN, init.WHITE)  # +1 aggiunge la primacarta
            init.screen.blit(text, textRect)

    def mostraPrimaCarta(self):
        init.screen.blit(self.pcarta.fronte, self.pcarta.rect)

    def mazzovuoto(self):
        if len(self.maz) > 0:
            return False
        else:
            return True

    def mescola(self):
        num_carte = len(self.maz)
        for i in range(num_carte):
            j = random.randrange(i, num_carte)
            self.maz[i], self.maz[j] = self.maz[j], self.maz[i]

    # listagiocatori passata come argomento (array contenente oggetti tipo Mano per ogni giocatore)
    def distribuisci(self, listagiocatori, n_carte_mano=1, primo=0):
        n_mani = len(listagiocatori)  # n_carte_mano (3 prima mano, 1 per le successive)
        for i in range(n_mani):  # per ogni giocatore
            mano = listagiocatori[(primo + i) % n_mani]
            for j in range(n_carte_mano):
                if self.mazzovuoto():
                    pcarta = self.pcarta
                    mano.aggiungicarta(pcarta)
                    self.pcarta = None
                else:
                    carta = self.maz.pop(0)  # pesca dal mazzo una carta
                    mano.aggiungicarta(carta)  # aggiungi carta alla mano di un giocatore



class MazzoPunti:
    def __init__(self, nome=""):
        self.mazzodeipunti = []
        self.nome = nome
        self.puntitotali = 0

    def stampamazzo(self):
        print("Mazzo di ", self.nome)
        for carta in self.mazzodeipunti:
            print(" ", carta)

    def lunghezzamazzo(self):
        return len(self.mazzodeipunti)

    def calcolapunti(self):
        self.puntitotali = 0
        for carta in self.mazzodeipunti:
            self.puntitotali += carta.punti

        return self.puntitotali