import pygame
import levels
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT_NAME, FONT_COLOR, BLACK, PLATFORM_SPEED, FONT_SIZE


#create a new class for text platforms
  #btw def init means it's initializing the attributes of the object and setting them to their default values thx chatGPT
class Platform(pygame.sprite.Sprite):
    pygame.font.init()
    font = pygame.font.Font(FONT_NAME, FONT_SIZE)
    def __init__(self, x, y, text, is_final):
        super().__init__() #Using `super().__init__()` is a more modular and flexible way to initialize the parent class, as it allows for easier inheritance and customization of the parent class in the future.
        self.x = x
        self.y = y
        self.text = text
        self.text_surface = Platform.font.render(text, True, FONT_COLOR)
        self.text_surface.set_alpha(255)
        
        self.is_final = is_final
        
        self.passenger = None
        #get image
        self.image = pygame.Surface((self.text_surface.get_width(), self.text_surface.get_height()))
        self.image.blit(self.text_surface, (x,y))
        
        #set colorkey (transparent color)
        self.image.set_colorkey(BLACK)
        
        #get rekt my dude
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw(self, screen):
        screen.blit(self.text_surface, self.rect)
    
                
class MovingPlatform(Platform):
    def __init__(self, x, y, text, is_final, y0, y1, x0, x1):
        super().__init__(x, y, text, is_final) # initialize parent class
        
        # initialize boundary variables
        self.top_bound = y0 
        self.bottom_bound = y1 
        self.left_bound = x0 
        self.right_bound = x1 
        
        
       # initialize directions
        if self.top_bound == self.bottom_bound:
            self.direction = (1, 0) # horizontal
            # initialize change in position
            self.change_x = 1
            self.change_y = 0
        elif self.left_bound == self.right_bound:
            self.direction = (0, 1) # vertical
            # initialize change in position
            self.change_x = 0
            self.change_y = 1
        else:
            raise ValueError("MovingPlatform init error must be either horizontal or vertical")
            


        self.passenger = None # initialize passenger
            
    def update(self):
        if self.direction == (1, 0): # if moving horizontally
            if self.rect.x >= self.right_bound or self.rect.x <= self.left_bound: # if at boundary
                self.change_x *= -1 # reverse x direction
            self.rect.x += self.change_x # update platform position
        elif self.direction == (0, 1): # if moving vertically
            if self.rect.y >= self.bottom_bound or self.rect.y <= self.top_bound: # if at boundary
                self.change_y *= -1 # reverse y direction
            self.rect.y += self.change_y # update platform position
        else:
            raise ValueError("MovingPlatform update method error not horizontal or vertical")
    
        # update passenger position
        if self.passenger:
            self.passenger.rect.x += self.change_x
            self.passenger.rect.y += self.change_y 
            

class SlowPlatform(Platform):
    def __init__(self, x, y, text, is_final):
        super().__init__(x, y, text, is_final)

    def update(self):
        if self.passenger:
            self.passenger.velocity.x -= 1
            
class BouncyPlatform(Platform):
    def __init__(self, x, y, text, is_final):
        super().__init__(x, y, text, is_final)
    
    def update(self):
        if self.passenger:
            self.passenger.velocity.y -= 12