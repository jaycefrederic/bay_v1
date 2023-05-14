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
            elif player.rect.colliderect(self.rect):
                self.handle_collision(player)
                
class MovingPlatform(Platform):
    def __init__(self, x, y, text, is_final, start, end):
        super().__init__(x, y, text, is_final)
        #self.velocity = pygame.math.Vector2(velocity)

        # start and end points
        self.start = start
        self.end = end
        self.direction = pygame.math.Vector2(self.end[0] - self.start[0], self.end[1] - self.start[1]).normalize() # initialize direction vector
        
        # initialize tweening variables
        self.starting_pos = pygame.math.Vector2(self.start[0], self.start[1])
        self.ending_pos = pygame.math.Vector2(self.end[0], self.end[1])
        self.current_pos = self.starting_pos # initialize current position
        
        self.distance = self.starting_pos - self.ending_pos # initialize distance

            
    def update(self): # use tweening to move the platform
        # update distance
        self.distance = self.current_pos.distance_to(self.ending_pos)
        # move platform according to distance/direction
        if self.distance != 0:
            self.current_pos += self.direction * PLATFORM_SPEED
        else: # if distance = 0 we reach end of path and reverse
            self.direction *= -1
            self.distance = self.starting_pos.distance_to(self.ending_pos)
        # update distance
        
        
        # update platform position
        self.rect.x = self.current_pos.x
        self.rect.y = self.current_pos.y
        
        # update passenger position
        if self.passenger:
            self.passenger.rect.bottom = self.rect.top
            self.passenger.rect.x = self.current_pos.x
            #self.passenger.rect.x += self.velocity.x
            #self.passenger.rect.y += self.velocity.y

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