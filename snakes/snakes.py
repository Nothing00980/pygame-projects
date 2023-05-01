from cv2 import blur
import pygame
import random
import os

# music
pygame.mixer.init()

pygame.init()
left=-1,0
right=1,0
up=0,-1
down=0,1
directions=[up,down,right,left]
# colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
green = (0,255,0)
s_height = 600
screen_width = 900

# making a window
gamewindow = pygame.display.set_mode((screen_width,s_height))

# background image
bg_img = pygame.image.load('snake.jpg')
bg_img = pygame.transform.scale(bg_img,(screen_width,s_height)).convert_alpha() # because of convert alpha gamescreen will not be affected
# basically update the screen number of times per second
clock = pygame.time.Clock()
# printing text on the screen
font = pygame.font.SysFont(None,55)
def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gamewindow.blit(screen_text,[x,y])

# function for plotting snake and increasing of it
def plot_snake(gamewindow,color,snake_list,snake_size):
    for x,y in  snake_list:
        # print(snake_list)
        pygame.draw.rect(gamewindow,color,[x,y,snake_size,snake_size])

# welcome screen
def welcomescreen():
    exit_game = False
    while not exit_game:
        gamewindow.fill(black)
        gamewindow.blit(bg_img,(0,0))
        text_screen("Welcome to Snakes",green,250,260)

        text_screen("press c for computer or h for human to Play",red,100,350)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    gameloop()
                elif event.key == pygame.K_c:
                    gameloopcomputer()
             
        
        pygame.display.update()
        clock.tick(60)

# class Snake:
#     def __init__(self,body , direction, color,speed):
#         self.speed=speed
#         self.body=body #initially located here
#         self.color=color
#         self.direction=self.newdirection=direction
#         self.IsDead=False
#     def UpdateDirection(self,game):
#         self.direction=self.newdirection #the next direction is stored in newdirection....logic is updated here
#     def Update(self,game):
#         if self.IsDead:
#             fadestep=5
#             self.color=(max(self.color[0]-fadestep,0),max(self.color[1]-fadestep,0),max(self.color[2]-fadestep,0))
#             if self.color[0]==0 and self.color[1]==0 and self.color[2]==0:
#                 self.color=(0,0,0)
#                 game.players.remove(self)
#         else:
#             #updates the snake...
#             head=self.body[0]#head of snake
#             head=(head[0]+self.direction[0],head[1]+self.direction[1])
#             #wrap the snake around the window
#             headx=game.hortiles if head[0]<0 else 0 if head[0]>game.hortiles else head[0]
#             heady=game.verttiles if head[1]<0 else 0 if head[1]>game.verttiles else head[1]
#             head=(headx,heady)
#             #update the body and see if the snake is dead
#             alivelist=[snake for snake in reversed(game.players) if not snake.IsDead]
#             for snake in alivelist:
#                 if head in snake.body:
#                     if head == snake.body[0]:#in case of head to head collision, kill both of the snakes
#                         snake.IsDead=True
#                     self.IsDead=True
#                     return
#             if head in game.obstacles:#hit an obstacle
#                 self.IsDead=True
#                 return
#             elif head == game.foodpos:
#                 #the snake ate the food
#                 game.foodpos=0,0
#                 self.body.append((self.body[0]))
#             #the snake hasnot collided....move along
#             self.body=[head]+[self.body[i-1] for i in range(1,len(self.body))]
#     def Draw(self,screen,game):
#         for part in self.body:
#             pygame.draw.rect(screen,self.color,(part[0]*game.tilesize,part[1]*game.tilesize,game.tilesize,game.tilesize),0)
#     def processkey(self,key):
#         pass #nothing to do here



# class ComputerSnake(Snake):
#     def __init__(self,body=[(0,0)] , direction=(1,0),color=(255,0,0),speed=1):
#         super().__init__(body,direction,color,speed)
#     def pathlen(self,a,b):
#         return int( ((a[0]-b[0])**2 + (a[1]-b[1])**2 )**0.5)
#     def add(self,a,b):
#         return a[0]+b[0],a[1]+b[1]
#     def UpdateDirection(self,game):
#         #this is the brain of the snake player
#         olddir=self.direction
#         position=self.body[0]
        
#         #new direction can't be up if current direction is down...and so on
#         complement=[(up,down),(down,up),(right,left),(left,right)]
#         invaliddir=[x for (x,y) in complement if y==olddir]
#         validdir=[dir for dir in directions if not ( dir in invaliddir )]
        
#         #get the list of valid directions for us
#         validdir=[dir for dir in validdir if not (self.add(position,dir) in game.obstacles or self.add(position,dir) in game.playerpos)]
#         #if we collide then set olddir to first move of validdir (if validdir is empty then leave it to olddir)
#         olddir= olddir if olddir in validdir or len(validdir)==0 else validdir[0]
#         #shortest path.....we assume that the direction we are currently going now gives the shortest path
#         shortest=self.pathlen(self.add(position,olddir) , game.foodpos)#length in shortest path
#         for dir in validdir:
#             newpos=self.add(position,dir)
#             newlen=self.pathlen(newpos , game.foodpos)#length in shortest path
#             if newlen < shortest:
#                 if not ( newpos in game.obstacles or newpos in game.playerpos):
#                     olddir=dir
#                     shortest=newlen
#         self.direction=olddir











# pygame inbuit function for window heading.
pygame.display.set_caption("snakes")
pygame.display.update()



# loop
def gameloop():
    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play()
    snake_list = []
    snk_length = 1
    exit_game = False
    game_over = False
    snake_x  =100
    snake_y = 100
    snake_size = 10
    score = 0

    # check if highscore file exist
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0")
            highscore = 0
    else:
        with open("highscore.txt","r") as f:
             highscore = f.read()

    foody = random.randint(0,s_height/2)
    foodx = random.randint(0,screen_width/2)

    velocityx = 0
    velocityy = 0
    fps = 30
    while not exit_game:
        if game_over:
            with open("hughscore.txt","w") as f:
                f.write(str(highscore))
            gamewindow.fill(black)
            text_screen("Your score :"+ str(score)+ "  Highscore:"+str(highscore),red,5,5)

            
            text_screen("Game over press h to continue as human or c as computer",red,screen_width/6,s_height/2.5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # quit functoin or keyword setting up
                    exit_game = True 
            #     elif event.type == pygame.KEYDOWN:
            #         for player in self.players:
            #             player.processkey(event.key)
            #         if event.key == K_h:
            #             pass
            #             self.players.append(HumanSnake())
            #             self.playercount+=1
            #         elif event.key == K_c:
            #             pass
            #             self.players.append(ComputerSnake())
            #             self.playercount+=1
            # count+=1
            # self.screen.fill((0,0,0))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        gameloop()
                    elif event.key == pygame.K_c:
                        gameloopcomputer()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # quit functoin or keyword setting up
                    exit_game = True 
                # humanoid or computer based.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        velocityx = -10
                        velocityy = 0
                        if event.key == pygame.K_RIGHT:
                            pass
                        else:
                            if event.key == pygame.K_UP:
                                velocityy = -10
                                velocityx = 0
                            if event.key == pygame.K_DOWN:
                                velocityy = 10
                                velocityx = 0
                    if event.key == pygame.K_DOWN:
                        velocityy = 10
                        velocityx = 0
                        if event.key == pygame.K_UP:
                            pass
                        else:
                            if event.key == pygame.K_RIGHT:
                                velocityx = 10
                                velocityy = 0
                            if event.key == pygame.K_LEFT:
                                velocityx = -10
                                velocityy = 0
                    if event.key == pygame.K_UP:
                        velocityy = -10
                        velocityx = 0
                        if event.key == pygame.K_DOWN:
                            pass
                        else:
                            if event.key == pygame.K_RIGHT:
                                velocityx = 10
                                velocityy = 0
                            if event.key == pygame.K_LEFT:
                                velocityx = -10
                                velocityy = 0
                    if event.key == pygame.K_RIGHT:
                        velocityx = 10
                        velocityy = 0
                        if event.key == pygame.K_LEFT:
                            pass
                        else:
                            if event.key == pygame.K_UP:
                                velocityy = -10
                                velocityx = 0
                            if event.key == pygame.K_DOWN:
                                velocityy = 10
                                velocityx = 0
                                    
    
              
                        
                            # cheat codes
                            if event.key == pygame.K_q:
                                score+=10
            # if snake_x == snake_x - velocityx:
            snake_x = snake_x + velocityx
            snake_y = snake_y + velocityy
            if abs(snake_x - foodx)<6 and abs(snake_y - foody)<6:
                # pygame.mixer.music.load('hiss.mp3')
                # pygame.mixer.music.play()
                score +=10
                # print("score = ",score*10)
                foody = random.randint(0,s_height/2)
                foodx = random.randint(0,screen_width/2)
                snk_length +=2
                if score>int(highscore):
                    highscore = score



                
            gamewindow.fill(black)
            text_screen("score :"+ str(score) + "  Highscore:" + str(highscore),red,5,5)

            pygame.draw.rect(gamewindow,red,[foodx,foody,snake_size,snake_size])
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            if len(snake_list)>snk_length:
                del snake_list[0]
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>s_height:
                game_over = True
                pygame.mixer.music.load('explode.mp3')
                pygame.mixer.music.play()
            if head in snake_list[:-1]: # it icludes all the element except last elements-- it is a method of slicing
                game_over = True
                pygame.mixer.music.load('explode.mp3')
                pygame.mixer.music.play()
                # print("Game over")
            # pygame.draw.rect(gamewindow,black,[snake_x,snake_y,snake_size,snake_size])
            plot_snake(gamewindow,green,snake_list,snake_size)

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

def gameloopcomputer():
    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play()
    snake_list = []
    snk_length = 1
    exit_game = False
    game_over = False
    snake_x  =100
    snake_y = 100
    snake_size = 10
    score = 0

    # check if highscore file exist
    if(not os.path.exists("hughscore.txt")):
        with open("hughscore.txt","w") as f:
            f.write("0")
            highscore = 0
    else:
        with open("hughscore.txt","r") as f:
             highscore = f.read()

    foody = random.randint(0,s_height/2)
    foodx = random.randint(0,screen_width/2)

    velocityx = 0
    velocityy = 0
    fps = 30
    while not exit_game:
        if game_over:
            with open("hughscore.txt","w") as f:
                f.write(str(highscore))
            gamewindow.fill(black)
            text_screen("Your score :"+ str(score)+ "  Highscore:"+str(highscore),red,5,5)

            
            text_screen("Game over press  c to continue as computer or h as human",red,screen_width/6,s_height/2.5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # quit functoin or keyword setting up
                    exit_game = True 
            #     elif event.type == pygame.KEYDOWN:
            #         for player in self.players:
            #             player.processkey(event.key)
            #         if event.key == K_h:
            #             pass
            #             self.players.append(HumanSnake())
            #             self.playercount+=1
            #         elif event.key == K_c:
            #             pass
            #             self.players.append(ComputerSnake())
            #             self.playercount+=1
            # count+=1
            # self.screen.fill((0,0,0))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        gameloop()
                    elif event.key == pygame.K_c:
                        gameloopcomputer()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT: # quit functoin or keyword setting up
                    exit_game = True 
                else:
                    while snake_x != foodx:
                        velocityx = foodx - snake_x
                    while snake_y != foody:
                        velocityy = foody-snake_y

                # humanoid or computer based.

                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_LEFT:
                #         velocityx = -10
                #         velocityy = 0
                #         if event.key == pygame.K_RIGHT:
                #             pass
                #         else:
                #             if event.key == pygame.K_UP:
                #                 velocityy = -10
                #                 velocityx = 0
                #             if event.key == pygame.K_DOWN:
                #                 velocityy = 10
                #                 velocityx = 0
                #     if event.key == pygame.K_DOWN:
                #         velocityy = 10
                #         velocityx = 0
                #         if event.key == pygame.K_UP:
                #             pass
                #         else:
                #             if event.key == pygame.K_RIGHT:
                #                 velocityx = 10
                #                 velocityy = 0
                #             if event.key == pygame.K_LEFT:
                #                 velocityx = -10
                #                 velocityy = 0
                #     if event.key == pygame.K_UP:
                #         velocityy = -10
                #         velocityx = 0
                #         if event.key == pygame.K_DOWN:
                #             pass
                #         else:
                #             if event.key == pygame.K_RIGHT:
                #                 velocityx = 10
                #                 velocityy = 0
                #             if event.key == pygame.K_LEFT:
                #                 velocityx = -10
                #                 velocityy = 0
                #     if event.key == pygame.K_RIGHT:
                #         velocityx = 10
                #         velocityy = 0
                #         if event.key == pygame.K_LEFT:
                #             pass
                #         else:
                #             if event.key == pygame.K_UP:
                #                 velocityy = -10
                #                 velocityx = 0
                #             if event.key == pygame.K_DOWN:
                #                 velocityy = 10
                #                 velocityx = 0
                                    
    
              
                        
                            # # cheat codes
                            # if event.key == pygame.K_q:
                            #     score+=10
            # if snake_x == snake_x - velocityx:
            snake_x = snake_x + velocityx
            snake_y = snake_y + velocityy
            if abs(snake_x - foodx)<6 and abs(snake_y - foody)<6:
                # pygame.mixer.music.load('hiss.mp3')
                # pygame.mixer.music.play()
                score +=10
                # print("score = ",score*10)
                foody = random.randint(0,s_height/2)
                foodx = random.randint(0,screen_width/2)
                snk_length +=2
                if score>int(highscore):
                    highscore = score



                
            gamewindow.fill(black)
            text_screen("score :"+ str(score) + "  Highscore:" + str(highscore),red,5,5)

            pygame.draw.rect(gamewindow,red,[foodx,foody,snake_size,snake_size])
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            if len(snake_list)>snk_length:
                del snake_list[0]
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>s_height:
                game_over = True
                pygame.mixer.music.load('explode.mp3')
                pygame.mixer.music.play()
            if head in snake_list[:-1]: # it icludes all the element except last elements-- it is a method of slicing
                game_over = True
                pygame.mixer.music.load('explode.mp3')
                pygame.mixer.music.play()
                # print("Game over")
            # pygame.draw.rect(gamewindow,black,[snake_x,snake_y,snake_size,snake_size])
            plot_snake(gamewindow,green,snake_list,snake_size)

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()

welcomescreen()