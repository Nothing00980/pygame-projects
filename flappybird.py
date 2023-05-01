from pickle import TRUE
import pygame
# making a game in python using pygame module

x = pygame.init()
# print(x)
# makes a window for pygame
gamewindow = pygame.display.set_mode((1200,500))
# title
pygame.display.set_caption("Flappy Bird")



# ----------game specific variables
# for quiting game
exit_game = False
# when game is over
game_over = False

# creating a game loop -- game is always a loop of windows
while not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # quit functoin or keyword setting up
            exit_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                print("you have pressed the right arrow key")
        # print(event) # printing all the events being done

pygame.quit()
quit()
