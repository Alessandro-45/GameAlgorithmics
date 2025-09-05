import pygame as pg
import constantes
Ventana = pg.display.set_mode((constantes.Ancho_ventana,
                               constantes.Alto_ventana))

pg.display.set_caption(constantes.nombre_juego)


class GameObject(pg.sprite.Sprite):

    def __init__(self, image, ancho, alto, posx, posy, speed):

        pg.sprite.Sprite.__init__(self)
        self.speed = speed
        self.ancho = ancho
        self.alto = alto
        self.posx = posx
        self.posy = posy
        self.image = pg.transform.scale(
            pg.image.load(image),
            (constantes.ancho_personaje, constantes.alto_personaje))  
    
    def dibujar(self):
        Ventana.blit(self.image, (self.posx, self.posy))


class Personaje(GameObject):
    
    def update(self):

        keys = pg.key.get_pressed()

        if keys[pg.K_UP]:
            self.posy -= self.speed
        if keys[pg.K_DOWN]:
            self.posy += self.speed
        if keys[pg.K_RIGHT]:
            self.posx += self.speed
        if keys[pg.K_LEFT]:
            self.posx -= self.speed
        if keys[pg.K_0]:
            self.posx, self.posy = 0, 0
        
class Enemy(GameObject):

    def move(self):

        if constantes.dir_enemy == 'right':

            self.posx += self.speed
            
            if self.posx >= constantes.Ancho_ventana - 5:
                constantes.dir_enemy = 'left'
        else:

            self.posx -= self.speed
            
            if self.posx <= 3:
                constantes.dir_enemy = 'right'