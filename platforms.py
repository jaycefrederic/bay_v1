import pygame
import levels
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT_NAME, FONT_COLOR, BLACK, PLATFORM_SPEED, FONT_SIZE


#create a new class for text platforms
  #btw def init means it's initializing the attributes of the object and setting them to their default values thx chatGPT
class Platform(pygame.sprite.Sprite):
    font = pygame.font.Font(FONT_NAME, FONT_SIZE)
    def __init__(self, x, y, text, is_final):
        super().__init__() #Using `super().__init__()` is a more modular and flexible way to initialize the parent class, as it allows for easier inheritance and customization of the parent class in the future.
        self.x = x
        self.y = y
        self.text = text
        self.text_surface = Platform.font.render(text, True, FONT_COLOR)
        self.text_surface.set_alpha(255)
        
        self.is_final = is_final
        
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
    
    def handle_collision(self, player):
            #lands the player on top of the platform
            player.rect.bottom = self.rect.top
            player.on_ground = True
            if issubclass(self, MovingPlatform) or issubclass(self, SlowPlatform) or issubclass(self, BouncyPlatform):
                self.passenger = player
        
    def check_collision(self, player):  # sourcery skip: use-named-expression
        if self.rect.colliderect(player.rect):
            #what part of player is touching the platform?
            collision_side = self.rect.collidepoint(player.rect.midbottom)
            if collision_side:
                self.handle_collision(player)
                
class MovingPlatform(Platform):
    def __init__(self, x, y, text, is_final, velocity, start, end):
        super().__init__(x, y, text, is_final)
        self.velocity = velocity
        self.passenger = None
        #start and end points
        self.start = start
        self.end = end
        #use start and end points to determine direction
        self.direction.x = 1 if self.end.x > self.start.x else -1
        self.direction.y = 1 if self.end.y > self.start.y else -1
        
    def update(self):
        #move the platform
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        #check if the platform has reached the end
        if abs(self.rect.x > self.end.x) or abs(self.rect.x < self.start.x):
            self.velocity.x *= -1
        if abs(self.rect.y > self.end.y) or abs(self.rect.y < self.start.y):
            self.velocity.y *= -1
        #move the passenger with the platform
        if self.passenger:
            self.passenger.rect.x += self.velocity.x
            self.passenger.rect.y += self.velocity.y

class SlowPlatform(Platform):
    def __init__(self, x, y, text, is_final):
        super().__init__(x, y, text, is_final)
    
    def update(self):
        if self.passenger:
            self.passenger.velocity.x += -1
            
class BouncyPlatform(Platform):
    def __init__(self, x, y, text, is_final):
        super().__init__(x, y, text, is_final)
    
    def update(self):
        if self.passenger:
            self.passenger.velocity.y += -8