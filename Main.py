import sys
import time
import numpy
import copy
import random
import pygame
import pygame.gfxdraw as gfx
from Menus import main_menu, player_set

#   Effects and particles with gfx lib  -   done
#   complex Colliding   -   done
#   enemies!
#   speed    -   damage(?)
#   turrets 1   -   refract!!!
#   graphs for ML!  -   done
#   modify deacceleration with regards to speed    -   done
#   menues:
#       pause bug    -    done
#       ship picking menue - done
#   better asteroids - done
#   better explosions mechanic - done
#   better hp mechanic - done
#   wave system - doing
#   modify FX system - done
#   make damage system - done
#          remember to kill all temporary Objects! (one bug fixed)

pygame.init()

try:
    s = open('C:/vova/scores.txt', 'r')
    s.close()
except:
    s = open('C:/vova/scores.txt', 'w')
    s.write('1')
    s.close()


# main_menu()
player_set()
