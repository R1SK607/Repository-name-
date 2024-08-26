from random import *
from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_weight, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_weight, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < mw_w - 85:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
            self.rect.y -= self.speed
            if self.rect.y < 5:
                self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

win_height = 500
win_width = 700
lost = 0 #Пропущено противников

mw_w = 700
mw_h = 500
mw = display.set_mode((mw_w, mw_h))
display.set_caption('United Space Shooter from Russia(USSR)')
bd = transform.scale(image.load('galaxy.jpg'), (mw_w, mw_h)) #stupid VSCode
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_in_the_hole = mixer.Sound('fire.ogg')
player = Player('rocket.png', 120, 400, 80, 100, 5)
clock = time.Clock()

font.init()
font1 = font.SysFont('Areal', 35)
font2 = font.SysFont('Areal', 100)

astros = sprite.Group()
for i in range(3):
    astro = Asteroid('asteroid.png', randint(5, 625), -80, 80, 50, 1)
    astros.add(astro)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(5, 625), -80, 80, 50, 1)
    monsters.add(monster)

bullets = sprite.Group()
run = True
finish = False
score = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key ==K_SPACE:
                fire_in_the_hole.play()
                player.fire()

    if finish != True:
        sprite_lt = sprite.spritecollide(player, monsters, False)
        sprite_lts = sprite.spritecollide(player, astros, False)
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)

        mw.blit(bd, (0, 0))

        llose = font1.render('Подбито:' + str(score), 1, (255,255,255))
        mw.blit(llose, (10, 20))
        wwwin = font1.render('Пропущено:' + str(lost), 1, (255,255,255))
        mw.blit(wwwin, (10, 50))

        player.update()
        monsters.update()
        astros.update()
        bullets.update()
        player.reset()
        monsters.draw(mw)
        astros.draw(mw)
        bullets.draw(mw)
    
        if sprite_lt or sprite_lts or lost >= 3:
            lose = font2.render('YOU LOSE, MAN!', True, (0, 0, 255))
            mw.blit(lose, (100, 100))
            finish = True
        
        if sprite_list:
            score += 1
            monster = Enemy('ufo.png', randint(5, 625), -80, 80, 50, 1)
            monsters.add(monster)
        
        if score >= 10:
            win = font2.render('YOU WIN, BRO!', True, (0, 0, 255))
            mw.blit(win, (100, 100))
            finish = True
        display.update()
    clock.tick(60)