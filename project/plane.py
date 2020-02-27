import os
import random
import pygame
import sys


clock = pygame.time.Clock()
pygame.init()
size = 800, 400
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color("white"))
FPS = 60
screen_rect = (0, 0, 800, 400)
GRAVITY = 0.25
score = 0
win = False
#fons
fons = ['fon1.png', 'fon2.png', 'fon3.png', 'fon4.png', 'fon5.png']
random.shuffle(fons)

def start_screen2():
    intro_text = ["------SCORE------",
                  str(score),
                  "PRESS ANY KEY"]
 
    fon = pygame.transform.scale(load_image('fon.png'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 130
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('GREEN'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 315
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинало игры
        pygame.display.flip()
        clock.tick(FPS)
        
def start_screen():
    intro_text = ["----------CONTROLS----------",
                  "     /\,<,>,\/ - MOVEMENT",
                  "     SPACEBAR - ATTACK",
                  "PRESS ANY KEY TO START"]
 
    fon = pygame.transform.scale(load_image('fon.png'), (800, 400))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 270
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинало игры
        pygame.display.flip()
        clock.tick(FPS)
        
def terminate():
    pygame.quit()
    sys.exit()
    
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image 

bullet_image = pygame.transform.scale(load_image("bullet.png", -1), (50, 10))
ship_image = pygame.transform.scale(load_image("spaceship.png", -1), (50, 50))
boom_image = pygame.transform.scale(load_image("boom.png", -1), (100, 100))
blackhole_image = pygame.transform.scale(load_image("blackhole.png", -1), (200, 200))
enemy_ship_image = pygame.transform.scale(load_image("enemyship.png", -1), (50, 50))
gameover_image = pygame.transform.scale(load_image(str("gameover.png")), (800, 400))
win_image = pygame.transform.scale(load_image(str("win.jpg")), (800, 400))

bullet_sound = pygame.mixer.Sound('bullet.wav')
boom_sound = pygame.mixer.Sound('boom.wav')
blackhole_sound = pygame.mixer.Sound('blackhole.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_sprites)
        self.image = ship_image
        self.image_boom = boom_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 175
        
    def moveto(self, axis):
        if axis == '+x':
            if self.rect[0] != 750:
                self.rect = self.rect.move(5, 0)               
        elif axis == '-x':
            if self.rect[0] != 0:
                self.rect = self.rect.move(-5, 0)       
        elif axis == '+y':
            if self.rect[1] != 350:
                self.rect = self.rect.move(0, 5)
        elif axis == '-y':
            if self.rect[1] != 0:
                self.rect = self.rect.move(0, -5)
                
    def boom(self):
        self.image = self.image_boom
        

         
class Particle(pygame.sprite.Sprite):
    fire = [boom_image]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))
 
    def __init__(self, pos, dx, dy):
        super().__init__(particle_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
 
        self.gravity = GRAVITY
 
    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()
                    
                    
class blackhole(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = blackhole_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()    
        self.rect.x = 1000
        self.rect.y = 100
    def update(self):
        if self.rect.x > 575:
            self.rect = self.rect.move(-20, 0) 
            
            
class blackholefake(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = blackhole_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()    
        self.rect.x = 25
        self.rect.y = 100
        
    def update(self):
        self.rect = self.rect.move(-10, 0)     
    
    
class enemy_ship(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = enemy_ship_image
        self.image_boom = boom_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(800, 1600)
        self.rect.y = random.randrange(0, 350)
        
    def update(self):
        self.rect = self.rect.move(-3, 0) 
        
    def boom(self):
        self.image = self.image_boom  
        
        
class boss_ship(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image("bossship.png", -1), (200, 400))
        self.image_boom = boom_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 0
        self.hp = 20
        
    def boom(self):
        create()
        explosion_sound.play()
        
class endscreen():
    def __init__(self):
        self.image = gameover_image  
        self.coord_x = -800
        self.coord_y = -400
        self.coords = (self.coord_x, self.coord_y)

    def update(self):
        self.coord_x += 8
        self.coord_y += 4      
        self.coords = (self.coord_x, self.coord_y)
   
        
class bullet(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = bullet_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = spaceship.rect[0]
        self.rect.y = spaceship.rect[1] + 20
        
    def update(self):
        self.rect = self.rect.move(15, 0) 
        
    def boom(self):
        self.kill()


def create_particles(position):
    particle_count = 10
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers)) 
        
end = endscreen()
particle_sprites = pygame.sprite.Group()
blackhole_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()           
env_sprites = pygame.sprite.Group()
projectile_sprites = pygame.sprite.Group()
boss_sprites = pygame.sprite.Group()
spawn = None
blackhole_sprites.empty()
player_sprites.empty()           
env_sprites.empty()
projectile_sprites.empty()
particle_sprites.empty()
boss_sprites.empty()  
boss = False
for i in range(20):
    enemy_ship(env_sprites)
background = pygame.transform.scale(load_image(fons.pop()), (800, 400))
spaceship = Spaceship()
player_sprites.add(spaceship)  

running = True
playing = True

start_screen()
while running:
    if playing:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet(projectile_sprites)
                    bullet_sound.play()           
        if keys[pygame.K_UP]:
            spaceship.moveto('-y')
        if keys[pygame.K_DOWN]:
            spaceship.moveto('+y')
        if keys[pygame.K_LEFT]:
            spaceship.moveto('-x')
        if keys[pygame.K_RIGHT]:
            spaceship.moveto('+x')
        if len(env_sprites) != 0:
            gateway = False            
            if boss is False:
                for enemy_ships in env_sprites:
                    if pygame.sprite.collide_mask(spaceship, enemy_ships):
                        playing = False
                        enemy_ships.boom()
                        spaceship.boom()
                        boom_sound.play()
                    
                    else:
                        for bullets in projectile_sprites:
                            if pygame.sprite.collide_mask(bullets, enemy_ships):
                                score += 1 
                                enemy_ships.kill()
                                bullets.kill()

                
            else:
                if pygame.sprite.collide_mask(spaceship, boss):
                        playing = False
                        spaceship.boom()
                        boom_sound.play()                
                for enemy_ships in env_sprites:
                    if pygame.sprite.collide_mask(spaceship, enemy_ships):
                        playing = False
                        enemy_ships.boom()
                        spaceship.boom()
                        boom_sound.play()
                    else:
                        for bullets in projectile_sprites:
                            if pygame.sprite.collide_mask(bullets, enemy_ships):
                                score += 1
                                enemy_ships.kill()
                                bullets.kill()
                for bullets in projectile_sprites:
                    if pygame.sprite.collide_mask(bullets, boss):
                        bullets.kill()
                        boom_sound.play()
                        boss.hp -= 1
                        print(boss.hp)
                    if boss.hp == 0:
                        win is True

                    
            for enemy_ships in env_sprites:
                enemy_ships.update()
            for bullets in projectile_sprites:
                bullets.update()
            if spawn != None:
                spawn.update()
            for enemy_ships in env_sprites:
                if enemy_ships.rect[0] < -50:
                    enemy_ships.kill()
            for bullets in projectile_sprites:
                if bullets.rect[0] > 780:
                    bullets.kill()

        elif len(env_sprites) == 0 and boss is False:
            if gateway is False:
                gateway = blackhole(blackhole_sprites)
            if gateway is not False:
                if pygame.sprite.collide_mask(bullets, gateway):
                    bullets.kill()
            if pygame.sprite.collide_mask(spaceship, gateway):
                if len(fons) == 0:
                    blackhole_sprites.empty()
                    player_sprites.empty()           
                    env_sprites.empty()
                    projectile_sprites.empty()
                    particle_sprites.empty()
                    boss_sprites.empty()
                    spawn = blackholefake(blackhole_sprites)
                    boss = boss_ship(boss_sprites)
                    for i in range(40):
                        enemy_ship(env_sprites)                    
                    background = pygame.transform.scale(load_image('bossfon.png'), (800, 400)) 
                    spaceship = Spaceship()
                    player_sprites.add(spaceship)
                    blackhole_sound.play()
                    
                else:
                    blackhole_sprites.empty()
                    player_sprites.empty()           
                    env_sprites.empty()
                    projectile_sprites.empty()
                    particle_sprites.empty()
                    boss_sprites.empty()                    
                    spawn = blackholefake(blackhole_sprites)                
                    for i in range(20):
                        enemy_ship(env_sprites)
                    background = pygame.transform.scale(load_image(fons.pop()), (800, 400)) 
                    spaceship = Spaceship()
                    player_sprites.add(spaceship)
                    blackhole_sound.play()
            else:
                gateway.update()
                for bullets in projectile_sprites:
                    bullets.update()
        elif len(env_sprites) == 0:
            if pygame.sprite.collide_mask(spaceship, boss):
                    playing = False
                    spaceship.boom()
                    boom_sound.play()             
            for bullets in projectile_sprites:
                if pygame.sprite.collide_mask(bullets, boss):
                    bullets.kill()
                    boom_sound.play()
                    boss.hp -= 1
                    print(boss.hp)
                    if boss.hp == 0:
                        score += 100
                        win is True
                        playing = False

            for bullets in projectile_sprites:
                bullets.update()
            for bullets in projectile_sprites:
                if bullets.rect[0] > 780:
                    bullets.kill()
                    
        screen.blit(background, (0, 0))
        blackhole_sprites.draw(screen)
        env_sprites.draw(screen)
        projectile_sprites.draw(screen)
        boss_sprites.draw(screen)
        particle_sprites.draw(screen)
        player_sprites.draw(screen)       
        pygame.display.flip()
        clock.tick(FPS)
                
    if playing is False:
        if win is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False        
            screen.blit(background, (0, 0))

            blackhole_sprites.draw(screen)
            env_sprites.draw(screen)
            projectile_sprites.draw(screen)
            boss_sprites.draw(screen)
            particle_sprites.draw(screen)
            particle_sprites.update()
            player_sprites.draw(screen)
            if win is True:
                screen.blit(win_image, end.coords)
            else:
                screen.blit(gameover_image, end.coords)
            
            if end.coord_x < 0:
                end.update()
            if end.coord_x >= 0:
                running = False
                playing = False            
            pygame.display.flip()
            clock.tick(FPS)                
        else:     
            screen.blit(background, (0, 0))
            blackhole_sprites.draw(screen)
            env_sprites.draw(screen)
            projectile_sprites.draw(screen)
            boss_sprites.draw(screen)
            particle_sprites.draw(screen)
            player_sprites.draw(screen)
            if win:
                screen.blit(win_image, end.coords)
            else:
                screen.blit(gameover_image, end.coords)
            
            if end.coord_x < 0:
                end.update()
            if end.coord_x >= 0:
                running = False
                playing = False
            pygame.display.flip()
            clock.tick(FPS)
start_screen2()
pygame.quit()