# Example file showing a circle moving on screen
import random
from sys import exit
import pygame
from pygame.sprite import Group

from pygame import Color
import keyboard

pygame.init()
# importing the images
keys = pygame.key.get_pressed()
wallpaper = pygame.image.load('images/background.png')
pilot = pygame.image.load('images/helicopter.png')
bird = pygame.image.load('images/bird.png')
bird1 = pygame.image.load('images/bird1.png')
stander_size = (bird.get_width()/5,bird.get_height()/5)
helicopter_size = (pilot.get_width()/4,pilot.get_height()/4)
pilot = pygame.transform.scale(pilot,helicopter_size)
bird = pygame.transform.scale(bird,stander_size)
bird1 = pygame.transform.scale(bird1,stander_size)
bull = pygame.image.load('images/bullet.png')
heart = pygame.image.load('images/heart.png')
heart = pygame.transform.scale(heart,(heart.get_width()/15,heart.get_height()/15))
bull = pygame.transform.scale(bull,(heart.get_width()/2,heart.get_height()/2))
def set_wallpaper(wallpaper):
    screen.fill("black")
    screen.blit(wallpaper,(0,0))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bull
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.score = 0
    def update(self):
        self.rect.x += 7
        if self.rect.x > screen.get_width():
            self.kill()  # Remove the bullet when it goes off-screen



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pilot  # Set the image to the loaded player image
        self.health = 3
        self.rect = self.image.get_rect()
        self.rect.center = (50,screen.get_height()//2)
        self.Alive = 1
        self.score = 0
        self.bullets = Group() #storing bullets
        self.last_shoot = 0


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5
        self.rect.y = max(0, min(self.rect.y, screen.get_height() - 40))
        collisions = pygame.sprite.spritecollide(self, birds, False)
        if collisions:
            self.health -= 1
            if self.health <= 0:
                # Handle game over here
                self.Alive = 0
            else:
                # Reset the player's position after a collision
                for bird in collisions:
                    bird.reset_position()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shoot >= 500:
                self.last_shoot = current_time
                aim = Bullet(self.rect.right, self.rect.centery)
                self.bullets.add(aim)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pixels = 1
        self.count = 0
        self.image = bird
        self.rect = bird.get_rect()
        self.health = 1
        self.rect.x = random.randint(screen.get_width()//2,screen.get_width()*3)
        self.rect.y = random.randint(0, screen.get_height() - 10)

    def reset_position(self):
        self.rect.x = random.randint(screen.get_width(), screen.get_width() * 2)
        self.rect.y = random.randint(0, screen.get_height() - 10)

    def update(self):
        self.rect.x -= 3
        if self.rect.x <= 0:
            self.rect.x = random.randint(screen.get_width(),screen.get_width()*2)
            self.rect.y = random.randint(0, screen.get_height() - self.image.get_height() - 10)
        self.count += 1
        if self.pixels:
            self.image = bird1
        else:
            self.image = bird
        if(self.count % 8 == 0):
            self.pixels = 1 - self.pixels
        collisions_bird = pygame.sprite.spritecollide(self, player.bullets, True)  # if bullet collisions bird
        if collisions_bird :
            for i in collisions_bird:
                if i.rect.x < screen.get_width():
                    player.score += 1
                    self.reset_position()


        # pygame setup

pygame.display.set_caption('Flappy bird')

pygame.mixer.music.load('music/ncs.mp3')

# Play the current song
pygame.mixer.music.play()

screen = pygame.display.set_mode((900, 500))
clock = pygame.time.Clock()

# remove the mouse shown in the game
pygame.mouse.set_visible(0)


pixel_font = pygame.font.Font('Fonts/Pixeltype.ttf',40)
debug_font = pygame.font.Font('Fonts/DebugFreeTrial-MVdYB.otf',80)


# importing beginning texts
orange = (224,170,47)
text_intro = pixel_font.render('Press Space to start',False,'White')
text_title = debug_font.render('Flappy Bird',False,orange)
text_title_border = debug_font.render('Flappy Bird',False,'White')
border = 2

# initialize
set_wallpaper(wallpaper)
screen.blit(text_intro, (580, 75))
for x_offset in range(-border, border + 1):
    for y_offset in range(-border, border + 1):
        screen.blit(text_title_border, (180 + x_offset, 125 + y_offset))

screen.blit(text_title, (180, 125))

# flip() the display to put your work on screen
pygame.display.flip()

enter_pressed = 0
# alive = 1
charcters = pygame.sprite.Group()
birds = pygame.sprite.Group()
player = Player()
charcters.add(player)

for _ in range(8):
    bird_sample = Bird()
    charcters.add(bird_sample)
    birds.add(bird_sample)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # pygame.QUIT event means the user clicked X to close your window
            pygame.quit()
            exit()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and enter_pressed == 0:
        enter_pressed = 1
        set_wallpaper(wallpaper)

    if(enter_pressed):
        set_wallpaper(wallpaper)
        charcters.draw(screen)
        player.bullets.draw(screen)
        charcters.update()
        player.bullets.update()

        if player.Alive == 0:
            set_wallpaper(wallpaper)
            screen.blit(text_intro, (580, 75))
            for x_offset in range(-border, border + 1):
                for y_offset in range(-border, border + 1):
                    screen.blit(text_title_border, (180 + x_offset, 125 + y_offset))
            charcters = pygame.sprite.Group()
            birds = pygame.sprite.Group()
            player = Player()
            charcters.add(player)

            for _ in range(8):
                bird_sample = Bird()
                charcters.add(bird_sample)
                birds.add(bird_sample)

            screen.blit(text_title, (180, 125))
            enter_pressed = 0
    score_text = pixel_font.render(f"Score: {player.score}", False, "White")
    screen.blit(score_text, (10, 10))
    for i in range(player.health):
        screen.blit(heart, (760 + i*35, 10))
    pygame.display.flip()
    clock.tick(60)
    # limits FPS to 60
