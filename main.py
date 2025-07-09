import pygame 
import time
import random
pygame.font.init() # font module 

Width , Height = 1000 , 800 # in px , window ko resolution 
WIN = pygame.display.set_mode((Width,Height)) # making the window 
pygame.display.set_caption("Rain Dodge")

# BG = pygame.image.load(...)

player_width = 40
player_height = 60
player_velocity = 5

FONT = pygame.font.SysFont("ithaca",30)

def draw(player , elapsed_time):
    WIN.fill((30, 30, 30))  # Dark gray background
    # WIN.blit() # BG , co-ordinate
    
    time_text = FONT.render(f"TIME : {round(elapsed_time)}s",1,"white")
    WIN.blit(time_text,(10,10)) # displaying the font
    
    pygame.draw.rect(WIN , "red", player)
    
    pygame.display.update()

def mainGame():
    run = True
    
    player = pygame.Rect(200 , Height-player_height , player_width , player_height) # x , y , width , height
    
    clock = pygame.time.Clock()
    
    start_time = time.time()
    elapsed_time = 0
    
    rain_increment = 2000 # in millisec
    rain_count = 0 
    
    while run:
        clock.tick(60) # fps = 120
        elapsed_time = time.time() - start_time
        
        for event in pygame.event.get(): #pygame.event.get = contains all the events that can be pressed
            if event.type == pygame.QUIT:
                run = False
                break
          
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (player.x - player_velocity >=0): # x co-ordinate greater than 0 than we can't move out of the screen
            player.x -= player_velocity   # moving left to (0,0)
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and (player.x + player_velocity + player_width<= Width):
            player.x += player_velocity  # moving right to (1000,0)   
                   
        draw(player , elapsed_time)
        
    pygame.quit()
    
if __name__ == "__main__":
    mainGame() 