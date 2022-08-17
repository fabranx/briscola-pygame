
import random
import time
from math import sin
import pygame
import sys
from pygame.locals import *


import init
from mazzo import Mazzo, MazzoPunti
from mano import Mano


def mostracartagiocata(nome, carta):
    if carta is None:
        return
    if nome == "Giocatore":
        giocx = 380

    else:  # nome == CPU
        giocx = 440

    giocy = (init.WINHEIGHT - 190) / 2

    if carta.rect.x > giocx:
        carta.rect.x -= 5
    if carta.rect.x < giocx:
        carta.rect.x += 5
    if carta.rect.y < giocy:
        carta.rect.y += 5
    if carta.rect.y > giocy:
        carta.rect.y -= 5

    if carta.rect.x == giocx and carta.rect.y == giocy:
        if nome == "Giocatore":
            init.giocartainposizione = True
        elif nome == "CPU":
            init.cpucartainposizione = True

    init.screen.blit(carta.fronte, carta.rect)


def valutagiocate(pcarta, cartegiocate, primo):
    vincente = cartegiocate[primo]  # inizializza vincente alla prima carta giocata

    for carta in cartegiocate:
        if vincente.briscola == carta.briscola:
            if carta.punti > vincente.punti:
                vincente = carta
            elif carta.punti == vincente.punti:
                if carta.valore > vincente.valore:
                    vincente = carta
        if vincente.briscola != carta.briscola:
            if carta.briscola == pcarta.briscola:
                vincente = carta
    return vincente


def effettomovimento(img, img_rect, anim):
    xblocks = range(0, init.WINWIDTH, 20)  # suddivide tutta la larghezza della finestra in blocchi da 20px
    yblocks = range(0, init.WINHEIGHT, 20)  # suddivide tutta l'altezza della finestra in blocchi da 20px
    anim = anim + 0.03
    img_x = (init.WINWIDTH - img_rect.width) // 2  # centra l'immagine sull'asse x
    img_y = 100    # posizione dell'immagine sull'asse y
    for x in xblocks:
        xpos = (x + (sin(anim + x * .01) * 5))  # posizione dei blocchi da 20px su asse x
        for y in yblocks:
            ypos = (y + (sin(anim + y * .01) * 5))  # posizione dei blocchi da 20px su asse y
            init.screen.blit(img, (x + img_x, y + img_y), (int(xpos), int(ypos), 20, 20))


def schemata_risultati(vincitore, punti_vincitore, mazzipunti):

    # CREAZIONE DEL MESSAGGIO
    testo = "C mostra carte avversario - G mostra le tue carte         Premi ESC per uscire - Premi N per una nuova partita "
    messaggio = text_format(testo, init.fontBold, 20, init.YELLOW)
    mess_rect = messaggio.get_rect()
    mess_rect.bottomright = (init.WINWIDTH-2, init.WINHEIGHT-2)  # -2 offset rispetto all'ombra

    # CREAZIONE OMBRA UGUALE A MESSAGGIO MA SPOSTATO
    messaggio_ombra = text_format(testo, init.fontBold, 20, init.BLACK)  # ombra del testo messaggio
    mess_ombra_rect = messaggio_ombra.get_rect()
    mess_ombra_rect.bottomright = (init.WINWIDTH, init.WINHEIGHT)

    # CARICA LE IMMAGINI
    haivinto = pygame.image.load('media/haivinto.png').convert_alpha()
    haiperso = pygame.image.load('media/haiperso.png').convert_alpha()
    pareggio = pygame.image.load('media/pareggio.png').convert_alpha()

    vinto_rectimg = haivinto.get_rect()
    perso_rectimg = haiperso.get_rect()
    pareggio_rectimg = pareggio.get_rect()

    # TESTO PUNTEGGI
    if vincitore == "Giocatore":
        punteggio_vincitore = text_format(f"IL TUO PUNTEGGIO: {punti_vincitore}", init.fontBold, 50, init.WHITE)
        punt_vin_rect = punteggio_vincitore.get_rect()
        punt_vin_rect.center = (init.WINWIDTH // 2, 300)

        punteggio_perdente = text_format(f"PUNTEGGIO AVVERSARIO: {120-punti_vincitore}", init.fontBold, 50, init.WHITE)
        punt_per_rect = punteggio_perdente.get_rect()
        punt_per_rect.center = (init.WINWIDTH // 2, 400)

        pygame.mixer.music.load('media/victory.wav')
        pygame.mixer.music.play(1)

    elif vincitore == "CPU":
        punteggio_vincitore = text_format(f"PUNTEGGIO AVVERSARIO: {punti_vincitore}", init.fontBold, 50, init.WHITE)
        punt_vin_rect = punteggio_vincitore.get_rect()
        punt_vin_rect.center = (init.WINWIDTH // 2, 300)

        punteggio_perdente = text_format(f"IL TUO PUNTEGGIO: {120 - punti_vincitore}", init.fontBold, 50, init.WHITE)
        punt_per_rect = punteggio_perdente.get_rect()
        punt_per_rect.center = (init.WINWIDTH // 2, 400)

        pygame.mixer.music.load('media/lose.wav')
        pygame.mixer.music.play(1)

    else:  # PAREGGIO
        punteggio_perdente = text_format(f"IL TUO PUNTEGGIO: {punti_vincitore}", init.fontBold, 50, init.WHITE)
        punt_per_rect = punteggio_perdente.get_rect()
        punt_per_rect.center = (init.WINWIDTH // 2, 300)

        punteggio_vincitore = text_format(f"PUNTEGGIO AVVERSARIO: {120 - punti_vincitore}", init.fontBold, 50, init.WHITE)
        punt_vin_rect = punteggio_vincitore.get_rect()
        punt_vin_rect.center = (init.WINWIDTH // 2, 400)

    anim = 0.0  # variabile che gestisce l'animazione

    while True:
        init.screen.fill(init.BLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == ord("n"):
                    start()
                if event.key == ord("g"):
                    player = "Giocatore"
                    mostracartepunti(player, mazzipunti)
                if event.key == ord("c"):
                    player = "CPU"
                    mostracartepunti(player, mazzipunti)

        anim = anim + 0.03  # 0.03 regola la velocità dell'animazione
        if vincitore == "Giocatore":
            effettomovimento(haivinto, vinto_rectimg, anim)
        elif vincitore == "CPU":
            effettomovimento(haiperso, perso_rectimg, anim)
        else:
            effettomovimento(pareggio, pareggio_rectimg, anim)

        init.screen.blit(punteggio_vincitore, punt_vin_rect)
        init.screen.blit(punteggio_perdente, punt_per_rect)

        init.screen.blit(messaggio_ombra, mess_ombra_rect)
        init.screen.blit(messaggio, mess_rect)
        pygame.display.update()
        init.clock.tick(init.FPS)


def mostracartepunti(player, mazzipunti):
    # TESTO MOSTRATO AL CENTRO DELLA SCHERMATA
    testo = text_format(f"Carte {player}", init.fontBold, 50, init.WHITE)
    testo_rect = testo.get_rect()
    testo_rect.center = (init.WINWIDTH // 2, 40)

    # CREAZIONE DEL MESSAGGIO
    testo_messaggio = "Premi ESC per tornare al menu precedente - Premi N per una nuova partita "
    messaggio = text_format(testo_messaggio, init.fontBold, 20, init.YELLOW)
    mess_rect = messaggio.get_rect()
    mess_rect.bottomright = (init.WINWIDTH-2, init.WINHEIGHT-2)  # -2 offset rispetto all'ombra

    # OMBRA MESSAGGIO
    messaggio_ombra = text_format(testo_messaggio, init.fontBold, 20, init.BLACK)
    mess_ombra_rect = messaggio_ombra.get_rect()
    mess_ombra_rect.bottomright = (init.WINWIDTH, init.WINHEIGHT)

    # INDICATORE DESTRO CARTE PAGINA SUCCESSIVA
    freccia_right = pygame.image.load("media/caret-right-solid.png")
    freccia_right = pygame.transform.smoothscale(freccia_right, (20, 50))
    fr_rect = freccia_right.get_rect()
    fr_rect.midright = (init.WINWIDTH, init.WINHEIGHT // 2)  # allineamento a centro destra

    # INDICATORE SINISTRO CARTE PAGINA PRECEDENTE
    freccia_left = pygame.image.load("media/caret-left-solid.png")
    freccia_left = pygame.transform.smoothscale(freccia_left, (20, 50))
    fl_rect = freccia_left.get_rect()
    fl_rect.midleft = (0, init.WINHEIGHT // 2)  # allineamento a centro sinistra

    max_card_x = (init.WINWIDTH-20) // (init.CARDWIDTH + 10)  # 20 margine sinistro iniziale | 10 margine orizzontale tra le carte
    max_card_y = (init.WINHEIGHT-100) // (init.CARDHEIGHT + 10)  # 100 margine superiore iniziale | 10 margine verticale tra le carte
    n_max_card = max_card_x * max_card_y  # -> numero massimo di carte mostrabili a schermo

    inizio = 0  # inizio della lista mazzodeipunti | 0 prima pagina (se le carte sono < n_max_card) | n pagina successiva (se le carte sono > n_max_card)

    if player == "Giocatore":
        idx = 0
    else:
        idx = 1  # "CPU"

    if mazzipunti[idx].lunghezzamazzo() <= n_max_card:
        indicatore = None  # None se le carte sono < di n_max_card. Se ci sono più pagine indicatore assume valore
                           # "destra" per mostrare la pagina successiva o
                           # "sinistra" per mostrare la pagina precedente
    else:
        indicatore = "destra"

    dim_carte = max_card_x * init.CARDWIDTH  # DIMENSIONE OCCUPATA DA UNA RIGA DI CARTE
    dim_spazi = (max_card_x - 1) * 10  # DIMENSIONE SPAZIO TRA LE CARTE
    totale_carte_spazio = dim_carte + dim_spazi  # TOTALE DIMENSIONE
    marg_x = (init.WINWIDTH - totale_carte_spazio) // 2  # MARGINE DESTRO E SINISTRO RIGA, PER CENTRARE LE CARTE

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == ord("n"):
                    start()
                # SE LE CARTE SONO PIU' DI N PREMI LE FRECCETTE PER VISUALIZZARE LE RESTANTI NON MOSTRATE
                if mazzipunti[idx].lunghezzamazzo() > n_max_card:
                    if event.key == K_RIGHT:
                        inizio = n_max_card  # inizio slice lista mazzopunti per mostrare le carte rimanenti non mostrate
                        indicatore = "sinistra"
                    if event.key == K_LEFT:
                        inizio = 0
                        indicatore = "destra"

        init.screen.fill(init.BLUE)

        init.screen.blit(testo, testo_rect)

        # POSIZIONAMENTO DELLE CARTE NELLA FINESTRA
        x, y = marg_x, 80  # coordinate di partenza
        for carta in mazzipunti[idx].mazzodeipunti[inizio:]:
            carta.rect.x = x
            carta.rect.y = y
            if carta.rect.x + init.CARDWIDTH > init.WINWIDTH:
                y += init.CARDHEIGHT + 10  # separa le carte verticalmente di 10px
                x = marg_x  # margine x iniziale nuova riga
                carta.rect.y = y  # assegna posizione x alla carta
                carta.rect.x = x  # assegna posizione y alla carta
            if carta.rect.y + init.CARDHEIGHT > init.WINHEIGHT:  # se la posizione della carta eccede la dimensione y dello schermo, non mostrare le carte rimanenti
                break
            init.screen.blit(carta.fronte, carta.rect)
            x += init.CARDWIDTH + 10  # separa le carte orizzontalmente di 10px

        init.screen.blit(messaggio_ombra, mess_ombra_rect)
        init.screen.blit(messaggio, mess_rect)

        if indicatore == "sinistra":
            init.screen.blit(freccia_left, fl_rect)
        elif indicatore == "destra":
            init.screen.blit(freccia_right, fr_rect)

        pygame.display.update()
        init.clock.tick(init.FPS)


def partita(nomi):
    pygame.display.set_caption('Briscola')
    mazzo = Mazzo()
    mazzo.mescola()
    mani = []
    cartegiocate = [None, None]
    mazzipunti = []

    init.manoinposizione = False
    init.giocartainposizione = True
    init.cpucartainposizione = True

    pygame.mixer.music.load('media/card_sound.wav')

    #  carica immagine freccie che indicano il vincitore della giocata
    try:
        freccia_up = pygame.image.load(f"media/arrow-up.png")
        freccia_up = pygame.transform.smoothscale(freccia_up, (300, 300))

        freccia_down = pygame.image.load(f"media/arrow-down.png")
        freccia_down = pygame.transform.smoothscale(freccia_down, (300, 300))

        freccia_rect = freccia_up.get_rect()
        freccia_rect.center = (init.WINWIDTH // 2, init.WINHEIGHT // 2)
    except FileNotFoundError:
        print("ERRORE CARICAMENTO FILE PNG")
        pygame.quit()
        sys.exit()

    for nome in nomi:
        mani.append(Mano(nome))
        mazzipunti.append(MazzoPunti(nome))

    pcarta = mazzo.primacarta()

    turno = random.randrange(0, 2)  # a chi tocca giocare - 0 Giocatore - 1 CPU
    primo = -1  # chi ha iniziato per prima a giocare. Inizializzato a -1 

    init.manoinposizione, init.giocartainposizione, init.cpucartainposizione
    click = False
    freccia = None  # indicazione della mano vincente (UP o DOWN)

    mazzo.distribuisci(mani, n_carte_mano=3, primo=turno)
    pygame.mixer.music.play(2)
    background_image = pygame.image.load("media/background2.png").convert()

    while True:
        init.screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                click = event.pos

        if init.manoinposizione and (init.giocartainposizione and init.cpucartainposizione):  # attende che l'animazione sia finita
            if turno == 1: # CPU
                if primo == -1:  # primo -> indice del giocatore che gioca per primo
                    primo = 1
                if cartegiocate[1] is None:
                    if len(mani[1].mano) > 0:
                        giocartacpu = mani[1].cartagiocata(cartegiocate, pcarta, mazzo.mazzovuoto())
                        cartegiocate[1] = giocartacpu  # aggiungi carta giocata nella lista delle carte giocate / (posizione 0 il primo a giocare, turno)
                        init.cpucartainposizione = False
                        turno = 0

                        pygame.mixer.music.play(1)

            elif turno == 0: # Giocatore
                if click:
                    if primo == -1:
                        primo = 0
                    if cartegiocate[0] is None:
                        if len(mani[0].mano) > 0:
                            for carta in mani[0].mano:
                                if carta.rect.collidepoint(click):
                                    giocarta = carta
                                    cartegiocate[0] = giocarta
                                    mani[0].mano.remove(giocarta)
                                    turno = 1  # il prossimo a giocare è CPU
                                    init.giocartainposizione = False

                                    init.selected_sound.play()
                                    time.sleep(0.2)
                                    init.selected_sound.stop()
                                    pygame.mixer.music.play(1)

                                    break  # la carta è stata selezionata, interrompe il ciclo

        click = False  # reimposta click in modo che il valore predente non venga memorizzato e non si clicchi per sbaglio su una carta

        if init.giocartainposizione and init.cpucartainposizione:  # se sono state fatte entrambe le giocate rimuovi le
            # cartegiocate
            if cartegiocate[0] is not None and cartegiocate[1] is not None:
                pygame.time.wait(800)
                vincente = valutagiocate(pcarta, cartegiocate, primo)
                ind_vincente = cartegiocate.index(vincente)  # indice carta vincente in cartegiocate
                turno = ind_vincente

                for carta in cartegiocate:
                    mazzipunti[ind_vincente].mazzodeipunti.append(carta)

                if ind_vincente == 0:
                    freccia = "DOWN"
                elif ind_vincente == 1:
                    freccia = "UP"

                cartegiocate = [None, None]
                primo = -1

        if mazzo.pcarta:
            mazzo.mostraPrimaCarta()
        mazzo.mostramazzo()
        mani[0].mostramano()
        mani[1].mostramano()
        mazzo.mostraCarteRimanenti()

        if cartegiocate[turno] is not None:
            mostracartagiocata(nomi[turno], cartegiocate[turno])
        if cartegiocate[(turno + 1) % 2] is not None and (
                init.giocartainposizione or init.cpucartainposizione):  # attende che la carta giocata da "turno" sia in
            # posizione prima di mostrare la carta di risposta
            mostracartagiocata(nomi[(turno + 1) % 2], cartegiocate[(turno + 1) % 2])

        pygame.display.update()
        init.clock.tick(init.FPS)

        if freccia == "UP":
            init.screen.blit(freccia_up, freccia_rect)
            pygame.display.update()
            pygame.time.wait(1200)
            freccia = None
            if not mazzo.mazzovuoto():
                mazzo.distribuisci(mani, n_carte_mano=1, primo=1)  # distribuisce le carte | primo il giocatore vincente | 1 = CPU
                pygame.mixer.music.play(1)
                init.manoinposizione = False

        elif freccia == "DOWN":
            init.screen.blit(freccia_down, freccia_rect)
            pygame.display.update()
            pygame.time.wait(1200)
            freccia = None
            if not mazzo.mazzovuoto():
                mazzo.distribuisci(mani, n_carte_mano=1, primo=0)  # distribuisce le carte - primo il giocatore vincente 0 = giocatore
                pygame.mixer.music.play(1)
                init.manoinposizione = False

        if mazzo.mazzovuoto():
            if (len(mani[0].mano) and len(mani[1].mano)) == 0:
                if all(x is None for x in cartegiocate):
                    print("FINE !!!\n Grazie per aver giocato")

                    punti_gioc = mazzipunti[0].calcolapunti()
                    punti_cpu = mazzipunti[1].calcolapunti()

                    if punti_gioc > punti_cpu:
                        vincitore = mazzipunti[0].nome
                        punti_vincitore = punti_gioc
                    elif punti_cpu > punti_gioc:
                        vincitore = mazzipunti[1].nome
                        punti_vincitore = punti_cpu
                    else:
                        vincitore = "Pareggio"
                        punti_vincitore = 60

                    schemata_risultati(vincitore, punti_vincitore, mazzipunti)


def start():
    giocatori = ["Giocatore", "CPU"]
    partita(giocatori)


# FUNZIONE USATA PER FORMATTARE IL TESTO
def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, True, textColor)

    return newText


def menu():
    selected = "start"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        init.selected_sound.play()
                        time.sleep(0.2)
                        init.selected_sound.stop()
                        start()
                    if selected == "quit":
                        init.selected_sound.play()
                        time.sleep(0.2)
                        init.selected_sound.stop()
                        pygame.quit()
                        sys.exit()

        # Main Menu UI
        init.screen.fill(init.BLUE)
        title = text_format("BRISCOLA", init.fontBold, 90, init.YELLOW)
        if selected == "start":
            text_start = text_format("START", init.fontBold, 75, init.WHITE)
        else:
            text_start = text_format("START", init.fontBold, 75, init.GREY)
        if selected == "quit":
            text_quit = text_format("QUIT", init.fontBold, 75, init.WHITE)
        else:
            text_quit = text_format("QUIT", init.fontBold, 75, init.GREY)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        init.screen.blit(title, (init.WINWIDTH // 2 - (title_rect[2] // 2), 80))  # xxxx_rect[2] è la lunghezza del rettangolo (x,y,width,height)
        init.screen.blit(text_start, (init.WINWIDTH // 2 - (start_rect[2] // 2), 300))
        init.screen.blit(text_quit, (init.WINWIDTH // 2 - (quit_rect[2] // 2), 360))

        pygame.display.update()
        init.clock.tick(init.FPS)
        pygame.display.set_caption("Briscola - Start Menu")


if __name__ == '__main__':
    menu()
