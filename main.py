import pygame as pg
import constantes
import objetos

pg.init()

# Variables para el scroll
scroll_x = 0
scroll_speed = 15

def detectar_colision(obj1, obj2, scroll_x=0):
    # Ajustar colisiones considerando el scroll
    rect1 = pg.Rect(obj1.posx - scroll_x, obj1.posy, obj1.ancho, obj1.alto)
    rect2 = pg.Rect(obj2.posx - scroll_x, obj2.posy, obj2.ancho, obj2.alto)
    return rect1.colliderect(rect2)

# Crear objetos
personaje = objetos.Personaje(constantes.image_personaje, 
                              constantes.ancho_personaje,
                              constantes.alto_personaje,
                              constantes.pos_ini_player_x, 
                              constantes.pos_ini_player_y, 
                              constantes.velocidad_player)

# Meta ubicada después de 3 shifts
meta = objetos.GameObject(constantes.image_finish, 
                          constantes.ancho_personaje,
                          constantes.alto_personaje,
                          constantes.META_POSX,  # Usar la nueva constante
                          constantes.Alto_ventana - 150,
                          0)

color1, color2, color3 = 163, 73, 164

# Crear plataformas expandidas hacia la derecha
walls = []

# Plataformas iniciales (primera pantalla)
walls.append(objetos.Wall(color1, color2, color3, 200, 500, 300, 30))
walls.append(objetos.Wall(color1, color2, color3, 500, 400, 200, 30))
walls.append(objetos.Wall(color1, color2, color3, 100, 300, 250, 30))

# Plataformas segunda pantalla
walls.append(objetos.Wall(color1, color2, color3, 800, 250, 300, 30))
walls.append(objetos.Wall(color1, color2, color3, 1000, 250, 200, 30))
walls.append(objetos.Wall(color1, color2, color3, 1200, 100, 250, 30))

# Plataformas tercera pantalla
walls.append(objetos.Wall(color1, color2, color3, 2200, 450, 400, 30))
walls.append(objetos.Wall(color1, color2, color3, 2600, 300, 200, 30))
walls.append(objetos.Wall(color1, color2, color3, 2400, 150, 150, 30))

# Plataformas cuarta pantalla (donde está la meta)
walls.append(objetos.Wall(color1, color2, color3, 3200, 500, 300, 30))
walls.append(objetos.Wall(color1, color2, color3, 3500, 350, 200, 30))

# Crear enemigos en diferentes plataformas
enemies = []
# Enemigos en primera pantalla
enemies.append(objetos.Enemy(constantes.image_enemy, constantes.ancho_personaje,
                            constantes.alto_personaje, 400, 300, constantes.velocidad_enemy, 'left'))

# Enemigos en segunda pantalla
enemies.append(objetos.Enemy(constantes.image_enemy, constantes.ancho_personaje,
                            constantes.alto_personaje, 1400, 150, constantes.velocidad_enemy, 'left'))

# Enemigos en tercera pantalla
enemies.append(objetos.Enemy(constantes.image_enemy, constantes.ancho_personaje,
                            constantes.alto_personaje, 2500, 100, constantes.velocidad_enemy, 'left'))

# Enemigos en cuarta pantalla
enemies.append(objetos.Enemy(constantes.image_enemy, constantes.ancho_personaje,
                            constantes.alto_personaje, 3300, 300, constantes.velocidad_enemy, 'left'))

clock = pg.time.Clock()
finish = False
run = True

# ... (código anterior igual)

# ... (código anterior igual)

clock = pg.time.Clock()
finish = False
run = True

umbral_scroll = 50  # Margen desde el borde para activar scroll

while run:
    clock.tick(60)
    
    for eventos in pg.event.get():
        if eventos.type == pg.QUIT:
            run = False
    
    if not finish:
       # Nuevo umbral para el cambio de pantalla
        umbral_salto = 200 # 200 píxeles antes del borde

        # Salto a la siguiente pantalla (derecha)
        if personaje.posx - scroll_x > constantes.Ancho_ventana - umbral_salto:
            scroll_x += constantes.Ancho_ventana
        
        # Salto a la pantalla anterior (izquierda)
        elif personaje.posx - scroll_x < umbral_salto and scroll_x > 0:
            scroll_x -= constantes.Ancho_ventana

        # Limitar el scroll
        scroll_x = max(0, min(scroll_x, constantes.MUNDO_ANCHO - constantes.Ancho_ventana))
        # Dibujar todo...
        objetos.Ventana.blit(constantes.background, (0, 0))
        meta.dibujar(scroll_x)
        personaje.dibujar(scroll_x)
        personaje.update(walls)
        
        for enemy in enemies:
            enemy.dibujar(scroll_x)
            enemy.move(walls)
        
        for wall in walls:
            wall.draw_wall(scroll_x)
        
        # Colisiones...
        colision_enemigo = False
        for enemy in enemies:
            if detectar_colision(personaje, enemy, scroll_x):
                colision_enemigo = True
                break
        
        if colision_enemigo:
            objetos.Ventana.fill((163, 73, 164))
            objetos.Ventana.blit(constantes.image_loser, (0, 0))
            finish = True
        
        if detectar_colision(personaje, meta, scroll_x):
            objetos.Ventana.fill((163, 173, 164))
            objetos.Ventana.blit(constantes.image_victory, (0, 0))
            finish = True
        
        # Solo mostrar progreso
        fuente = pg.font.SysFont(None, 36)
        progreso = f"Progreso: {int((personaje.posx / constantes.META_POSX) * 100)}%"
        texto = fuente.render(progreso, True, (255, 255, 255))
        objetos.Ventana.blit(texto, (10, 10))
    
    pg.display.update()

pg.quit()