import pygame as pg
import constantes
import objetos


pg.init()
def detectar_colision(obj1, obj2):
    rect1 = pg.Rect(obj1.posx, obj1.posy, obj1.ancho, obj1.alto)
    rect2 = pg.Rect(obj2.posx, obj2.posy, obj2.ancho, obj2.alto)
    return rect1.colliderect(rect2)

def colision_con_pared(objeto, lista_paredes):
    rect_obj = pg.Rect(objeto.posx, objeto.posy, objeto.ancho, objeto.alto)
    for pared in lista_paredes:
        if rect_obj.colliderect(pared.rect):
            return True
    return False

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
color1, color2, color3 = 163, 73, 164
wall1 = objetos.Wall(color1, color2, color3, 50, 30,
                     constantes.Ancho_ventana - 400,
                     15)
wall2 = objetos.Wall(color1, color2, color3, 50, 50,
                     constantes.Ancho_ventana - 400,
                     15)

walls = [wall1, wall2]


clock = pg.time.Clock()


finish = False
run = True
while run == True:
    clock.tick(60)
    
    for eventos in pg.event.get():

        if eventos.type == pg.QUIT:
            run = False
    if not finish:
        objetos.Ventana.fill((255, 255, 255))
        personaje.dibujar()
        personaje.update()
        enemy.dibujar()
        enemy.move()
        wall1.draw_wall()
        wall2.draw_wall()

        if detectar_colision(personaje, enemy) or colision_con_pared(personaje, walls):
            objetos.Ventana.fill((163, 73, 164))
            objetos.Ventana.blit(constantes.image_loser, (0,0))
            finish = True

    pg.display.update()
pg.quit()

