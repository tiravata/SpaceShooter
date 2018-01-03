bound_break_vert = False
bound_break_gor = False
t = [True, True, True, True]
score = 0
FPS = 30

size = width, height = 720, 576
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
control_keys = [False,False,False,False,False]
ball_speed_limit = 10
#...

#####################      Ships       ####################

#rotation rate, acceleration, deacceleration, enviroment deacceleration, hull, shields, type(mass)
SHIP_CONSTANTS = [[10, 0.25, 0.20, 0.05, 10, 10, 2],
                  [5, 0.1, 0.05, 0.02, 30, 20, 8],
                  [10, 0.25, 0.20, 0.05, 10, 10, 4],
                  [],
                  []]

picked_ship = 2
EXPL = 9
start_lives = 2
