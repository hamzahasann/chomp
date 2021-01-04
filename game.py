import sys
import time
import pygame
from pygame.locals import *
import random

#Colour
BLACK=(0,0,0)
WHITE=(200,200,200)
RED=(128,0,0)
GREEN=(0,128,0)
BLUE=(0,0,128)
PURPLE=(128,0,128)
#Display
FPS=30
SCREEN_W=500
SCREEN_H=550
SPRITE={}
SOUND={}
SCREEN=pygame.display.set_mode([SCREEN_W+100,SCREEN_H])
SCREEN.fill(BLACK)

#Constants
LIMIT=10
h,w=10,10
sz=SCREEN_W/LIMIT
alive=[[True for i in range(w)] for j in range(h)]
text=["P1 turn", "P2 turn"]
text_win=["********P1 wins********", "********P2 wins********"]
cnt=0
game_over=False
end_time=3
start=0
rndb=[[0 for i in range(w)] for j in range(h)]
best_move={}
def game():
    global game_over
    while(True):
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            draw_grid()
            draw_bestmove()
            if game_over==False:draw_move()
            if game_over==True:
                if time.time()-start>end_time:
                    pygame.quit()
                    sys.exit()
                else:
                    draw_result()
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type==pygame.MOUSEBUTTONDOWN and event.button==1) and game_over==False:
                mouse_action()

            pygame.display.update()

def draw_grid():
    for x in range(0,h):
        for y in range(0,w):
            blk=pygame.Rect(x*sz,y*sz,sz,sz)
            pygame.draw.rect(SCREEN,find_col(x,y),blk)
            pygame.draw.rect(SCREEN,BLACK,blk,1)
    blk=pygame.Rect(0,0,sz,sz)
    pygame.draw.rect(SCREEN,BLUE,blk)
    pygame.draw.rect(SCREEN,BLACK,blk,1)

def draw_move():
    font=pygame.font.Font('freesansbold.ttf',32)
    txt=font.render(text[cnt],True,WHITE,BLACK)
    box=txt.get_rect()
    box.center=(250,int((SCREEN_H+SCREEN_W)/2))
    SCREEN.blit(txt,box)

def draw_result():
    font=pygame.font.Font('freesansbold.ttf',32)
    txt=font.render(text_win[cnt],True,WHITE,BLACK)
    box=txt.get_rect()
    box.center=(int(SCREEN_W/2),int((SCREEN_H+SCREEN_W)/2))
    SCREEN.blit(txt,box)

def draw_bestmove():
    font=pygame.font.Font('freesansbold.ttf',32)
    hash=zobrist()
    x,y=best_move[hash][0],best_move[hash][1]
    move_str="NONE"
    if cnt==0 and game_over==False:
        move_str=str(x)+" "+str(y)
        blk=pygame.Rect(y*sz,x*sz,sz,sz)
        pygame.draw.rect(SCREEN,PURPLE,blk)
        pygame.draw.rect(SCREEN,BLACK,blk,1)
    txt=font.render(move_str,True,WHITE,BLACK)
    box=txt.get_rect()
    box.center=(int(SCREEN_W+50),SCREEN_H//5)
    SCREEN.blit(txt,box)


def find_col(x,y):
    if alive[y][x]:
        return GREEN
    else: return RED

def inside(x,y):
    if x<w and y<h:
        return True
    return False

def mouse_action():
    x,y=pygame.mouse.get_pos()
    x=int(x/sz)
    y=int(y/sz)
    if x==0 and y==0:
        # end_game()
        global game_over,start
        game_over=True
        start=time.time()
    if(inside(x,y)):
        #print(x,y)
        if alive[y][x]:
            global cnt
            cnt=1-cnt
            # print(cnt)
            for r in range (y,h):
                for c in range(x,w):
                    alive[r][c]=False

def zobrist():
    hash=0
    for i in range(0,h):
        for j in range(0,w):
            if(alive[i][j]):
                hash^=rndb[i][j]
    return hash
def moves():
    with open("randomboard.txt",'r') as f:
        data=f.read()
        data=[i for i in data.split()]
        for i in range(len(data)):
            rndb[i//h][i%w]=int(data[i])

    with open("bestmoves.txt",'r') as f:
        data=f.read()
        data=[int(i) for i in data.split()]
        for i in range(0,len(data),3):
            best_move[data[i]]=[data[i+1],data[i+2]]

moves()

if __name__=="__main__":
    pygame.init()
    pygame.display.set_caption('CHOMP')
    clock=pygame.time.Clock()
    while True:
        game()
