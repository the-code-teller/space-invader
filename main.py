import pygame
import random

class GameObject:
    
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Player(GameObject):

    def __init__(self) -> None:
        self.image = pygame.image.load('player.png')
        self.x = 185
        self.y = 480
        self.speed_x = 0

    def set_position(self):
        self.x += self.speed_x

        # restrict movement at boundries
        if self.x <= 0:
            self.x = 0
        elif self.x >= 336:
            self.x = 336

    def move_right(self):
        self.speed_x = 0.5

    def move_left(self):
        self.speed_x = -0.5

    def stop(self):
        self.speed_x = 0

class Enemy(GameObject):
    def __init__(self) -> None:
        self.image = pygame.image.load('enemy.png')
        self.x = random.randint(0, 337)
        self.y = random.randint(50, 150)
        self.speed_x = 0.5
        self.speed_y = 50

    def set_position(self):
        self.x += self.speed_x

        # change Direction at boundries
        if self.x <= 0:
            self.move_right()
            self.y += self.speed_y
        elif self.x >= 336:
            self.move_left()
            self.y += self.speed_y

    def move_right(self):
        self.speed_x = 0.5

    def move_left(self):
        self.speed_x = -0.5

    def respawn(self):
        self.x = random.randint(0, 373)
        self.y = random.randint(50, 150)

class Bullet(GameObject):

    def __init__(self) -> None:
        self.image = pygame.image.load('bullet.png')
        self.x = 386.5
        self.y = 490
        self.speed_y = -2
        self.state = 'ready'

    def set_position(self, x, y):
        if self.state == 'ready':
            self.x = x + 16.5
            self.y = y + 10
        elif self.state == 'fired':
            self.y += self.speed_y
            if self.y <= 0:
                self.state = 'ready'
            
    def fire(self):
        self.state = 'fired'

class GameTexts:

    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 32)

    def show(self):
        score = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(score, (self.x, self.y))

class Score(GameTexts):

    def __init__(self):
        super().__init__()
        self.value = 0
        self.x = 10
        self.y = 10
        self.text = 'Score : 0'

    def increase(self):
        self.value += 1
        self.text = 'Score :' + str(self.value)

class GameOver(GameTexts):

    def __init__(self):
        super().__init__()
        self.x = 200
        self.y = 250
        self.text = "GAME OVER"

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((400, 600))

# Title
pygame.display.set_caption("Space Invaders")

# Icon
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('bg.jpg')

if __name__=='__main__':

    player = Player()
    enemies = []
    for i in range(5):
        enemies.append(Enemy())
    bullet = Bullet()
    score = Score()

    #Game Loop
    running = True
    while running:

        # Background image
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
            
            # KeyDown Event Handling for Player Movement
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_SPACE:
                    bullet.fire()

            # KeyUp Event Handling for Player Movement
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.stop()

        # Setting Positions
        player.set_position()
        for enemy in enemies:
            enemy.set_position()
        bullet.set_position(player.x, player.y)

        # Display Characters
        player.draw()
        bullet.draw()
        for enemy in enemies:
            enemy.draw()
        score.show()

        # Enemy Kill
        for enemy in enemies:
            if bullet.x >= enemy.x and bullet.x <= enemy.x+32 and bullet.y >= enemy.y and bullet.y <= enemy.y+32:
                enemy.respawn()          
                score.increase()  

        # Player-Enemy Collision
        for enemy in enemies:
            if enemy.x >= player.x-62 and enemy.x <= player.x+62 and enemy.y >= player.y-62 and enemy.y <= enemy.y+62:
                running = False

        # Update all changes of while loop
        pygame.display.update()
