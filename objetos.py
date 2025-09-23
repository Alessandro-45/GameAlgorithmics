import pygame as pg
import constantes

Ventana = pg.display.set_mode((constantes.Ancho_ventana, constantes.Alto_ventana))
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
        self.rect = self.image.get_rect(topleft=(posx, posy))
    
    def update(self):
        # CORRECCIÓN: Mantener rect actualizado con posx, posy
        self.rect.x = self.posx
        self.rect.y = self.posy
    
    def dibujar(self, scroll_x=0):
        Ventana.blit(self.image, (self.posx - scroll_x, self.posy))

class Personaje(GameObject):
    def __init__(self, image, ancho, alto, posx, posy, speed):
        super().__init__(image, ancho, alto, posx, posy, speed)
        self.vel_y = 0
        self.saltando = False
        self.en_suelo = False
    
    def update(self, walls=None):  # CORRECCIÓN: Hacer walls opcional
        if walls is None:
            walls = []
            
        old_x, old_y = self.posx, self.posy
        
        # Movimiento horizontal
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.posx > 0:
            self.posx -= self.speed
        if keys[pg.K_RIGHT] and self.posx < constantes.MUNDO_ANCHO - self.ancho:
            self.posx += self.speed
        
        # Salto
        if keys[pg.K_UP] and self.en_suelo:
            self.vel_y = -15
            self.saltando = True
            self.en_suelo = False
        
        # Gravedad
        self.vel_y += 0.8
        self.posy += self.vel_y
        
        # Actualizar rectángulo
        self.rect.x = self.posx
        self.rect.y = self.posy
        
        # Manejar colisiones si hay walls
        if walls:
            self._manejar_colisiones(walls, old_x, old_y)
        
        # Reset con tecla 0
        if keys[pg.K_0]:
            self.posx, self.posy = 100, 100
            self.vel_y = 0
        
        # Limitar caída
        if self.posy > constantes.Alto_ventana:
            self.posy = 100
            self.vel_y = 0
    
    def _manejar_colisiones(self, walls, old_x, old_y):
        self.en_suelo = False
        
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # Colisión desde arriba
                if old_y + self.alto <= wall.rect.top and self.vel_y > 0:
                    self.posy = wall.rect.top - self.alto
                    self.vel_y = 0
                    self.en_suelo = True
                    self.saltando = False
                
                # Colisión desde abajo
                elif old_y >= wall.rect.bottom and self.vel_y < 0:
                    self.posy = wall.rect.bottom
                    self.vel_y = 0
                
                # Colisión lateral izquierda
                elif old_x + self.ancho <= wall.rect.left and self.posx + self.ancho > wall.rect.left:
                    self.posx = wall.rect.left - self.ancho
                
                # Colisión lateral derecha
                elif old_x >= wall.rect.right and self.posx < wall.rect.right:
                    self.posx = wall.rect.right

class Enemy(GameObject):
    def __init__(self, image, ancho, alto, posx, posy, speed, direccion='left'):
        super().__init__(image, ancho, alto, posx, posy, speed)
        self.vel_y = 0
        self.en_suelo = False
        self.direccion = direccion
    
    def move(self, walls):
        old_x, old_y = self.posx, self.posy
        
        # Movimiento horizontal
        if self.direccion == 'left':
            self.posx -= self.speed
        else:
            self.posx += self.speed
        
        # Gravedad
        self.vel_y += 0.8
        self.posy += self.vel_y
        
        # Actualizar rectángulo
        self.rect.x = self.posx
        self.rect.y = self.posy
        
        # Manejar colisiones
        self._manejar_colisiones(walls, old_x, old_y)
    
    def update(self):
        # CORRECCIÓN: Método update básico para compatibilidad
        self.rect.x = self.posx
        self.rect.y = self.posy
    
    def _manejar_colisiones(self, walls, old_x, old_y):
        self.en_suelo = False
        
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # Colisión desde arriba (aterrizar)
                if old_y + self.alto <= wall.rect.top and self.vel_y > 0:
                    self.posy = wall.rect.top - self.alto
                    self.vel_y = 0
                    self.en_suelo = True
                
                # Colisión lateral - cambiar dirección
                elif self.direccion == 'left' and old_x + self.ancho <= wall.rect.left:
                    self.direccion = 'right'
                    self.posx = wall.rect.left - self.ancho
                elif self.direccion == 'right' and old_x >= wall.rect.right:
                    self.direccion = 'left'
                    self.posx = wall.rect.right

class Wall(pg.sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        pg.sprite.Sprite.__init__(self)
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height

        self.image = pg.Surface([self.width, self.height])
        self.image.fill((color_1, color_2, color_3))

        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def update(self):
        pass  # Las paredes no necesitan actualización

    def draw_wall(self, scroll_x=0):
        pg.draw.rect(Ventana, (self.color_1, self.color_2, self.color_3), 
                    (self.rect.x - scroll_x, self.rect.y, self.width, self.height))