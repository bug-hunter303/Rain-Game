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
rain_width = 10
rain_height = 20
rain_vel = 3
BG = pygame.image.load("Assests/10.png")
BG = pygame.transform.scale(BG , (Width , Height))
original_img = pygame.image.load("Assests/raindrop.png").convert_alpha()
raindrop_img = pygame.transform.scale(original_img , (12,20))


FONT = pygame.font.SysFont("ithaca",30)

def draw(player , elapsed_time , rain):
    WIN.fill((30, 30, 30))  # Dark gray background
    # WIN.blit(BG , (0,0)) # BG , co-ordinate
    
    time_text = FONT.render(f"TIME : {round(elapsed_time)}s",1,"white")
    WIN.blit(time_text,(10,10)) # displaying the font
    
    pygame.draw.rect(WIN , "red", player)
    
    for drop in rain:
        WIN.blit(raindrop_img , (drop.x,drop.y))
    
    pygame.display.update()

def mainGame():
    run = True
    hit = False
    
    player = pygame.Rect(200 , Height-player_height , player_width , player_height) # x , y , width , height
    
    clock = pygame.time.Clock()
    
    start_time = time.time()
    elapsed_time = 0
    
    rain_increment = 2000 # in millisec
    rain_count = 0 
    
    rain_drops = []
    
    while run:
        rain_count += clock.tick(60) # fps = 60
        elapsed_time = time.time() - start_time
        
        if rain_count > rain_increment:  # generating the rain 
            for _ in range(3):
                rain_x = random.randint(0, Width - rain_width) # random integer to add the drops for the rain
                new_drop = pygame.Rect(rain_x, - rain_height, rain_width , rain_height)  # starts at the top of the screen and moves down 
                rain_drops.append(new_drop)

            rain_increment = max(200 , rain_increment - 50 )
            rain_count = 0
        
        for event in pygame.event.get(): #pygame.event.get = contains all the events that can be pressed
            if event.type == pygame.QUIT:
                run = False
                break
          
        keys = pygame.key.get_pressed() # player movement
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (player.x - player_velocity >=0): # x co-ordinate greater than 0 than we can't move out of the screen
            player.x -= player_velocity   # moving left to (0,0)
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and (player.x + player_velocity + player_width<= Width):
            player.x += player_velocity  # moving right to (1000,0)   
            
        for drop in rain_drops[:]:
            drop.y += rain_vel
            if drop.y > Height:
                rain_drops.remove(drop)
            elif drop.y + drop.height >= player.y and drop.colliderect(player):
                run = False
                hit = True
                break
        
        if hit:
            lost_text = FONT.render("YOU LOST",True,"white")
            WIN.blit(lost_text , (Width/2 - lost_text.get_width()/2 , Height/2 - lost_text.get_height()/2))
            pygame.display.update()
            
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                        waiting = False 
             
        draw(player , elapsed_time , rain_drops)
        
    pygame.quit()
    
if __name__ == "__main__":
    mainGame() 