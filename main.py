import pygame as pg
import constantes
import objetos


pg.init()


personaje = objetos.Personaje(constantes.image_personaje, 
                              constantes.ancho_personaje,
                              constantes.alto_personaje,
                              10, 10, 15)
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
    

    pg.display.flip()
    








pg.quit()

