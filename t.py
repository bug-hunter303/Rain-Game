import pygame 
import time
import random

Width , Height = 1000 , 800 # in px , window ko resolution 
WIN = pygame.display.set_mode((Width,Height)) # making the window 
pygame.display.set_caption("Rain Dodge")

def mainGame():
    run = True
    
    while run:
        for event in pygame.event.get(): #pygame.event.get = contains all the events that can be pressed
            if event.type == pygame.QUIT:
                run = False
                break
            
    pygame.quit()
    
if __name__ == "__main__":
    mainGame() 