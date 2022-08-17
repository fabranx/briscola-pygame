import pygame
import sys
import os

WINWIDTH = 1100  # lunghezza finestra
WINHEIGHT = 700  # larghezza finestra

FPS = 60
SPEEDCARD = 5  # velocità animazione carte
CARDWIDTH = 120  # larghezza carte
CARDHEIGHT = 190  # altezza carte
MARG_R_MAZZO = 150  # margine destro mazzo
MARG_R_PCARTA = 250  # margine destro prima carta
MARG_B_PCARTA = 280  # margine inferiore prima carta

CYAN = (0, 255, 255)
GREEN = (0, 180, 100)
RED = (255, 0, 0, 100)
WHITE = (255, 255, 255)
BLUE = (0, 80, 200)
YELLOW = (255, 180, 0)
GREY = (50, 50, 50)
BLACK = (0, 0, 0)

if sys.platform.startswith('win32'):
    perc = "CARTE\\"
elif sys.platform.startswith('linux'):
    perc = "CARTE/"

os.environ['SDL_VIDEO_CENTERED'] = '1'  # centra la finestra


programIcon = pygame.image.load('media/icona.png')
pygame.display.set_icon(programIcon)

screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
clock = pygame.time.Clock()

pygame.init()
selected_sound = pygame.mixer.Sound('media/selected.wav')

fontBold = 'media/Quicksand-Bold.otf'
fontRegular = 'media/Quicksand-Regular.otf'

manoinposizione = False
giocartainposizione = True
cpucartainposizione = True