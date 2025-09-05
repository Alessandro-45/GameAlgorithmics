import pygame as pg
import constantes
import objetos


pg.init()


personaje = objetos.Personaje(constantes.image_personaje, 
                              constantes.ancho_personaje,
                              constantes.alto_personaje,
                              constantes.pos_ini_player_x, constantes.pos_ini_player_y, constantes.velocidad_player)

enemy = objetos.Enemy(constantes.image_enemy,
                      constantes.ancho_personaje,
                      constantes.alto_personaje,
                      constantes.pos_ini_enemy_x,
                      constantes.pos_ini_enemy_y,
                      constantes.velocidad_player)
clock = pg.time.Clock()



run = True
while run == True:
    clock.tick(60)
    objetos.Ventana.fill((255,255,255))
    for eventos in pg.event.get():

        if eventos.type == pg.QUIT:
            run = False
    personaje.dibujar()
    personaje.update()
    enemy.dibujar()
    enemy.move()

    pg.display.flip()
    








pg.quit()

