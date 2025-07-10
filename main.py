import pygame 
import time
import random
pygame.font.init() # font module 

Width , Height = 1000 , 800 # in px , window ko resolution 
WIN = pygame.display.set_mode((Width,Height)) # making the window 
pygame.display.set_caption("Rain Dodge")

# BG = pygame.image.load(...)

#Constants
player_width = 40
player_height = 60
player_velocity = 5
rain_width = 10
rain_height = 20
rain_vel = 3

#Backgrounds
BG = pygame.image.load("assets/10.png")
BG = pygame.transform.scale(BG , (Width , Height))
# original_img = pygame.image.load("assets/raindrop.png").convert_alpha()
# raindrop_img = pygame.transform.scale(original_img , (12,25))

# FONTS LOAD 
FONT = pygame.font.SysFont("ithaca",30)

def draw(player , elapsed_time , rain_drops , rain_frames):
    # WIN.fill((30, 30, 30))  # Dark gray background
    WIN.blit(BG , (0,0)) # BG , co-ordinate
    
    time_text = FONT.render(f"TIME : {round(elapsed_time)}s",1,"white")
    WIN.blit(time_text,(10,10)) # displaying the font
    
    pygame.draw.rect(WIN , "red", player)
    
    for drop in rain_drops:
        frame = rain_frames[drop["frame"]]
        WIN.blit(frame , (drop["rect"].x , drop["rect"].y))
    
    pygame.display.update()

def load_raindrop_frames(path, num_frames):
    sprite_sheet = pygame.image.load(path).convert_alpha()
    frame_width = sprite_sheet.get_width() // num_frames
    frame_height = sprite_sheet.get_height()

    frames = []
    for i in range(num_frames):
        frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(pygame.transform.scale(frame, (12, 25)))  # Resize if needed
    return frames


def mainGame():  #main game loop 
    
    raindrop_frames = load_raindrop_frames("assets/raindrop_spritesheets.png")
    
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
        
        if rain_count > rain_increment:
            for _ in range(3):
                rain_x = random.randint(0, Width - rain_width)
                drop = {
                    "rect": pygame.Rect(rain_x, -rain_height, rain_width, rain_height),
                    "frame": 0,
                    "timer": 0
                }
                rain_drops.append(drop)
    
            rain_increment = max(200, rain_increment - 50)
            rain_count = 0
        
        # event handling
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