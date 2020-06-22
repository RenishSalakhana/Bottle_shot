
import pygame, sys
from math import cos, sin, pi, degrees, radians

pygame.init()

monitor_size = (pygame.display.Info().current_w,pygame.display.Info().current_h)
win = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.mouse.set_visible(0)
pygame.display.set_caption("bottle shoot game for shivanshu and shivansh")

bg_img = pygame.image.load('data/bg_image.jpg')
gun_load = pygame.image.load('data/transparent-gun-9mm.png')
bullet_load = pygame.image.load('data/9mm_bullet.png')


fir_sound = pygame.mixer.Sound('data/bullet.wav')
hit_sound = pygame.mixer.Sound('data/glassBreak.wav')
cheer_sound = pygame.mixer.Sound('data/cheering.wav')

clock = pygame.time.Clock()

score = 0
###################################################################################################
### global function
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
        
def gameOver():
    global level
    w, h = win.get_size()
    font = pygame.font.Font('freesansbold.ttf', 50)
    score_str = font.render("level "+str(level+1)+' complete ', True, (0,0,0))
    textRect = score_str.get_rect()
    textRect.center = (w//2, h//2)
    win.blit(score_str, textRect)
    pygame.display.update()

def level_fn(level):
    global greenbottles
    dist={0:(0,0), 1:(1024,0), 2:(1024,720), 3:(0,720)}
    for i in range((level%4)+1):
        greenbottles.append(bottleClass(dist[i], i+1))    
    
def redrawGameWindwow():
    global winn, level, score
    w, h = win.get_size()
    path = (int(w * 0.1), int(h * 0.1), int(w * 0.8), int(h * 0.8))
    pygame.draw.rect(win, (200,0,0), path, 2)
    
    for gb in greenbottles:
        gb.draw(win)
    ##### winning logic
    if greenbottles==[] and winn:
        cheer_sound.play()
        gun.visible = False
        winn = False
    if not winn:
        gameOver()
        pygame.time.delay(4000)
        level += 1
        if level % 4==0:
            score += 150
            gun.vel += 2
        level_fn(level)
        winn = True
        gun.visible = True
            
    
    gun.draw(win)
    
    text = font.render('Score: ' + str(score), 4, (0, 0, 0))
    win.blit(text, (win.get_width()*0.85,20))
    text = font.render('Level: ' + str(level+1), 4, (0, 0, 0))
    win.blit(text, (win.get_width()*0.05,20))

    pygame.display.update()


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
##        pygame.draw.rect(win, (0,255,255), (self.pos[0] + self.x, self.pos[1] + self.y, self.b_w, self.b_h), 2)

        
############################################################################################
        
class gunClass(object):
    def __init__(self):
        self.g_angle = 0        # in degree
        self.b_angle = 0        # in radian
        self.vel =1
        self.time = 0

        self.gun_img = pygame.transform.rotozoom(gun_load,1, 0.3)
        self.bullet_img = pygame.transform.rotozoom(bullet_load, 0,0.1)

        self.bulletx=2000
        self.bullety=0
        self.startP = [0,0]
        self.visible = True     
        

    def draw(self, win):
        if self.visible:
            w, h = win.get_size()
            gun_w, gun_h = self.gun_img.get_size()
            blitRotate(win, self.gun_img, (w//2,h//2), (gun_w//2,gun_h//2), self.g_angle)
            self.g_angle += self.vel
            if self.g_angle >= 360:
                self.g_angle = 0
            ### for bullet
            if self.bulletx < w+20 and self.bulletx > -20 and self.bullety < h+20 and self.bullety > -20  :
                self.bulletPath()
                self.time += 2
            else:
                self.time = 0

    def bulletPath(self):
        if self.visible:
            velx = cos(self.b_angle) * 20
            vely = sin(self.b_angle) * 20

            distX = velx * self.time
            distY = vely * self.time

            self.bulletx = round(self.startP[0] + distX)
            self.bullety = round(self.startP[1] - distY)
            b_w,b_h=self.bullet_img.get_size()
            win.blit(self.bullet_img, (gun.bulletx-b_w//2, gun.bullety-b_h//2))

    def shoot(self,win):
        if self.time is 0:
            fir_sound.play()
            w, h = win.get_size()
            self.startP[0]= int(w//2 + 90 * cos(radians(23+self.g_angle))) #newX = oldX + dist * cos(angle)
            self.startP[1]= int(h//2 - 90 * sin(radians(23+self.g_angle)))
            self.bullet_img = pygame.transform.rotozoom(bullet_load, -90+self.g_angle,0.1)
            self.bulletx = round(self.startP[0])
            self.bullety = round(self.startP[1])
            
            self.b_angle = radians(self.g_angle)

        
#############################################################################################
#main loop
font = pygame.font.SysFont('comicsans',30 , True)

run = True
fullscreen = False
greenbottles=[]
level = 0
gun = gunClass()
winn = True
level_fn(level)

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

    if keys[pygame.K_SPACE]:
        gun.shoot(win)
    
        
    for gb in greenbottles:
        if (gb.pos[0] + gb.x < gun.bulletx and gun.bulletx < gb.pos[0] + gb.x + gb.b_w) and (gb.pos[1]+gb.y < gun.bullety and gun.bullety < gb.pos[1]+gb.y+gb.b_h):
            score += 10
            hit_sound.play()
            greenbottles.pop(greenbottles.index(gb))
            
    redrawGameWindwow()    
pygame.quit()

 
