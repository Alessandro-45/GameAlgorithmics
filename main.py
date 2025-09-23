import pygame as pg
import constantes
import objetos

pg.init()

def detectar_colision(obj1, obj2, scroll_x=0):
    rect1 = pg.Rect(obj1.posx - scroll_x, obj1.posy, obj1.ancho, obj1.alto)
    rect2 = pg.Rect(obj2.posx - scroll_x, obj2.posy, obj2.ancho, obj2.alto)
    return rect1.colliderect(rect2)

# Variables para el scroll
left_bound = constantes.Ancho_ventana/40
right_bound = constantes.Ancho_ventana - 8*left_bound
shift = 0
seccion_actual = 0

# listas de sprites
all_sprites = pg.sprite.Group()
barriers = pg.sprite.Group()
enemies = pg.sprite.Group()

# Crear objetos
personaje = objetos.Personaje(constantes.image_personaje, 
                              constantes.ancho_personaje,
                              constantes.alto_personaje,
                              constantes.pos_ini_player_x, 
                              constantes.pos_ini_player_y, 
                              constantes.velocidad_player)

meta = objetos.GameObject(constantes.image_finish, 
                          constantes.ancho_personaje,
                          constantes.alto_personaje,
                          constantes.META_POSX,
                          constantes.Alto_ventana - 150,
                          0)

color1, color2, color3 = 163, 73, 164

# Crear plataformas
platform1 = objetos.Wall(color1, color2, color3, 200, 500, 300, 30)
platform2 = objetos.Wall(color1, color2, color3, 500, 400, 200, 30)
platform3 = objetos.Wall(color1, color2, color3, 100, 300, 250, 30)
platform4 = objetos.Wall(color1, color2, color3, 1200, 500, 300, 30)
platform5 = objetos.Wall(color1, color2, color3, 1500, 350, 200, 30)
platform6 = objetos.Wall(color1, color2, color3, 1300, 200, 250, 30)
platform7 = objetos.Wall(color1, color2, color3, 2200, 450, 400, 30)
platform8 = objetos.Wall(color1, color2, color3, 2600, 300, 200, 30)
platform9 = objetos.Wall(color1, color2, color3, 2400, 150, 150, 30)
platform10 = objetos.Wall(color1, color2, color3, 3200, 500, 300, 30)
platform11 = objetos.Wall(color1, color2, color3, 3500, 350, 200, 30)

# AGREGAR: Crear lista de walls para las colisiones
walls_list = [platform1, platform2, platform3, platform4, platform5,
              platform6, platform7, platform8, platform9, platform10, platform11]

# Agregar a grupos
all_sprites.add(platform1, platform2, platform3, platform4, platform5,
                platform6, platform7, platform8, platform9, platform10, platform11,
                personaje, meta)
barriers.add(platform1, platform2, platform3, platform4, platform5,
             platform6, platform7, platform8, platform9, platform10, platform11)

# Crear enemigos
enemy1 = objetos.Enemy(constantes.image_enemy, constantes.ancho_personaje,
                      constantes.alto_personaje, 400, 300, constantes.velocidad_enemy, 'left')
enemy2 = objetos.Enemy(constantes.image_enemy, constantes.ancho_personaje,
                      constantes.alto_personaje, 1400, 150, constantes.velocidad_enemy, 'left')
enemy3 = objetos.Enemy(constantes.image_enemy, constantes.ancho_personaje,
                      constantes.alto_personaje, 2500, 100, constantes.velocidad_enemy, 'left')
enemy4 = objetos.Enemy(constantes.image_enemy, constantes.ancho_personaje,
                      constantes.alto_personaje, 3300, 300, constantes.velocidad_enemy, 'left')

enemies.add(enemy1, enemy2, enemy3, enemy4)
all_sprites.add(enemy1, enemy2, enemy3, enemy4)

clock = pg.time.Clock()
finish = False
run = True

while run:
    clock.tick(60)
    
    for eventos in pg.event.get():
        if eventos.type == pg.QUIT:
            run = False
    
    if not finish:
        # CORRECCIÓN: Actualizar personaje con la lista de walls
        personaje.update(walls_list)
        
        # CORRECCIÓN: Actualizar enemigos con la lista de walls
        for enemy in enemies:
            enemy.move(walls_list)
        
        # Actualizar otros sprites (platforms, meta)
        for sprite in all_sprites:
            if sprite not in [personaje] + list(enemies):
                sprite.update()
        
        # Lógica de scroll y colisiones
        if pg.sprite.spritecollide(personaje, enemies, False):
            # CORRECCIÓN: No usar kill(), mejor cambiar finish
            finish = True
        
        # CORRECCIÓN: Lógica de scroll mejorada
        keys = pg.key.get_pressed()
        movimiento_horizontal = 0
        
        if keys[pg.K_LEFT]:
            movimiento_horizontal = -personaje.speed
        if keys[pg.K_RIGHT]:
            movimiento_horizontal = personaje.speed
        
        # Aplicar scroll si el personaje llega a los bordes
        if (personaje.rect.x > right_bound and movimiento_horizontal > 0 or
            personaje.rect.x < left_bound and movimiento_horizontal < 0):
            
            shift -= movimiento_horizontal
            # Limitar shift al tamaño del mundo
            shift = max(0, min(shift, constantes.MUNDO_ANCHO - constantes.Ancho_ventana))
            
            # Mover todos los sprites
            for sprite in all_sprites:
                sprite.rect.x -= movimiento_horizontal

        # Renderizado
        local_shift = shift % constantes.Ancho_ventana
        objetos.Ventana.blit(constantes.background, (local_shift, 0))
        if local_shift != 0:
            objetos.Ventana.blit(constantes.background, (local_shift - constantes.Ancho_ventana, 0))

        # Dibujar sprites
        all_sprites.draw(objetos.Ventana)
        
        # Detectar victoria - CORRECCIÓN: Usar rectángulos directamente
        if personaje.rect.colliderect(meta.rect):
            objetos.Ventana.fill((163, 173, 164))
            objetos.Ventana.blit(constantes.image_victory, (0, 0))
            finish = True

        # Mostrar información - CORRECCIÓN: Calcular sección actual
        seccion_actual = min(int(personaje.posx / constantes.Ancho_ventana), 3)
        fuente = pg.font.SysFont(None, 36)
        info_seccion = f"Sección: {seccion_actual + 1}/4"
        texto_seccion = fuente.render(info_seccion, True, (255, 255, 255))
        objetos.Ventana.blit(texto_seccion, (10, 10))
        
        # CORRECCIÓN: Usar posx en lugar de rect.x para progreso
        progreso_porcentaje = min(int((personaje.posx / constantes.META_POSX) * 100), 100)
        progreso = f"Progreso: {progreso_porcentaje}%"
        texto_progreso = fuente.render(progreso, True, (255, 255, 255))
        objetos.Ventana.blit(texto_progreso, (10, 50))
        
        # Si hay game over, mostrar pantalla de derrota
        if finish and pg.sprite.spritecollide(personaje, enemies, False):
            objetos.Ventana.fill((163, 73, 164))
            objetos.Ventana.blit(constantes.image_loser, (0, 0))
    
    pg.display.update()

pg.quit()