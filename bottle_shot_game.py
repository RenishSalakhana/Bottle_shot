
import pygame, sys
from math import cos, sin, pi, degrees, radians

pygame.init()

monitor_size = (pygame.display.Info().current_w,pygame.display.Info().current_h)
win = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

pygame.display.set_caption("bolle shoot game for shivansh")
### image load
bg_img = pygame.image.load('data/bg_image.jpg')
gun_load = pygame.image.load('data/transparent-gun-9mm.png')
bullet_load = pygame.image.load('data/9mm_bullet.png')

### sfg load
fir_sound = pygame.mixer.Sound('data/bullet.wav')
hit_sound = pygame.mixer.Sound('data/glassBreak.wav')
cheer_sound = pygame.mixer.Sound('data/cheering.wav')

clock = pygame.time.Clock()

score = 0

### image center rotation
def blitRotate(surf, image, pos, originPos, angle):
    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

##########################################################################
class bottleClass(object):
    def __init__(self, dist, pn):
        self.x = dist[0]
        self.y = dist[1]
        self.vel = 6
        self.bottle = pygame.image.load('data/green-glass-bottle.png')
        self.bottle_img = pygame.transform.rotozoom(self.bottle, 0, 0.2)
        self.b_w, self.b_h = self.bottle_img.get_size()
        self.run_part= pn
        self.pos = (0,0,0,0)

    def draw(self, win):
        w, h = win.get_size()
        self.b_w, self.b_h = self.bottle_img.get_size()
        path = (int(w * 0.1), int(h * 0.1), int(w * 0.8), int(h * 0.8))
        self.pos = (path[0]-self.b_w//2, path[1] - self.b_h//2)
        
        if self.run_part == 1:
            self.bottle_img = pygame.transform.rotozoom(self.bottle, -90, 0.2)
            self.x += self.vel
            if self.x >= path[2]:
                self.run_part = 2
                self.x = path[2]
            if self.y is not 0:
                self.y = 0

        elif self.run_part == 2:
            self.bottle_img = pygame.transform.rotozoom(self.bottle,180, 0.2)
            self.y += self.vel   
            if self.x is not path[2]:
                self.x = path[2]
            if self.y >= path[3]:
                self.run_part = 3
                self.y = path[3]

        elif self.run_part == 3:
            self.bottle_img = pygame.transform.rotozoom(self.bottle,90, 0.2)
            self.x -= self.vel
            if self.x <= 0:
                self.run_part = 4
                self.x = 0
            if self.y is not path[3]:
                self.y = path[3]
        else:
            self.bottle_img = pygame.transform.rotozoom(self.bottle,0, 0.2)
            self.y -= self.vel
            if self.x is not 0:
                self.x = 0
            if self.y < 0:
                self.run_part = 1
                self.y = 0

        win.blit(self.bottle_img, (self.pos[0] + self.x, self.pos[1] + self.y))
        #pygame.draw.rect(win, (0,255,255), (self.pos[0] + self.x, self.pos[1] + self.y, self.b_w, self.b_h), 2)

        
############################################################################################
        
class gunClass(object):
    def __init__(self):
        self.angle = 0
        self.vel = 0
        self.gun_img = pygame.transform.rotozoom(gun_load,1, 0.3)
        self.bulletx=0
        self.bullety=0
        

    def draw(self, win):
        w, h = win.get_size()
        gun_w, gun_h = self.gun_img.get_size()
        blitRotate(win, self.gun_img, (w//2,h//2), (gun_w//2,gun_h//2), self.angle)
        self.angle += self.vel
        if self.angle >= 360:
            self.angle = 0

    def bulletPath(self, startx, starty, angle, time):
        velx = cos(angle) * 10
        vely = sin(angle) * 10

        distX = velx * time
        distY = vely * time

        self.bulletx = round(distX + startx)
        self.bullety = round(starty - distY)


    def shoot(self,win):
        fir_sound.play()
        w, h = win.get_size()
        self.bulletx = w//2
        self.bullety = h//2
        return radians(self.angle)

        
#############################################################################################
        
def gameOver():
    w, h = win.get_size()
    font = pygame.font.Font('freesansbold.ttf', 50)
    score_str = font.render("Score :"+str(score), True, (0,0,255))
    win.blit(score_str, (w//2, h//2))
    
def redrawGameWindwow():
    global winn
    w, h = win.get_size()
    path = (int(w * 0.1), int(h * 0.1), int(w * 0.8), int(h * 0.8))
    pygame.draw.rect(win, (200,0,0), path, 2)
    
    for gb in greenbottles:
        gb.draw(win)
    ##### winning logic
    if greenbottles==[] and winn:
        gun.vel = 0
        cheer_sound.play()
        winn = False
    if not winn:
        gameOver()
    
    gun.draw(win)
    
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (win.get_width()*0.9,10))

    pygame.display.update()


######################################################################################################
#main loop
font = pygame.font.SysFont('comicsans',30 , True)

run = True
fullscreen = False
dist={1:(0,0), 2:(1024,0), 3:(1024,720), 4:(0,720)}
greenbottles=[]
for i in range(1,2):
    greenbottles.append(bottleClass(dist[i], i))
gun = gunClass()
time = 0
angle = 0
winn = True

while run:
    clock.tick(27)
##    win.fill((50,100,100))
    bg_img = pygame.transform.scale(bg_img,(win.get_width(), win.get_height()) )
    win.blit(bg_img,(0,0))

    for event in pygame.event.get():
        ######## exit
        if event.type == pygame.QUIT:
            run = False
        ######## screen resize
        if event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    win = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                else:
                    win = pygame.display.set_mode((win.get_width(), win.get_height()), pygame.RESIZABLE)
                    

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and time == 0:
        angle = gun.shoot(win)
        gun.bulletPath(win.get_width()//2, win.get_height()//2, angle, time)

##    pygame.draw.circle(win, (0,255,255), (gun.bulletx, gun.bullety), 10)
    bullet_img = pygame.transform.rotozoom(bullet_load, -90,0.1)
    win.blit(bullet_img, (gun.bulletx+70, gun.bullety-45))
    if gun.bulletx < win.get_width()+20 and gun.bulletx > 0 and gun.bullety < win.get_height()+20 and gun.bullety > 0  :
        time += 2
        gun.bulletPath(win.get_width()//2, win.get_height()//2, angle, time)
    else:
        time = 0
    for gb in greenbottles:
        if (gb.pos[0] + gb.x < gun.bulletx and gun.bulletx < gb.pos[0] + gb.x + gb.b_w) and (gb.pos[1]+gb.y < gun.bullety and gun.bullety < gb.pos[1]+gb.y+gb.b_h):
            score += 1
            hit_sound.play()
            greenbottles.pop(greenbottles.index(gb))
    redrawGameWindwow()    
pygame.quit()

 
