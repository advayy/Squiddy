import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Squiddy!")

walkRight = [pygame.image.load('squiddy_data/R1 copy.png'),
             pygame.image.load('squiddy_data/R2 copy.png'),
             pygame.image.load('squiddy_data/R3 copy.png'),
             pygame.image.load('squiddy_data/R4 copy.png'),
             pygame.image.load('squiddy_data/R5 copy.png'),
             pygame.image.load('squiddy_data/R6 copy.png'),
             pygame.image.load('squiddy_data/R7 copy.png'),
             pygame.image.load('squiddy_data/R8 copy.png'),
             pygame.image.load('squiddy_data/R9 copy.png')]
walkLeft = [pygame.image.load('squiddy_data/L1 copy.png'),
            pygame.image.load('squiddy_data/L2 copy.png'),
            pygame.image.load('squiddy_data/L3 copy.png'),
            pygame.image.load('squiddy_data/L4 copy.png'),
            pygame.image.load('squiddy_data/L5 copy.png'),
            pygame.image.load('squiddy_data/L6 copy.png'),
            pygame.image.load('squiddy_data/L7 copy.png'),
            pygame.image.load('squiddy_data/L8 copy.png'),
            pygame.image.load('squiddy_data/L9 copy.png')]
background = pygame.image.load('squiddy_data/Background.jpg')
character = pygame.image.load('squiddy_data/standing copy.png')
bubble_mov = [pygame.image.load('squiddy_data/BB1.png'), pygame.image.load('squiddy_data/BB2.png'),
              pygame.image.load('squiddy_data/BB3.png'), pygame.image.load('squiddy_data/BB4.png')]

sn_bubble = pygame.mixer.Sound('squiddy_data/Bubble.wav')
sn_pop = pygame.mixer.Sound('squiddy_data/Pop.wav')
sn_UTS = pygame.mixer.music.load('squiddy_data/UTS_LM.mp3')
sn_endgame = pygame.mixer.Sound('squiddy_data/End_Game.wav')
pygame.mixer.music.play(-1)

score = 0

clock = pygame.time.Clock()


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 20
        self.isJump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing_still = False
        self.hitBox = (self.x + 19, self.y + 4, 26, 56)
        self.is_dropping = False
        self.drop_count = 0

    def drop(self):
        self.is_dropping = True
        self.drop_count = 0
        self.isJump = False
        self.jump_count = 10
        self.y = 200
        self.x = 244 - (self.width // 2)

    def draw(self, window):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        self.hitbox_frnt = (self.x + 19, self.y + 4, 26, 56)
        self.hitbox_right = (self.x + 4, self.y + 10, 52, 54)
        self.hitbox_left = (self.x + 4, self.y + 10, 52, 54)

        if not self.standing_still:
            if self.left:
                window.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
                self.hitBox = self.hitbox_left
            elif self.right:
                window.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
                self.hitBox = self.hitbox_right
        else:
            if self.left:
                window.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.hitBox = self.hitbox_left
            elif self.right:
                window.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.hitBox = self.hitbox_left
            else:
                window.blit(character, (self.x, self.y))
                self.hitBox = self.hitbox_frnt

    def hit(self):
        sn_endgame.play()
        self.x = 250
        self.y = 366
        self.walkCount = 0
        self.jump_count = 10
        self.isJump = False
        font1 = pygame.font.SysFont('arial', 40)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width() / 2), 150))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.QUIT()


class enemy(object):
    e_fish_l = [pygame.image.load('squiddy_data/FL1.png'), pygame.image.load('squiddy_data/FL2.png'),
                pygame.image.load('squiddy_data/FL3.png'), pygame.image.load('squiddy_data/FL4.png'),
                pygame.image.load('squiddy_data/FL5.png'), pygame.image.load('squiddy_data/FL6.png')]
    e_fish_r = [pygame.image.load('squiddy_data/FR1.png'), pygame.image.load('squiddy_data/FR2.png'),
                pygame.image.load('squiddy_data/FR3.png'), pygame.image.load('squiddy_data/FR4.png'),
                pygame.image.load('squiddy_data/FR5.png'), pygame.image.load('squiddy_data/FR6.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 5
        self.hitBox = (self.x, self.y, self.width, self.height)
        self.health = 100
        self.vanish = False
        self.is_dropping = False
        self.drop_count = 0
        self.enemy_gen = 0

    def draw(self, window):
        if not self.vanish:
            self.move()
            if self.walkCount >= 18:
                self.walkCount = 0

            self.hitbox_right = (self.x + 2, self.y + 4, 50, 48)
            self.hitbox_left = (self.x + 10, self.y + 4, 50, 48)

            if self.vel > 0:
                window.blit(self.e_fish_r[self.walkCount // 3], (self.x, self.y))
                self.hitBox = self.hitbox_right
                self.walkCount += 1
            else:
                window.blit(self.e_fish_l[self.walkCount // 3], (self.x, self.y))
                self.hitBox = self.hitbox_left
                self.walkCount += 1

            pygame.draw.rect(window, (0, 255, 0), (self.hitBox[0], (self.hitBox[1] - 15), self.hitBox[2], 10))
            pygame.draw.rect(window, (255, 0, 0),
                             (self.hitBox[0], (self.hitBox[1] - 15), (self.hitBox[2] * (1 - self.health / 100)), 10))

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0

    def hit(self):
        self.health -= bullet.damage_val
        if self.health <= 0:
            sn_endgame.play()
            pygame.time.delay(100)
            self.vanish = True
            self.hitBox = (1, 1, 0, 0)
            pygame.time.delay(300)
            self.reset_me()

    def reset_me(self):
        self.health = 100
        self.y = 200
        self.x = 244 - (self.width // 2)
        self.vanish = False
        self.hitBox = (self.x, self.y, self.width, self.height)
        self.is_dropping = True
        self.enemy_gen += 1
        if self.vel > 0:
            self.vel += 2 * self.enemy_gen
        else:
            self.vel -= 2 * self.enemy_gen


class projectile(object):
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.facing = facing
        self.velocity = 25 * facing
        self.moveCount = 0
        self.damage_val = 7

    def draw(self, win):
        win.blit(bubble_mov[0], (self.x, self.y))


# mainloop
font = pygame.font.SysFont('arial', 20, True, False)  # bold and not italic
squiddy = Player(250, (436 - 70), 64, 64)
evilFish = enemy(50, (436 - 70), 64, 64, (450 - 64))
bubble_bullets = []
run = True
shootLoop = 0


def redraw_game_window():
    win.blit(background, (0, 0))
    text = font.render("Score: " + str(score), 1, (0, 0, 0))
    win.blit(text, (370, 10))
    for bullet in bubble_bullets:
        if bullet.facing == 0:
            bubble_bullets.pop(bubble_bullets.index(bullet))
        else:
            bullet.draw(win)
    squiddy.draw(win)
    evilFish.draw(win)
    pygame.display.update()


while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sn_endgame.play()
            pygame.time.delay(300)
            run = False

    if squiddy.is_dropping:
        if squiddy.drop_count >= -10:
            if squiddy.y < 365:
                squiddy.y -= int((squiddy.drop_count ** 2) * 0.5 * -1)  # (runs a quadratic function)
                squiddy.drop_count -= 1
        else:
            squiddy.y = 366
            squiddy.drop_count = 0
            squiddy.is_dropping = False

    if evilFish.is_dropping:
        if evilFish.drop_count >= -10:
            if evilFish.y < 365:
                evilFish.y -= int((evilFish.drop_count ** 2) * 0.5 * -1)  # (runs a quadratic function)
                evilFish.drop_count -= 1
        else:
            evilFish.y = 366
            evilFish.drop_count = 0
            evilFish.is_dropping = False

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for bullet in bubble_bullets:
        if bullet.y - (bullet.height // 2) < evilFish.hitBox[1] + evilFish.hitBox[3] and bullet.y + (
                bullet.height // 2) > evilFish.hitBox[1]:
            if bullet.x + (bullet.width) > evilFish.hitBox[0] and bullet.x - (bullet.width // 2) < evilFish.hitBox[0] + \
                    evilFish.hitBox[2]:
                sn_pop.play()
                evilFish.hit()
                score += 1 + 2 * (evilFish.enemy_gen)
                if score >= 1000:
                    sn_endgame.play()
                    pygame.time.delay(300)
                    run = False
                bubble_bullets.pop(bubble_bullets.index(bullet))

        if 500 > bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bubble_bullets.pop(bubble_bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_x]:
        sn_endgame.play()
        pygame.time.delay(300)
        run = False
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if squiddy.left:
            facing = -1
        elif squiddy.right:
            facing = 1
        else:
            facing = 0
        if len(bubble_bullets) < 5:  # using //2 gives u an integer without a decimal which can damage code positioning
            if facing != 0:
                sn_bubble.play()
            bubble_bullets.append(projectile(squiddy.x + 13, squiddy.y + 26, facing))
        shootLoop = 1
    if keys[pygame.K_LEFT]:
        if squiddy.x >= squiddy.velocity:
            squiddy.x -= squiddy.velocity
        else:
            squiddy.x = 0
        squiddy.right = False
        squiddy.left = True
        squiddy.standing_still = False
    elif keys[pygame.K_RIGHT]:
        if squiddy.x < 500 - squiddy.width:
            squiddy.x += squiddy.velocity
        else:
            squiddy.x = 500 - squiddy.width
        squiddy.right = True
        squiddy.left = False
        squiddy.standing_still = False
    elif keys[pygame.K_DOWN] and not squiddy.isJump:
        squiddy.left = False
        squiddy.right = False
    else:
        squiddy.standing_still = True
        squiddy.walkCount = 0

    if not squiddy.isJump:
        if keys[pygame.K_UP] and not squiddy.is_dropping:
            squiddy.isJump = True
            squiddy.walkCount = 0
            squiddy.jump_count = 10
    else:
        if squiddy.jump_count >= -10:
            neg = 1
            if squiddy.jump_count < 0:
                neg = -1
            squiddy.y -= int((squiddy.jump_count ** 2) * 0.5 * neg)  # (runs a quadratic function)
            squiddy.jump_count -= 1
        else:
            squiddy.jump_count = 10
            squiddy.isJump = False

    y_condition = squiddy.hitBox[1] + squiddy.hitBox[3] // 2 > evilFish.hitBox[1] - evilFish.hitBox[3] // 2 and \
                  squiddy.hitBox[1] - squiddy.hitBox[3] // 2 < evilFish.hitBox[1] + evilFish.hitBox[3] // 2
    x_condition = squiddy.hitBox[0] + squiddy.hitBox[2] // 2 > evilFish.hitBox[0] - evilFish.hitBox[2] // 2 and \
                  squiddy.hitBox[0] - squiddy.hitBox[2] // 2 < evilFish.hitBox[0] + evilFish.hitBox[2] // 2

    if y_condition and evilFish.vanish == False:
        if x_condition:
            squiddy.hit()
            squiddy.drop()
            score -= 5

    redraw_game_window()

pygame.quit()
