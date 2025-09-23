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
        self.rect = self.image.get_rect(topleft=(posx, posy))
    
    def dibujar(self, scroll_x=0):
        # Aplicar scroll para dibujar en posición correcta
        Ventana.blit(self.image, (self.posx - scroll_x, self.posy))

class Personaje(GameObject):
    def __init__(self, image, ancho, alto, posx, posy, speed):
        super().__init__(image, ancho, alto, posx, posy, speed)
        self.vel_y = 0
        self.saltando = False
        self.en_suelo = False
    
    def update(self, walls):
        old_x, old_y = self.posx, self.posy
        
        # Movimiento horizontal (limitado al ancho del mundo)
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
        
        # Manejar colisiones
        self._manejar_colisiones(walls, old_x, old_y)
        
        # Reset con tecla 0
        if keys[pg.K_0]:
            self.posx, self.posy = 100, 100
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
        
        # Limitar caída
        if self.posy > constantes.Alto_ventana:
            self.posy = 100
            self.vel_y = 0

class Enemy(GameObject):
    def __init__(self, image, ancho, alto, posx, posy, speed, direccion='left'):
        super().__init__(image, ancho, alto, posx, posy, speed)
        self.vel_y = 0
        self.en_suelo = False
        self.direccion = direccion  # 'left' o 'right'
    
    def move(self, walls):
        old_x, old_y = self.posx, self.posy
        
        # Movimiento horizontal (siempre hacia la izquierda)
        if self.direccion == 'left':
            self.posx -= self.speed
            # Cambiar dirección si llega al borde de una plataforma o choca con pared
            if self._en_borde_izquierdo(walls) or self._choca_con_pared_izquierda(walls):
                self.direccion = 'right'
        else:
            self.posx += self.speed
            if self._en_borde_derecho(walls) or self._choca_con_pared_derecha(walls):
                self.direccion = 'left'
        
        # Gravedad
        self.vel_y += 0.8
        self.posy += self.vel_y
        
        # Actualizar rectángulo
        self.rect.x = self.posx
        self.rect.y = self.posy
        
        # Manejar colisiones
        self._manejar_colisiones(walls, old_x, old_y)
    
    def _manejar_colisiones(self, walls, old_x, old_y):
        self.en_suelo = False
        
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # Colisión desde arriba
                if old_y + self.alto <= wall.rect.top and self.vel_y > 0:
                    self.posy = wall.rect.top - self.alto
                    self.vel_y = 0
                    self.en_suelo = True
                
                # Colisión desde abajo
                elif old_y >= wall.rect.bottom and self.vel_y < 0:
                    self.posy = wall.rect.bottom
                    self.vel_y = 0
                
                # Colisión lateral izquierda
                elif old_x + self.ancho <= wall.rect.left and self.posx + self.ancho > wall.rect.left:
                    self.posx = wall.rect.left - self.ancho
                    self.direccion = 'right'  # Cambiar dirección
                
                # Colisión lateral derecha
                elif old_x >= wall.rect.right and self.posx < wall.rect.right:
                    self.posx = wall.rect.right
                    self.direccion = 'left'  # Cambiar dirección
    
    def _en_borde_izquierdo(self, walls):
        # Verificar si está en el borde izquierdo de una plataforma
        test_rect = pg.Rect(self.posx - 5, self.posy + self.alto, 5, 5)
        for wall in walls:
            if test_rect.colliderect(wall.rect):
                return False
        return self.en_suelo
    
    def _en_borde_derecho(self, walls):
        # Verificar si está en el borde derecho de una plataforma
        test_rect = pg.Rect(self.posx + self.ancho, self.posy + self.alto, 5, 5)
        for wall in walls:
            if test_rect.colliderect(wall.rect):
                return False
        return self.en_suelo
    
    def _choca_con_pared_izquierda(self, walls):
        test_rect = pg.Rect(self.posx - self.speed, self.posy, self.ancho, self.alto)
        for wall in walls:
            if test_rect.colliderect(wall.rect):
                return True
        return False
    
    def _choca_con_pared_derecha(self, walls):
        test_rect = pg.Rect(self.posx + self.speed, self.posy, self.ancho, self.alto)
        for wall in walls:
            if test_rect.colliderect(wall.rect):
                return True
        return False

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

    def draw_wall(self, scroll_x=0):
        # Dibujar la pared aplicando el scroll
        pg.draw.rect(Ventana, (self.color_1, self.color_2, self.color_3), 
                    (self.rect.x - scroll_x, self.rect.y, self.width, self.height))