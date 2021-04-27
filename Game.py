import sys

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)
windowHeight = 600
windowWidth = 800
FRAMERATE = 60
clock = pygame.time.Clock()


def empty(seq):
    try:
        return all(map(empty, seq))
    except TypeError:
        return False


class Enemy(pygame.sprite.Sprite):
    left = True
    right = False
    countTouch = 0

    def __init__(self, x, y):
        super().__init__()
        self.sizex = 40
        self.sizey = 40
        self.enemyfig_image = pygame.Surface((self.sizex, self.sizey))
        self.enemyfig_image.fill(RED)
        self.enemyfig_rect = self.enemyfig_image.get_rect()
        self.velocity = 2
        self.x = x
        self.y = y
        self.countEne = 8
        self.updateCount = 0
        self.updateCountMax = 2
        self.speedDown = 60
        self.rect = pygame.Rect(self.x, self.y, self.sizex, self.sizey)

    def moveDown(self):
        if not self.y > windowHeight - self.sizey:
            self.y += self.speedDown

    def moveRight(self):
        if not self.x > windowWidth - self.sizex:
            self.x += self.velocity

    def moveLeft(self):
        if not self.x < 0:
            self.x -= self.velocity


class Shoot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.velocity = 7
        self.sizex = 6
        self.sizey = 20
        self.shoot_image = pygame.Surface((self.sizex, self.sizey))
        self.shoot_image.fill(MAGENTA)
        self.shoot_rect = self.shoot_image.get_rect()
        self.x = x
        self.y = y

    def moveUp(self):
        self.y -= self.velocity

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.sizex, self.sizey)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sizex = 40
        self.sizey = 40
        self.figur_image = pygame.Surface((self.sizex, self.sizey))
        self.figur_image.fill(WHITE)
        self.figur_rect = self.figur_image.get_rect()
        self.velocity = 5
        self.x = windowWidth / 2 - self.sizex
        self.y = 500

    def moveUp(self):
        if not self.y < 0:
            self.y -= self.velocity

    def moveDown(self):
        if not self.y > windowHeight - self.sizey:
            self.y += self.velocity

    def moveRight(self):
        if not self.x > windowWidth - self.sizex:
            self.x += self.velocity

    def moveLeft(self):
        if not self.x < 0:
            self.x -= self.velocity


class App:
    def __init__(self):
        self.running = True
        self.screen = None
        self.player = Player()
        self.countRow = 1
        self.howmanyrows = 5
        self.allEnemies = [[] for _ in range(0, self.howmanyrows)]
        self.leftlist = []
        self.leftmin = None
        self.index1l = None
        self.index2l = None
        self.rightlist = []
        self.rightmin = None
        self.index1r = None
        self.index2r = None
        self.howmanyrowsstart = 4
        for i in range(0, 8):
            self.allEnemies[0].append(Enemy(i * 80, 50))
        self.shots = []
        self.counter = 0
        self.key_pressed_space = False
        self.init = False

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((windowWidth, windowHeight), pygame.HWSURFACE)
        pygame.display.set_caption("Aliens")
        self.running = True

    def on_loop(self):
        if empty(self.allEnemies) and self.countRow >= self.howmanyrows - 1:
            print("You won")
            pygame.quit()
            sys.exit()

        if not self.howmanyrowsstart == 1 and self.init == False:
            self.init = True
            self.countRow += 1
            while self.howmanyrowsstart > 1:
                for i in range(0, 8):
                    self.allEnemies[self.countRow].append(Enemy(i * 80, 50))
                for enemy in self.allEnemies[self.countRow]:
                    enemy.moveDown()
                self.howmanyrowsstart -= 1

        if Enemy.countTouch == 4:  # Move down and new Enemies
            Enemy.countTouch = 0
            for listenemy in self.allEnemies:
                for enemy in listenemy:
                    enemy.moveDown()
            if self.countRow < self.howmanyrows - 1:
                self.countRow += 1
                for i in range(0, 8):
                    self.allEnemies[self.countRow].append(Enemy(i * 80, 50))

        try:
            if len(self.allEnemies[self.countRow]) == 0 and self.countRow < self.howmanyrows - 1:
                Enemy.countTouch = 0
                Enemy.left = True
                Enemy.right = False
                self.countRow += 1
                if self.countRow <= self.howmanyrows:
                    for i in range(0, 8):
                        self.allEnemies[self.countRow].append(Enemy(i * 80, 50))
        except:
            pass

        # Getting the index of the enemy far left
        self.leftlist.clear()
        for i in range(0, self.howmanyrows):
            if not len(self.allEnemies[i]) == 0:
                self.leftlist.append(self.allEnemies[i][0])
        self.leftmin = min(ene.x for ene in self.leftlist)
        for listenemy in self.allEnemies:
            for enemy in listenemy:
                if enemy.x == self.leftmin:
                    self.index2l = listenemy.index(enemy)
                    self.index1l = self.allEnemies.index(listenemy)

        # Getting the index of the enemy far right
        self.rightlist.clear()
        for i in range(0, self.howmanyrows):
            if not len(self.allEnemies[i]) == 0:
                self.rightlist.append(self.allEnemies[i][-1])
        self.rightmin = max(ene.x for ene in self.rightlist)
        for listenemy in self.allEnemies:
            for enemy in listenemy:
                if enemy.x == self.rightmin:
                    self.index2r = listenemy.index(enemy)
                    self.index1r = self.allEnemies.index(listenemy)

        # Left and Right
        if Enemy.left:
            for listenemy in self.allEnemies:
                for enemy in listenemy:
                    enemy.moveRight()
            if windowWidth - self.allEnemies[self.index1r][self.index2r].sizex <= \
                    self.allEnemies[self.index1r][self.index2r].x:
                Enemy.right = True
                Enemy.left = False
                Enemy.countTouch += 1
        if Enemy.right:
            for listenemy in self.allEnemies:
                for enemy in listenemy:
                    enemy.moveLeft()
            if self.allEnemies[self.index1l][self.index2l].x <= 0:
                Enemy.right = False
                Enemy.left = True
                Enemy.countTouch += 1

        for shot in self.shots:
            shot.moveUp()

        # Collision
        for listenemy in self.allEnemies:
            for enemy in listenemy:
                enemy.rect = pygame.Rect(enemy.x, enemy.y, enemy.sizex, enemy.sizey)
                # Shot collision
                for shot in self.shots:
                    shot.rect = pygame.Rect(shot.x, shot.y, shot.sizex, shot.sizey)
                    if enemy.rect.colliderect(shot.get_rect()):
                        self.allEnemies[self.allEnemies.index(listenemy)].remove(enemy)
                        self.shots.remove(shot)
                # Player Collision
                self.player.rect = pygame.Rect(self.player.x, self.player.y, self.player.sizex, self.player.sizey)
                if enemy.rect.colliderect(self.player):
                    print("You lost")
                    pygame.quit()
                    sys.exit()

    def on_render(self):
        self.screen.fill(BLACK)
        # Hier Sachen zum Rendern einfügen mit blit
        self.screen.blit(self.player.figur_image, (self.player.x, self.player.y))
        for listenemy in self.allEnemies:
            for enemy in listenemy:
                self.screen.blit(enemy.enemyfig_image, (enemy.x, enemy.y))
        for shot in self.shots:
            self.screen.blit(shot.shoot_image, (shot.x, shot.y))
        pygame.display.flip()

    def on_execute(self):
        if self.on_init() == False:
            self.running = False

        while self.running:
            self.counter += 1
            clock.tick(FRAMERATE)

            pygame.event.pump()
            keys = pygame.key.get_pressed()

            # Hier Keys einfügen
            if keys[pygame.K_ESCAPE]:
                self.running = False
            if keys[pygame.K_w]:
                self.player.moveUp()
            if keys[pygame.K_s]:
                self.player.moveDown()
            if keys[pygame.K_a]:
                self.player.moveLeft()
            if keys[pygame.K_d]:
                self.player.moveRight()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and not self.key_pressed_space:
                    if event.key == pygame.K_SPACE:
                        self.shots.append(Shoot(self.player.x + self.player.sizex / 2 - 3, self.player.y))
                        self.key_pressed_space = True

            self.on_loop()
            self.on_render()

            if self.counter == FRAMERATE:
                self.counter = 0
                self.key_pressed_space = False


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
