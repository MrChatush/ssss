
from pygame import *
from random import *
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)
       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load("galaxy.jpg"),(700, 500))
run =True
FPS=60

score=0
lost=0

clock=time.Clock()
monsters=sprite.Group()
bullets=sprite.Group()

mixer.init()
mixer.music.load('space.ogg')
kick=mixer.Sound('fire.ogg')
mixer.music.play()

 
        
            
            


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed() 
        if keys[K_a] and self.rect.x>20:
            self.rect.x = self.rect.x - self.speed
        if keys[K_d] and self.rect.x<650:
            self.rect.x = self.rect.x + self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)   
        bullets.add(bullet)
ship=Player('rocket.png', 350, 400, 80, 50, 8)

class Enemy(GameSprite):
    def update(self):
        if self.rect.y <470:
            self.rect.y=self.rect.y+self.speed
        elif self.rect.y>=470:
            self.rect.x=randint(70,670)
            self.rect.y=30
            global lost
            lost = lost + 1

finish=False

font.init()
font=font.SysFont('Arial', 40)
lose=font.render('YOU Lose',True, (255,215,0))
win=font.render('YOU WIN!',True, (255,215,0))

for i in range(1, 6):
    enemy_1 = Enemy('ufo.png', randint(80, 420), 40, 80, 50, randint(1, 5))
    monsters.add(enemy_1)

while run:
   #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
       #событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #fire_sound.play()
                ship.fire()
    if not finish:
       #обновляем фон
        window.blit(background,(0,0))
 
       #пишем текст на экране
        text = font.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        collides = sprite.groupcollide(
            monsters, bullets, True, True
            )
 
        text_lose = font.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
 
       #производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
 
       #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
 
        display.update()
