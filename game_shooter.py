import pygame, os, random as rd
 
#Constantes
ancho = 800
alto = 600
negro = (0, 0, 0)
blanco = (255, 255, 255)
gris_oscuro = (51, 47, 44)
gris = (205, 205, 205)
verde = (0, 255, 0)
naranja = (255, 165, 0) 
rojo = (255, 0, 0)
rosa = (231,145,191)
mejor_puntaje = 0

try:
    with open("mejor_puntaje.txt", "r") as file:
        mejor_puntaje = int(file.read())
except FileNotFoundError:
    pass

pygame.init()
pygame.mixer.init()
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Game Kirby Shooter")
icon = pygame.image.load("elementos/kirby_icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

def Text(surface, text, size, x, y):
    font = pygame.font.Font("elementos/font/ZeroCool.ttf", size)
    text_surface = font.render(text, True, blanco)
    text_rect = text_surface.get_rect(  )
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def TextEnter(surface, text, size, x, y):
    font = pygame.font.Font("elementos/font/ZeroCool.ttf", size)
    text_surface = font.render(text, True, negro)
    text_rect = text_surface.get_rect(  )
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def Indication(surface, text, size, x, y):
    font = pygame.font.Font("elementos/font/ZeroCool.ttf", size)
    text_surface = font.render(text, True, gris)
    text_rect = text_surface.get_rect(  )
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def barra(surface, x, y, porcentaje):
    bar_ancho = 100
    bar_alto = 10
    fill = (porcentaje / 100) * bar_ancho
    life = os.path.join("elementos","heart_life.png")
    borde = pygame.Rect(x + 25, y + 6, bar_ancho, bar_alto)
    fill = pygame.Rect(x + 25, y + 6, fill, bar_alto)
    life = pygame.image.load(life)
    surface.blit(life, (x, y))
    if porcentaje > 59:
        pygame.draw.rect(surface, verde, fill)
    if porcentaje < 60 and porcentaje > 20:
        pygame.draw.rect(surface, naranja, fill)
    if porcentaje <= 20:
        pygame.draw.rect(surface, rojo, fill)
    pygame.draw.rect(surface, blanco, borde, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("elementos/kirby_arma.png").convert()
        self.image.set_colorkey(blanco)
        self.rect = self.image.get_rect()
        self.rect.centerx = ancho // 2
        self.rect.bottom = alto - 10
        self.speed_x = 0
        self.speed_y = 0
        self.shield = 100

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_w] or keystate[pygame.K_UP]:
            self.speed_y = -5
        if keystate[pygame.K_s] or keystate[pygame.K_DOWN]:
            self.speed_y = 5
        if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > ancho:
            self.rect.right = ancho
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > alto:
            self.rect.bottom = alto
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):  
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = rd.choice(enemy_images)
        self.image.set_colorkey(blanco)
        self.rect = self.image.get_rect()
        self.rect.x = rd.randrange(ancho - self.rect.width)
        self.rect.y = rd.randrange(-140, -100)
        self.speedy = rd.randrange(1, 10)
        self.speedx = rd.randrange(-5, 5)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > alto + 10 or self.rect.left < -40 or self.rect.right > ancho + 40:
            self.rect.x = rd.randrange(ancho - self.rect.width)
            self.rect.y = rd.randrange(-100, -40)
            self.speedy = rd.randrange(1, 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("elementos/laser1.png").convert()
        self.image.set_colorkey(negro) 
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = e_animation[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 #velocidad de explosión
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len (e_animation):
                self.kill()
            else:
                center = self.rect.center
                self.image = e_animation[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    pantalla.blit(background, [0, 0])
    Text(pantalla, "KIRBY SHOOTER", 65, ancho // 2, alto // 4)
    Text(pantalla, "SPACE for shoot", 27, ancho // 2, (alto // 2) - 16)
    Text(pantalla,"Left, Up, Down and Rigth or", 27, ancho // 2, (alto // 2) + 16)
    Text(pantalla,"A, W, S and D for move", 27, ancho // 2, (alto // 2) + 48)
    TextEnter(pantalla, "Press ENTER", 20, ancho // 2, alto * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:  # Espera a que se presione la tecla "Enter"
                    waiting = False

def pantalla_game_over(surface, text, score, enemies_killed, best_score, size, x, y):
    pantalla.blit(background, [0, 0])
    font_title = pygame.font.Font("elementos/font/ZeroCool.ttf", size)
    font_details = pygame.font.Font("elementos/font/ZeroCool.ttf", size - 28)
    font_details2 = pygame.font.Font("elementos/font/ZeroCool.ttf", size - 18)
    font_details3 = pygame.font.Font("elementos/font/ZeroCool.ttf", size - 45)   # Tamaño de letra para detalles
    text_surface = font_title.render(text, True, rojo)  # Puedes ajustar el color como desees
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x // 2, y // 4 - 40)
    surface.blit(text_surface, text_rect)
    text_surface2 = font_details3.render("ENTER to Menu", True, negro)
    text_rect2 = text_surface2.get_rect()
    text_rect2.midtop = (x // 2, y // 2 + 166)
    surface.blit(text_surface2, text_rect2)

    score_text = f"Your score is: {score}"
    enemies_text = f"Enemies your killed: {enemies_killed}"
    best_score_text = f"BEST SCORE: {best_score}"
    score_surface = font_details.render(score_text, True, gris)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (x // 2 , y // 2 - 56)
    surface.blit(score_surface, score_rect)
    enemies_surface = font_details.render(enemies_text, True, gris)
    enemies_rect = enemies_surface.get_rect()
    enemies_rect.midtop = (x // 2, y //2 - 16)
    surface.blit(enemies_surface, enemies_rect)
    best_score_surface = font_details2.render(best_score_text, True, verde)
    best_score_rect = best_score_surface.get_rect()
    best_score_rect.midtop = (x // 2, y // 2 + 56)
    surface.blit(best_score_surface, best_score_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:  # Espera a que se presione la tecla "Enter"
                    waiting = False

#Imagenes de los enemigos
enemy_images = []
enemy_list = ["elementos/scarfy_enemy.png", "elementos/gorgo_enemy.png", "elementos/waddle_dee_enemy.png", "elementos/gip_enemy.png","elementos/bronto_enemy.png"]
for img in enemy_list:
    enemy_images.append(pygame.image.load(img).convert())
    

#Animación de la explosión
e_animation = []
for i in range(9):
    file = "elementos/regularExplosion0{}.png".format(i)
    image = pygame.image.load(file).convert()
    image.set_colorkey(negro)
    image_scale = pygame.transform.scale(image, (70, 70))
    e_animation.append(image_scale)

#Fondo
background = pygame.image.load("elementos/background.png").convert()

#Sonidos
laser_sound = pygame.mixer.Sound("elementos/music/laser5.ogg")
laser_sound.set_volume(0.4)
explosion_sound = pygame.mixer.Sound("elementos/music/explosion.wav")
explosion_sound.set_volume(0.2)
kirby_beaten = pygame.mixer.Sound("elementos/music/Kirby_angry_voice.mp3")
kirby_dead = pygame.mixer.Sound("elementos/music/Kirby_dead_voice.mp3")

pygame.mixer.music.load("elementos/music/music.ogg")
pygame.mixer.music.set_volume(0.3)

pygame.mixer.music.play(loops = -1)

#Game over
game_over = True
running = True
score = 0
while running:
    if game_over:
        
        show_go_screen()

        game_over = False
        all_sprites = pygame.sprite.Group()
        enemy_list = pygame.sprite.Group()  
        bullets = pygame.sprite.Group()

        #Generación de enemigos
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemy_list.add(enemy)
        score = 0

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    all_sprites.update()
   
   #Colision enemigo/laser
    hits = pygame.sprite.groupcollide(enemy_list, bullets, True, True)
    for hit in hits:
        score += 15 
        explosion_sound.play()
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        enemy = Enemy()
        all_sprites.add(enemy)
        enemy_list.add(enemy)

    #Colisión kirby/enemigo
    hits = pygame.sprite.spritecollide(player, enemy_list, True)
    for hit in  hits:
        player.shield -= 8
        if player.shield > 0:
            kirby_beaten.play()
        enemy = Enemy()
        all_sprites.add(enemy)
        enemy_list.add(enemy)

        if player.shield <= 0:
            game_over = True
            kirby_dead.play()
            # Puedes reemplazar estos valores con tus propias variables de puntuación y enemigos derrotados
            pantalla_game_over(pantalla, "GAME OVER", score, score // 15, mejor_puntaje, 65, ancho, alto)   
    # Una vez que se sale del bucle principal (fin del juego), mostrar la pantalla de fin de juego
            pantalla.fill(negro)  # Limpia la pantalla
            pygame.display.flip()  # Actualiza la pantalla
            
    if score > mejor_puntaje:
        mejor_puntaje = score
        def puntaje_mas_alto(nuevo_puntaje):
            with open("mejor_puntaje.txt", "w") as file:
                file.write(str(nuevo_puntaje))
        puntaje_mas_alto(mejor_puntaje)
      
    pantalla.blit(background, [0, 0])
    all_sprites.draw(pantalla)

    #Marcador
    Text(pantalla, str(score), 25, ancho // 2, 10)
    Indication(pantalla, "Move to A, W, S and D", 15, ancho - 150, alto - 80)
    Indication(pantalla, "or Left, Up, Down and Rigth", 15, ancho - 150, alto - 60)
    Indication(pantalla, "Shoot to Space", 15, ancho - 150, alto - 40)

    #Vida
    barra(pantalla, 5, 5, player.shield)

    pygame.display.flip()

pygame.quit()