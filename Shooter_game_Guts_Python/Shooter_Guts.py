from pygame import*
from random import randint
import time as timer
window_width = 700
window_height = 800
window = display.set_mode( (window_width, window_height) )
display.set_caption("Pygame window")

clock = time.Clock()
fps = 60

bg = transform.scale(image.load("galaxy.jpg"), (window_width, window_height))
class Character(sprite.Sprite):
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed):
        super().__init__()
        self.filename = filename
        self.size_x = size_x
        self.size_y = size_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.image = transform.scale(image.load(self.filename), (self.size_x, self.size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

UFO_MOVE_Through = 0

class Enemy(Character):
    def update(self):
        global UFO_MOVE_Through
        self.rect.y += self.speed
        if (self.rect.y > 800):
            UFO_MOVE_Through += 1
            self.rect.y = 0
            self.rect.x = randint(0, 600)
            self.speed = randint(1, 4)
        UFO_text = style.render("UFO Through: " + str(UFO_MOVE_Through), 1, (255,255,255))
        window.blit(UFO_text, (10,72))
class Asteroid(Character):
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed_x, speed_y):
        super().__init__(filename, size_x, size_y, pos_x, pos_y, 0)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if (self.rect.y > 800 or self.rect.x < 0 or self.rect.x > 650):
            self.rect.y = 0
            self.rect.x = randint(0, 600)
            self.speed = randint(1, 4)

class Bullet(Character):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Character("rocket.png", 50, 100, 375, 675, 5)

enemy_group = sprite.Group()
for i in range(10):
    enemy = Enemy("ufo.png", 100, 50, randint(5, 600), 0, randint(1, 4))
    enemy_group.add(enemy)
bullet_group = sprite.Group()
enemy1_group = sprite.Group()
for i in range(4):
    As = Asteroid("asteroid.png", 50, 50, randint(5, 600), 0, randint(-3, 3), randint(2, 3))
    enemy1_group.add(As)


game = True
finish = False
fire_time = timer.time()
bullet_count = 10
reload_time = 2
health = 3
font.init()
style = font.SysFont('Arial', 36)
reload_text = style.render("", 1, (255, 255, 255))

while game:
    display.update()
    clock.tick(fps)

    for e in event.get():
        if e.type == QUIT:
            game = False

    if(finish == False):
        window.blit(bg, (0, 0))
        bullet_text = style.render("Bullets: " + str(bullet_count), 1, (255,255,255))
        window.blit(bullet_text, (10,10))
        health_text = style.render("Health: " + str(health), 1, (255,255,255))
        window.blit(health_text, (10,40))
        window.blit(reload_text, (250,370))

        key_list = key.get_pressed()
        if (key_list[K_LEFT] and player.rect.x > 0):
            player.rect.x -= player.speed
        if (key_list[K_RIGHT] and player.rect.x < 650):
            player.rect.x += player.speed
        if (key_list[K_UP] and player.rect.y > 0):
            player.rect.y -= player.speed
        if (key_list[K_DOWN] and player.rect.y < 700):
            player.rect.y += player.speed

        if (bullet_count > 0):
            if (key_list[K_SPACE] and timer.time() - fire_time > 0.2):
                bullet = Bullet("bullet.png", 30, 30, player.rect.x, player.rect.y, 5)
                bullet_group.add(bullet)
                bullet_count -= 1
                fire_time = timer.time()
        else:
            reload_text = style.render("RELOADING..." , 1, (255,255,255))
            if (timer.time() - fire_time > reload_time):
                reload_text = style.render("" , 1, (255,255,255))
                print("RELOADED")  
                bullet_count = 10    

        collide_list = sprite.spritecollide(player, enemy_group, True)
        if len(collide_list) > 0:
            enemy = Enemy("ufo.png", 100, 50, randint(5, 600), 0, randint(1, 4))
            enemy_group.add(enemy)
            health -= 1
            health_text = style.render("Health: " + str(health), 1, (255,255,255))
            window.blit(health_text, (10,40))
            if health == 0:
                lose_text = style.render("YOU LOSE : Health = " + str(health), 1, (255,255,255))
                window.blit(lose_text, (220,350))
                print("YOU LOSE")
                finish = True
        collide1_list = sprite.spritecollide(player, enemy1_group, True)
        if len(collide1_list) > 0:
            As = Asteroid("asteroid.png", 50, 50, randint(5, 600), 0, randint(-3, 3), randint(2, 3))
            enemy1_group.add(As)
            health -= 1
            health_text = style.render("Health: " + str(health), 1, (255,255,255))
            window.blit(health_text, (10,40))
            if health == 0:
                lose_text = style.render("YOU LOSE : Health = " + str(health), 1, (255,255,255))
                window.blit(lose_text, (220,350))
                print("YOU LOSE")
                finish = True
        if (UFO_MOVE_Through == 10):
            print("YOU LOSE")
            finish = True

        sprites_list = sprite.groupcollide(enemy_group, bullet_group, True, True)
        sprites_list = sprite.groupcollide(enemy1_group, bullet_group, True, True)
        for s in sprites_list:
            enemy = Enemy("ufo.png", 100, 50, randint(5, 600), 0, randint(1, 4))
            enemy_group.add(enemy)
        for s in sprites_list:
            As = Asteroid("asteroid.png", 50, 50, randint(5, 600), 0, randint(-3, 3), randint(2, 3))
            enemy1_group.add(As)

        player.draw()
        bullet_group.update()
        bullet_group.draw(window)
        enemy_group.update()
        enemy_group.draw(window)
        enemy1_group.update()
        enemy1_group.draw(window)