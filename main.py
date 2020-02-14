import pygame
import random
import math
import time

screenWidth = 1280
screenHeight = 720

# INITIALIZE
pygame.init()
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Apocalypse Survivor")
clock = pygame.time.Clock()

soldierRight = pygame.image.load('soldierR.png')
soldierLeft = pygame.transform.rotate(soldierRight, 180)
soldierUp = pygame.transform.rotate(soldierRight, 90)
soldierDown = pygame.transform.rotate(soldierRight, 270)
runRight = [pygame.image.load('run2.png'),
            pygame.image.load('run1.png'),
            pygame.image.load('run2.png'),
            pygame.image.load('run3.png'),
            pygame.image.load('run4.png'),
            pygame.image.load('run3.png')]
runLeft = [pygame.transform.rotate(runRight[0], 180),
           pygame.transform.rotate(runRight[1], 180),
           pygame.transform.rotate(runRight[2], 180),
           pygame.transform.rotate(runRight[3], 180),
           pygame.transform.rotate(runRight[4], 180),
           pygame.transform.rotate(runRight[5], 180)]
runUp = [pygame.transform.rotate(runRight[0], 90),
         pygame.transform.rotate(runRight[1], 90),
         pygame.transform.rotate(runRight[2], 90),
         pygame.transform.rotate(runRight[3], 90),
         pygame.transform.rotate(runRight[4], 90),
         pygame.transform.rotate(runRight[5], 90)]
runDown = [pygame.transform.rotate(runRight[0], 270),
           pygame.transform.rotate(runRight[1], 270),
           pygame.transform.rotate(runRight[2], 270),
           pygame.transform.rotate(runRight[3], 270),
           pygame.transform.rotate(runRight[4], 270),
           pygame.transform.rotate(runRight[5], 270)]
medkitImage = pygame.image.load('medkit.png')
zombieRight = pygame.image.load('zombieR.png')
zombieLeft = pygame.transform.rotate(zombieRight, 180)
zombieUp = pygame.transform.rotate(zombieRight, 90)
zombieDown = pygame.transform.rotate(zombieRight, 270)
backGround = pygame.image.load('bg.jpg')
bulletSound = pygame.mixer.Sound('shoot.wav')
bulletSound.set_volume(0.1)
dieSound = pygame.mixer.Sound('die.wav')
dieSound.set_volume(0.7)
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

bullets = []
zombies = []
medkits = []
difficulty = 0



class character:
    health = 100
    width = 135
    height = 80
    x = screenWidth / 2
    y = screenHeight / 2
    velocity = 7
    left = False
    right = True
    up = False
    down = False
    isFiring = False
    isAlive = False
    isMoving = False
    fireDirectionX = 0
    fireDirectionY = 0
    walkCount = 0

    def draw():
        if character.left:
            if character.isMoving:
                win.blit(runLeft[character.walkCount // 4], (character.x + 20, character.y))
                character.isMoving = False
            win.blit(soldierLeft, (character.x, character.y))
        elif character.right:
            if character.isMoving:
                win.blit(runRight[character.walkCount // 4], (character.x - 20, character.y))
                character.isMoving = False
            win.blit(soldierRight, (character.x, character.y))
        elif character.up:
            if character.isMoving:
                win.blit(runUp[character.walkCount // 4], (character.x, character.y + 20))
                character.isMoving = False
            win.blit(soldierUp, (character.x, character.y))
        elif character.down:
            if character.isMoving:
                win.blit(runDown[character.walkCount // 4], (character.x, character.y - 20))
                character.isMoving = False
            win.blit(soldierDown, (character.x, character.y))
        character.walkCount += 1



class enemy:
    zombieWidth = 80
    zombieHeight = 80
    zombieCount = 0
    deadZombie = 0
    points = 0
    apocalypse = False

    def __init__(self):

        self.chance = random.randint(1, 4)
        self.velocity = random.randint(2, 5)
        self.borderControl = 0
        self.isAlive = True
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        if self.chance == 1:
            self.positionX = random.uniform(20, screenWidth - 20 - enemy.zombieWidth)
            self.positionY = 10
            self.down = True
        elif self.chance == 2:
            self.positionY = random.uniform(20, screenHeight - 20 - enemy.zombieHeight)
            self.positionX = 10
            self.right = True
        elif self.chance == 3:
            self.positionX = random.uniform(20, screenWidth - 20 - enemy.zombieWidth)
            self.positionY = screenHeight - 10 - enemy.zombieHeight
            self.up = True
        elif self.chance == 4:
            self.positionY = random.uniform(20, screenHeight - 20 - enemy.zombieHeight)
            self.positionX = screenWidth - 10 - enemy.zombieWidth
            self.left = True

    def draw(self):
        if self.left:
            self.positionX -= self.velocity - (self.borderControl * screenWidth)
            win.blit(zombieLeft, (self.positionX, self.positionY))
        elif self.right:
            self.positionX += self.velocity - (self.borderControl * screenWidth)
            win.blit(zombieRight, (self.positionX, self.positionY))
        elif self.up:
            self.positionY -= self.velocity - (self.borderControl * screenHeight)
            win.blit(zombieUp, (self.positionX, self.positionY))
        elif self.down:
            self.positionY += self.velocity - (self.borderControl * screenHeight)
            win.blit(zombieDown, (self.positionX, self.positionY))


class circle:
    radius = 5
    bulletCount = 0
    velocity = 13

    def __init__(self, circleX=0.0, circleY=0.0, directionX=0, directionY=0):
        if character.right:
            self.circleX = circleX + character.width
            self.circleY = circleY + character.height - 20
        elif character.left:
            self.circleX = circleX
            self.circleY = circleY + 20
        elif character.up:
            self.circleX = circleX + character.height - 20
            self.circleY = circleY
        elif character.down:
            self.circleX = circleX + 20
            self.circleY = circleY + character.width

        self.velocityX = self.velocity * directionX
        self.velocityY = self.velocity * directionY
        self.isValid = True

    def draw(self):
        pygame.draw.circle(win, (255, 0, 0), (int(self.circleX), int(self.circleY)), self.radius)
        self.circleX += self.velocityX
        self.circleY += self.velocityY


class medkit:
    medCount = 0

    def __init__(self):
        self.x = random.randint(100, screenWidth - 100)
        self.y = random.randint(150, screenHeight - 150)


    def reset(self):
        self.x = random.randint(100, screenWidth - 100)
        self.y = random.randint(150, screenHeight - 150)
        self.usedAt = time.localtime().tm_sec

    def draw(self):
        win.blit(medkitImage, (self.x + 20, self.y + 20))


def drawGameWindow():

    if character.walkCount + 1 >= 24:
        character.walkCount = 0
    win.blit(backGround, (0, 0))
    textfont = pygame.font.SysFont(None, 36)
    pointInfo = textfont.render('Points : ' + str(int(enemy.points)), True, (255, 0, 0), (255, 255, 255))
    zombieInfo = textfont.render('Zombies : ' + str(enemy.zombieCount), True, (255, 0, 0), (255, 255, 255))
    Info = textfont.render('Shoot:Space, Slow Time:z ', True, (255, 0, 0), (255, 255, 255))
    character.draw()

    if medkit.medCount:
        medDistance = math.sqrt(
                      pow((character.x + 40) - (medkits[0].x + 20), 2) + \
                      pow((character.y + 40) - (medkits[0].y + 20), 2)
                      )
        if medDistance < 60:
            character.health += 30
            medkit.medCount -= 1
            medkits[0].usedAt = time.localtime().tm_sec
        else:
            medkits[0].draw()

    else:
        currentTime = time.localtime().tm_sec
        if currentTime - medkits[0].usedAt == 5:
            medkits[0].reset()
            medkit.medCount += 1

    if enemy.apocalypse:
        for index in range(enemy.zombieCount):
            if 0 < zombies[index].positionX < screenWidth and 0 < zombies[index].positionY < screenHeight:
                zombies[index].borderControl = 0
                if zombies[index].isAlive:
                    zombies[index].draw()
                    spaceX = pow((character.x + 40) - (zombies[index].positionX + enemy.zombieWidth / 2), 2)
                    spaceY = pow((character.y + 40) - (zombies[index].positionY + enemy.zombieHeight / 2), 2)
                    space = math.sqrt(spaceX + spaceY)
                    if space < 60:
                        character.health -= 2
                for counter in range(circle.bulletCount):
                    if bullets[counter].isValid:
                        distanceX = pow(bullets[counter].circleX - (zombies[index].positionX + enemy.zombieWidth / 2),
                                        2)
                        distanceY = pow(bullets[counter].circleY - (zombies[index].positionY + enemy.zombieHeight / 2),
                                        2)
                        distance = math.sqrt(distanceX + distanceY)
                        if distance < 40 and zombies[index].isAlive and bullets[counter].isValid:
                            dieSound.play()
                            zombies[index].isAlive = False
                            bullets[counter].isValid = False
                            enemy.points += 10
                            enemy.deadZombie += 1



            else:
                zombies[index].borderControl = 1
                zombies[index].draw()

    if character.isFiring:
        for index in range(circle.bulletCount):
            if 0 < bullets[index].circleX < screenWidth and \
                    0 < bullets[index].circleY < screenHeight and \
                    bullets[index].isValid:
                bullets[index].draw()
            else:
                bullets[index].isValid = False

    win.blit(pointInfo, (100, 100))
    win.blit(zombieInfo, (1000, 100))
    win.blit(Info, (100, 650))
    pygame.draw.rect(win, (255, 255, 255), (490, 650, 300, 40))
    character.health = min(character.health,100)
    pygame.draw.rect(win, (255, 0, 0), (500, 660, (character.health * 280) / 100, 20))
    pygame.display.update()


def addZombie():
    zombies.append(enemy())
    enemy.zombieCount += 1
    enemy.apocalypse = True


def gameIntro():
    intro = True
    introFont = pygame.font.SysFont(None, 64)
    introInfo = introFont.render('Press space to start.', True, (255, 0, 0), (255, 255, 255))
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                character.isAlive = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for i in range(20):
                        addZombie()
                    intro = False
        win.blit(backGround, (0, 0))
        win.blit(introInfo, (400, 300))
        pygame.display.update()
        clock.tick(15)


def gameOutro():
    outro = True
    outroFont = pygame.font.SysFont(None, 64)
    outroInfo = outroFont.render('GAME OVER', True, (255, 0, 0), (255, 255, 255))
    outroInfo2 = outroFont.render('Your Points : ' + str(enemy.points), True, (255, 0, 0), (255, 255, 255))

    while outro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                character.isAlive = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    outro = False
                    gameReset()

        win.blit(backGround, (0, 0))
        win.blit(outroInfo, (400, 300))
        win.blit(outroInfo2, (350, 400))
        pygame.display.update()
        clock.tick(15)


def gameReset():
    character.health = 100
    character.x = screenWidth / 2
    character.y = screenHeight / 2
    character.left = False
    character.right = True
    character.up = False
    character.down = False
    character.isFiring = False
    character.isAlive = False
    character.isMoving = False
    character.fireDirectionX = 0
    character.fireDirectionY = 0
    character.isAlive = True
    enemy.points = 0


# MAIN
gameIntro()
character.isAlive = True
medkits.append(medkit())
medkit.medCount += 1
while character.isAlive:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            character.isAlive = False

    # LISTEN KEYBOARD
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and character.x > 0 + character.velocity:
        character.x -= character.velocity
        character.isMoving = True
        character.fireDirectionY = 0
        character.fireDirectionX = -1
        character.right = False
        character.down = False
        character.up = False
        character.left = True

    if keys[pygame.K_RIGHT] and character.x < screenWidth - character.width - character.velocity:
        character.x += character.velocity
        character.isMoving = True
        character.fireDirectionY = 0
        character.fireDirectionX = 1
        character.left = False
        character.down = False
        character.up = False
        character.right = True

    if keys[pygame.K_UP] and character.y > 0 + character.velocity:
        character.y -= character.velocity
        character.isMoving = True
        character.fireDirectionX = 0
        character.fireDirectionY = -1
        character.down = False
        character.right = False
        character.left = False
        character.up = True

    if keys[pygame.K_DOWN] and character.y < screenHeight - character.width - character.velocity:
        character.y += character.velocity
        character.isMoving = True
        character.fireDirectionX = 0
        character.fireDirectionY = 1
        character.left = False
        character.right = False
        character.up = False
        character.down = True

    if keys[pygame.K_z]:
        clock.tick(10)
    else:
        clock.tick(100)

    if keys[pygame.K_SPACE]:
        bulletSound.play()
        bullets.append(circle(character.x, character.y, character.fireDirectionX, character.fireDirectionY))
        circle.bulletCount += 1
        character.isFiring = True

    if enemy.deadZombie >= (20 + difficulty):
        difficulty += 5
        for i in range(20 + difficulty):
            addZombie()
        enemy.deadZombie = 0

    # DRAW
    drawGameWindow()

    if character.health <= 0:
        character.isAlive = False
        gameOutro()

# EXIT
pygame.quit()
