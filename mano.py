from pygame.locals import *
import init


class Mano:
    def __init__(self, nome=""):
        self.mano = []
        self.nome = nome

    def ordina_mano(self):
        import operator
        self.mano.sort(key=operator.attrgetter('punti'))
        listaCarteSenzaPunti = []  # sottolista carta con 0 punti
        listaCarteConPunti = []  # sottolista carta con punti
        for carta in self.mano:
            if carta.punti == 0:
                listaCarteSenzaPunti.append(carta)
            else:
                listaCarteConPunti.append(carta)
        listaCarteSenzaPunti.sort(key=operator.attrgetter('valore'))  # ordina la sottolista per valore della carta

        self.mano = listaCarteSenzaPunti + listaCarteConPunti

    def aggiungicarta(self, aggiungi):
        self.mano.append(aggiungi)

    def stampamano(self):
        print("\n", self.nome)
        for carta in self.mano:
            print(" - ", carta)

    def __str__(self):
        for carta in self.mano:
            print(carta)
        return f"mano di {self.nome}\n {self.mano}"

    def cartagiocata(self, carte_sul_tavolo, briscola, mazzovuoto):
        self.ordina_mano()  # mano ordinata per punteggio dal più piccolo al più grande

        if all(x == carte_sul_tavolo[0] for x in
               carte_sul_tavolo):  # se tutti gli elementi sono None sei il primo a iniziare il turno
            giocarta = self.mano[0]  # inizializza giocarta al primo elemento della mano
            for c in self.mano:  # per ogni carta nella mano
                if mazzovuoto:
                    if c.briscola == briscola.briscola:
                        continue
                    else:
                        giocarta = c
                        break
                else:
                    if not c.briscola == briscola.briscola:  # se la carta non è una briscola
                        if (c.punti != 11) and (c.punti != 10):
                            giocarta = c  # assegna questa carta a giocarta
                            break  # break perchè le carte successive hanno punteggio più alto e non conviene giocarle
            self.mano.remove(giocarta)

        else:  # se sei il secondo o successivi a giocare
            giocarta = self.mano[0]

            if mazzovuoto:
                for c in self.mano:
                    if c.briscola == briscola.briscola:
                        continue
                    else:
                        giocarta = c
                        break

            for g in carte_sul_tavolo:
                if g is not None:

                    if g.briscola == briscola.briscola:  # se la carta sul tavolo è una briscola
                        for c in self.mano:
                            if c.briscola != g.briscola:
                                if g.punti == 0 and c.punti == 0:
                                    giocarta = c
                                    break

                            elif c.briscola == g.briscola:
                                if 0 < g.punti < c.punti:
                                    giocarta = c
                                    break

                    elif g.briscola != briscola.briscola:  # se la carta sul tavolo non è una briscola
                        for c in self.mano:
                            if c.briscola != g.briscola:
                                if g.punti == 0 and c.punti == 0 and c.briscola != briscola.briscola:
                                    giocarta = c
                                    break
                                elif g.punti > 0:
                                    if c.briscola == briscola.briscola:
                                        giocarta = c
                            elif c.briscola == g.briscola:
                                if c.punti >= g.punti:
                                    giocarta = c

            self.mano.remove(giocarta)

        return giocarta

    def mostramano(self):
        cartainposizione = [False, False, False]

        if len(self.mano) == 0:
            return
        else:
            if self.nome == "CPU":
                posy = 5
            else:
                posy = init.WINHEIGHT - 195
            posx = [250, 380, 510]
            for i, c in enumerate(self.mano):
                # print("i ", i)
                if c.rect.x > posx[i]:
                    c.rect.x -= 5
                elif c.rect.x < posx[i]:
                    c.rect.x += 5

                if self.nome == "CPU":
                    if c.rect.y > posy:
                        c.rect.y -= 5
                else:
                    if c.rect.y < posy:
                        c.rect.y += 5
                if c.rect.x == posx[i]:
                    cartainposizione[i] = True

                if self.nome == "CPU":
                    init.screen.blit(c.retro, c.rect)
                else:
                    init.screen.blit(c.fronte, c.rect)

            if all(x is True for x in cartainposizione):  # se tutte le carte sono nella rispettiva posizione allora la mano è in posizione
                init.manoinposizione = True