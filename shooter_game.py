#Создай собственный Шутер!

from random import randint
from pygame import *
init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(image_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(0, win_width - 65)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500

font.init()
font1 = font.SysFont('Arial', 36)

score = 0
lost = 0

win_score = 10
lose_score = 5

window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

display.set_caption('pygame window')

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

player = Player('rocket.png', 350, win_height - 100, 80, 100, 10)

image_bullet = 'bullet.png'

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

finish = False
run = True
clock = time.Clock()
FPS = 50

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if not finish:
        window.blit(background,(0,0))

        player.update()
        monsters.update()
        bullets.update()

        text = font1.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        work = sprite.groupcollide(bullets, monsters, True, True)

        for e in work:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if score >= win_score:
            win_text = font1.render('Вы выйграли!', True,  (255, 255, 255))
            window.blit(win_text, (200, 200))
            finish = True
        
        if lost >= lose_score:
            lose_text = font1.render('Вы проиграли!', True, (255, 255, 255))
            window.blit(lose_text, (200, 200))
            finish = True

        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        display.update()
    clock.tick(FPS)