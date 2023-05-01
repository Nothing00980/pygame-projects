

import pygame,random
from pygame.locals import *
from sys import exit
import math
import os

pygame.init()

fps=30 #frames per second. The higher, the harder
#direction of snake
left=-1,0
right=1,0
up=0,-1
down=0,1
green = (0,255,0)

white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
s_height = 600
screen_width = 900
directions=[up,down,right,left]
# gamewindow = pygame.display.set_mode((screen_width,s_height))

# bg_img = pygame.image.load('snake.jpg')
# bg_img = pygame.transform.scale(bg_img,(screen_width,s_height)).convert_alpha() 

# clock = pygame.time.Clock()


# font = pygame.font.SysFont(None,55)
# def text_screen(text,color,x,y):
#     screen_text = font.render(text,True,color)
#     gamewindow.blit(screen_text,[x,y])

# def welcomescreen():
#     exit_game = False
#     while not exit_game:
#         gamewindow.fill(black)
#         gamewindow.blit(bg_img,(0,0))
#         text_screen("Welcome to Snakes",green,250,260)

#         text_screen("press c for computer or h for human to Play",red,100,350)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 exit_game = True
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN:
#                     SnakeGame.start()


class Snake:
    def __init__(self,body , direction, color,speed):
        self.speed=speed
        self.body=body #initially located here
        self.color=color
        self.direction=self.newdirection=direction
        self.IsDead=False
    def UpdateDirection(self,game):
        self.direction=self.newdirection #the next direction is stored in newdirection....logic is updated here
    def Update(self,game):
        if self.IsDead:
            fadestep=5
            self.color=(max(self.color[0]-fadestep,0),max(self.color[1]-fadestep,0),max(self.color[2]-fadestep,0))
            if self.color[0]==0 and self.color[1]==0 and self.color[2]==0:
                self.color=(0,0,0)
                game.players.remove(self)
        else:
            #updates the snake...
            head=self.body[0]#head of snake
            head=(head[0]+self.direction[0],head[1]+self.direction[1])
            #wrap the snake around the window
            headx=game.hortiles if head[0]<0 else 0 if head[0]>game.hortiles else head[0]
            heady=game.verttiles if head[1]<0 else 0 if head[1]>game.verttiles else head[1]
            head=(headx,heady)
            #update the body and see if the snake is dead
            alivelist=[snake for snake in reversed(game.players) if not snake.IsDead]
            for snake in alivelist:
                if head in snake.body:
                    if head == snake.body[0]:#in case of head to head collision, kill both of the snakes
                        snake.IsDead=True
                    self.IsDead=True
                    return
            if head in game.obstacles:#hit an obstacle
                self.IsDead=True
                return
            elif head == game.foodpos:
                #the snake ate the food
                game.foodpos=0,0
                self.body.append((self.body[0]))
            #the snake hasnot collided....move along
            self.body=[head]+[self.body[i-1] for i in range(1,len(self.body))]
    def Draw(self,screen,game):
        for part in self.body:
            pygame.draw.rect(screen,self.color,(part[0]*game.tilesize,part[1]*game.tilesize,game.tilesize,game.tilesize),0)
    def processkey(self,key):
        pass #nothing to do here
    def boundary(self):
        pass

class HumanSnake(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0),upkey=K_UP,downkey=K_DOWN,rightkey=K_RIGHT,leftkey=K_LEFT,color=(0,255,0)):
        super().__init__(body,direction,color,1)#speed is always 1
        #assign the keys to control the human snake
        self.upkey=upkey
        self.downkey=downkey
        self.rightkey=rightkey
        self.leftkey=leftkey
        
    def processkey(self,key):
        #we check the old direction not the new direction.
        if key==self.upkey:
            if self.direction != down:
                self.newdirection=up
        elif key==self.downkey:
            if self.direction != up:
                self.newdirection=down
        elif key==self.rightkey:
            if self.direction != left:
                self.newdirection=right
        elif key==self.leftkey:
            if self.direction != right:
                self.newdirection=left

class ComputerSnake(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0),color=(255,0,0),speed=1):
        super().__init__(body,direction,color,speed)
    def pathlen(self,a,b):
        return int( ((a[0]-b[0])**2 + (a[1]-b[1])**2 )**0.5)
    def add(self,a,b):
        return a[0]+b[0],a[1]+b[1]
    def UpdateDirection(self,game):
        #this is the brain of the snake player
        olddir=self.direction
        position=self.body[0]
        
        #new direction can't be up if current direction is down...and so on
        complement=[(up,down),(down,up),(right,left),(left,right)]
        invaliddir=[x for (x,y) in complement if y==olddir]
        validdir=[dir for dir in directions if not ( dir in invaliddir )]
        
        #get the list of valid directions for us
        validdir=[dir for dir in validdir if not (self.add(position,dir) in game.obstacles or self.add(position,dir) in game.playerpos)]
        #if we collide then set olddir to first move of validdir (if validdir is empty then leave it to olddir)
        olddir= olddir if olddir in validdir or len(validdir)==0 else validdir[0]
        #shortest path.....we assume that the direction we are currently going now gives the shortest path
        shortest=self.pathlen(self.add(position,olddir) , game.foodpos)#length in shortest path
        for dir in validdir:
            newpos=self.add(position,dir)
            newlen=self.pathlen(newpos , game.foodpos)#length in shortest path
            if newlen < shortest:
                if not ( newpos in game.obstacles or newpos in game.playerpos):
                    olddir=dir
                    shortest=newlen
        self.direction=olddir
        
class SnakeGame:
    tilesize=20
    hortiles=60
    verttiles=40
    def __init__(self):
        #create the window and do other stufff
        pygame.init()
        self.screen = pygame.display.set_mode(((self.hortiles+1)*self.tilesize,(self.verttiles+1)*self.tilesize+25))
        pygame.display.set_caption('Python Snake')
        
        #load the font
        self.font = pygame.font.Font(None, 30)
        self.obstacles=[]
        self.obscolor=(0,0,255)
        self.foodcolor=(0,255,255)
        self.foodpos=(0,0)
        self.playercount=0

    def GenerateFood(self):
        if(self.foodpos == (0,0)):
            self.foodpos=random.randrange(1,self.hortiles),random.randrange(1,self.verttiles)
            while (self.foodpos in self.playerpos or self.foodpos in self.obstacles):
                self.foodpos=random.randrange(1,self.hortiles),random.randrange(1,self.verttiles)

    def SetObstacles(self,level):
        for i in range(1,level+1):
            lo=random.randrange(1,self.hortiles),random.randrange(1,self.verttiles) #last obstacle
            self.obstacles.append(lo)
            for j in range(1,random.randint(1,int(level/2))):
                if(random.randint(1,2) == 1):
                    lo=(lo[0]+1,lo[1])
                else:
                    lo=(lo[0],lo[1]+1)
                if( 0<lo[0]<=self.hortiles and 0<lo[1]<=self.verttiles ):
                    self.obstacles.append(lo)
    def setplayers(self,players):
        self.playercount+=len(players)
        self.players=players
    
    def printstatus(self):
        if(len(self.players) >0):
            text = self.font.render(str(len(self.players))+" players playing", 1,(255,255,255))
        else:
            text=self.font.render("All players dead....press c for new computer snake or h for new human snake",1,(255,0,0))
        textpos = text.get_rect(centerx=self.screen.get_width()/2,y=(self.verttiles+1)*self.tilesize)
        self.screen.blit(text, textpos)
    
    def UpdatePlayerInfo(self):
        #update where the players are in the board just before updating the logic
        self.playerpos=[]
        for player in self.players:
            self.playerpos+=player.body
    def start(self):
        # if(not os.path.exists("highscore.txt")):
        #     with open("highscore.txt","w") as f:
        #         f.write("0")
        #         highscore = 0
        # else:
        #     with open("highscore.txt","r") as f:
        #      highscore = f.read()
        clock = pygame.time.Clock()
        count=0

        while True:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit();exit()
                elif event.type == pygame.KEYDOWN:
                    for player in self.players:
                        player.processkey(event.key)
                    if event.key == K_h:
                        pass
                        self.players.append(HumanSnake())
                        self.playercount+=1
                    elif event.key == K_c:
                        pass
                        self.players.append(ComputerSnake())
                        self.playercount+=1
            count+=1
            self.screen.fill((0,0,0))
            #game logic is updated in the code below
            self.UpdatePlayerInfo()
            self.GenerateFood() #generate food if necessary
            for player in [a for a in self.players if not a.IsDead]:
                player.UpdateDirection(self) #update game logic (only for alive players)
            for player in [a for a in self.players if  count%a.speed == 0]:
                player.Update(self)
            #print all the content in the screen
            for player in self.players:
                player.Draw(self.screen,self)
            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen,self.obscolor,(obstacle[0]*self.tilesize,obstacle[1]*self.tilesize,self.tilesize,self.tilesize),0)
            pygame.draw.rect(self.screen,self.foodcolor,(self.foodpos[0]*self.tilesize,self.foodpos[1]*self.tilesize,self.tilesize,self.tilesize),0)
            self.printstatus()
            pygame.display.update()
#start the game
if(__name__ == "__main__"):
    snake=SnakeGame()
    # snake.SetObstacles(10) #level of obstacles
    snake.setplayers([  
    #HumanSnake([(12,14)])
    #,ComputerSnake(),
    #ComputerSnake([(17,14)]*2,up)
    ])
    # welcomescreen()
    snake.start()