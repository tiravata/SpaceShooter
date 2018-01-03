import pygame

import ShipParams as sp
from Assets import *
from Funcs import *
from Controls import *
from Menus import *

fps = sp.FPS

clock = pygame.time.Clock()

def main_loop(realGuy):

    # test = Object(ball_img, 60, 30, 100, 100)
    pl = realGuy

    global tur
    global t
    global score
    global fps
    global SPAWNING_WAVE

    for x, y in enumerate(pl.turrets):
        y.number = x

    while(1):

        global space_lock
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            Menus.pause_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.USEREVENT+1:
                global t
                for x in range(len(t)):
                    t[x] = True
                pygame.time.set_timer(pygame.USEREVENT+1, 0)

            if event.type == pygame.USEREVENT+2:

                pygame.time.set_timer(pygame.USEREVENT+2, 0)

                proX = random.randint(100, 300)
                proY = random.randint(100, 300)

                buff_sp = pygame.sprite.Sprite()
                buff_sp.rect = menu_button.get_rect()
                buff_sp.rect.width = 100
                buff_sp.rect.height = 100
                buff_sp.rect.centerx = width/2
                buff_sp.rect.centery = height/2
                if len(pygame.sprite.spritecollide(buff_sp, asteroids, 0)) == 0:
                    print('Here you go')
                    interface.empty()
                    pl = ship_assign(sp.picked_ship, pl.lives, True)

                else:
                    print('next time')
                    pygame.time.set_timer(pygame.USEREVENT+2, 100)

            if event.type == pygame.USEREVENT+3:
                print('spawning')
                spawn_wave(pl)
                SPAWNING_WAVE = False
                pygame.time.set_timer(pygame.USEREVENT+3, 0)

        ###########     Movement        ###########

        move_all_objects()

        for x in asteroids:
            bound_pass(x)

        """TEST"""
        for m in script_mob_group:
            bound_pass(m)
            m.update()
            m.slow_down()
        """/TEST"""

        for pl in player_group:

            for x in pl.arr_input:
                x(pl, keys)

            pl.slow_down()
            bound_pass(pl)

            for x in pl.player_hull_group:
                orbit_rotate(x.source, x, 0, x.distance, x.angle)
                bound_pass(x)

            for x in pl.turrets:
                bound_pass(x)

            for x in pl.shields:

                x.rect.centerx = x.source.rect.centerx
                x.rect.centery = x.source.rect.centery

            for x in pl.orbiting:
                bound_pass(x)
                orbit_eliptic(pl, x)
            # for i in x.mounts:
            #     orbit_rotate(x, i, 5, 30, 2)

        for x in projectiles:
            bound_pass(x)

        for z in missiles:

            bound_pass(z)
            z.update()
            z.rect.move(z.speed)

        for x in mob_group:

            bound_pass(x)
            x.slow_down()
            # x.accelerate(-x.ENV_DEACCELERATION)
        ##########      Logic       #########

        for x in hit_waves:
            for y in asteroids:
                if pygame.sprite.collide_circle(x, y):
                    x.damage(y)

        for pl in player_group:

            pl.update()

            for i in pl.shields:
                i.rect.move(i.speed)

            for z in pl.player_hull_group:

                # try:
                for i in pygame.sprite.spritecollide(z, asteroids, 0):
                    if i not in noclip_asteroids:
                        i.damage(pl.type*1)

                        if pl.damage(2):
                            break
                # # except:
                #     print('excep')

            for i in pl.shields:
                for i_2 in pygame.sprite.spritecollide(i, asteroids, 0):

                    i_2.damage(5)
                    if len(asteroids) == 0:
                        pygame.time.set_timer(pygame.USEREVENT+3, 2000)
                    i.damage(2*i_2.type)
                    score += i_2.type*10

            for x in pl.turrets:
                x.auto_fire()

            for x in pl.orbiting:
                x.active()

        for i in projectiles:
            for i_2 in pygame.sprite.spritecollide(i, asteroids, 0):
                FX_explosion(i.rect.centerx, i.rect.centery)
                i.damage(i_2)

                if len(asteroids) == 0:
                    pygame.time.set_timer(pygame.USEREVENT+3, 2000)
                score += i_2.type*10

        for i in missiles:
            for i_2 in pygame.sprite.spritecollide(i, asteroids, 0):
                FX_explosion(i.rect.centerx, i.rect.centery)
                i.blow_up()
                if len(asteroids) == 0:
                    pygame.time.set_timer(pygame.USEREVENT+3, 2000)
                score += i_2.type*10

        for i in time_dependent:
            if i.timer < i.time_count:
                i.kill()
            else:
                i.time_count +=1

        if len(asteroids) == 0 and not SPAWNING_WAVE:
            print('spawning...')
            pygame.time.set_timer(pygame.USEREVENT+3, 2000)
            SPAWNING_WAVE = True
        #########      Drwaing      ################

        screen.blit(BG, (0,0))

        #########      Drwaing      ################

#        draw_rotating(obj)
        for pl in player_group:
            draw_rotating(pl)
            speed = np.sqrt(pl.speed[0]**2 + pl.speed[1]**2)
            if speed > 8:
                blur(pl, speed)

            '''Check the hull group sprites'''
            # for x in pl.player_hull_group:
                # pygame.draw.rect(screen, (0,255,0), x.rect)

        for object in asteroids:
            draw_rotating(object)

        for object in noclip_asteroids:
            draw_rotating(object)

        for object in glow:
            object.update()

        """TEST"""
        for x in script_mob_group:
            draw_rotating(x)
        """/TEST"""

        for object in projectiles:
            draw_rotating(object)
            blur(object, object.speed_max)

        for object in missiles:
            draw_rotating(object)
            if object.aim != None:
                draw_triangle(object.aim, (0,255,0), 40, 2)

        for object in effects:
            draw_rotating(object)

        for object in interface:
            screen.blit(object.image, object.rect)

        for pl in player_group:
            pl.show_HP()

            for x in pl.shields:
                draw_rotating(x)
                x.show_HP()

            for x in pl.turrets:

                try:
                    draw_triangle(x.locked, (255, 0, 0), x.locked.rect.width, 1)
                    draw_triangle(x.predict_pos, (255, 0, 0), 5, 1)
                except:
                    pass

            for x in pl.orbiting:

                try:
                    draw_triangle(x.locked, (255, 0, 0), x.locked.rect.width, 1)
                    draw_triangle(x.predict_pos, (255, 0, 0), 5, 1)
                except:
                    pass
                draw_rotating(x)

        #test.rotate(1)

        # for x in test.sub_group:
        #     pygame.draw.rect(screen, (0,255,0), x.rect)
        """colliding rects test"""
        # for z in pl.player_hull_group:
        #     pygame.draw.rect(screen, (0,255,0), z.rect)

        for x in player_group:

            for x_2 in x.mounts:
                x_2.bg_rect.x = x_2.rect.x+3
                x_2.bg_rect.y = x_2.rect.y+3

                try:
                    screen.blit(x_2.bg, x_2.bg_rect)
                except:
                    ptint('wrong')

                draw_rotating(x_2)

        pygame.display.flip()

        for object in effects:
            object.update()

        for x in noclip_asteroids:
            x.update()

        clock.tick(fps)
