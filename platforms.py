import pygame
import levels
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT_NAME, FONT_COLOR, BLACK, PLATFORM_SPEED, FONT_SIZE


#create a new class for text platforms
  #btw def init means it's initializing the attributes of the object and setting them to their default values thx chatGPT
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, text, is_final):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.text_surface = self.font.render(text, True, FONT_COLOR)
        self.text_surface.set_alpha(280)

        self.is_final = is_final

        #get image
        self.image = pygame.Surface((self.text_surface.get_width(), self.text_surface.get_height()))
        self.image.blit(self.text_surface, (x,y))

        #set colorkey (transparent color)
        self.image.set_colorkey(BLACK)

        #get rekt bro
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #regular platforms "aren't" moving lol
        ###self.velocity.x = 0
        ###self.velocity.y = 0


        #now we draw the text onto the screen
    def draw(self, screen):
        screen.blit(self.text_surface, self.rect)

        #alrighty boys let's do some collisions
    def check_collision(self, player):
        if self.rect.colliderect(player.rect):
             #what part of player is touching the platform?
            collision_side = self.rect.collidepoint(player.rect.midbottom)
            if collision_side:
                #lands the player on top of the platform
                player.rect.bottom = self.rect.top
                player.on_ground = True
                
    # this is for when i add more levels
    
        if (
            self.rect.colliderect(player.rect)
            and self.is_final
            and current_level_no < len(levels.level_list) - 1
        ):
            current_level_no += 1
            current_level = levels.level_list[current_level_no]
            player.level = current_level
            player.rect.x = 120
            player.rect.y = DISPLAY_HEIGHT - player.rect.height - 120


    def update(self):
        self.rect.x += 0
        self.rect.y += 0

#slow down platforms
class SlowPlatform(Platform):
    def check_collision(self, player):
        super().check_collision(player)
        if self.rect.colliderect(player.rect):
            player.velocity.x *= 0.2
            player.rect.bottom = self.rect.top
            player.on_ground = True


#lift platforms
class BouncyPlatform(Platform):
    def check_collision(self, player):
        super().check_collision(player)
        if self.rect.colliderect(player.rect):
            player.rect.bottom = self.rect.top
            player.on_ground = True
            player.velocity.y = -10        

#next let's talk about moving platforms
# This is a class for creating a moving platform in a game with a text label on it

class MovingPlatform(pygame.sprite.Sprite):
    
    def __init__(self, x, y, text, velocity, start, end):
        super().__init__()
        self.x = x
        self.y = y
        self.text = text
        
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.text_surface = self.font.render(text, True, FONT_COLOR)
        self.text_surface.set_alpha(255)

        # Create the platform surface
        self.image = pygame.Surface((self.text_surface.get_width(), self.text_surface.get_height()))
        self.image.blit(self.text_surface, (0, 0))
        
        # set color key
        self.image.set_colorkey(BLACK)
        
        # Initialize the position and movement vectors
        self.position = pygame.math.Vector2(x, y)
        self.velocity = velocity      
          
        # get rect
        self.rect = self.image.get_rect(topleft=self.position)
        self.rect.x = x
        self.rect.y = y
        
        # start and end positions
        self.start = pygame.math.Vector2(start)
        self.end = pygame.math.Vector2(end)
        
        # Calculate the initial direction based on start and end positions
        self.direction = (self.end - self.start).normalize()
        
        # store a passenger
        self.passenger = None
        
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, player):  # sourcery skip: use-named-expression
        if self.rect.colliderect(player.rect):
            # what part of player is touching the platform?
            # walrus operator `:=` assigns the result of `self.rect.collidepoint(player.rect.midbottom)` to the variable `collision_side` and also checking if the result is truthy (i.e. if the player's midbottom point is colliding with the platform); checking for collision and getting the collision side at the same time.
            collision_side = self.rect.collidepoint(player.rect.midbottom)
            if collision_side:
                #lands the player on top of the platform
                player.rect.bottom = self.rect.top
                player.on_ground = True
                self.passenger = player

    
    def update(self):
        # Update the position based on velocity
        self.position += pygame.math.Vector2(*self.velocity)

        # If the platform has reached its end position, reverse direction
        if self.position.distance_to(pygame.math.Vector2(*self.end)) < PLATFORM_SPEED:
            self.velocity *= -1

        # Round the position to integer values and update the rect
        self.rect.topleft = self.position
        
        # move the passenger with the platform
        if self.passenger is not None:
            self.passenger.rect.x += self.velocity.x
            self.passenger.rect.y += self.velocity.y