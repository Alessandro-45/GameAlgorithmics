import pygame as pg

Ancho_ventana = 1000
Alto_ventana = 800
nombre_juego = 'Mi primer juegazo. Autor: Neptali Ramirez'

dir_enemy = 'right'
pos_ini_player_x = 100
pos_ini_player_y = 100
pos_ini_enemy_x = 600
pos_ini_enemy_y = 600

velocidad_player = 10
velocidad_enemy = 3  # Reducida para mejor control con gravedad

ancho_personaje = 70
alto_personaje = 70
image_personaje = 'pacman.jpg'
image_enemy = 'enemy.png'
background = pg.transform.scale(pg.image.load('Background.jpg'), (Ancho_ventana, Alto_ventana))
image_loser = pg.transform.scale(pg.image.load('loser.webp'), (Ancho_ventana, Alto_ventana))
image_victory = pg.transform.scale(pg.image.load('victory.jpg'), (Ancho_ventana, Alto_ventana))

image_finish = 'finish.webp'

# Nuevas constantes para el mundo expandido
MUNDO_ANCHO = Ancho_ventana * 4  # 4 pantallas de ancho
META_POSX = Ancho_ventana * 3 - 100  # Meta después de 3 shifts