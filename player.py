import pygame
import constants
from platforms import MovingPlatform

""" player class. in its own file. headman likes his privacy. """

#resurrecting headman 
    # but let's copy the way i did it before because that seemed to work
class Player(pygame.sprite.Sprite):
    
    walking_frames_l = []
    walking_frames_r = []

    direction = "R"

    level = None

    def __init__(self):
        self.velocity = pygame.math.Vector2(0, 0)
        # separate rect for collision detection
        self.rect = pygame.Rect(0, 0, 40, 64)
        pygame.sprite.Sprite.__init__(self)

        # right facing imgs in this block
        sprite_sheet = pygame.image.load("headman.png")
        image = sprite_sheet.subsurface(pygame.Rect(40,64,40,64))
        self.walking_frames_r.append(image)
        image = sprite_sheet.subsurface(pygame.Rect(0,64,40,64))
        self.walking_frames_r.append(image)
        image = sprite_sheet.subsurface(pygame.Rect(40,0,40,64))
        self.walking_frames_r.append(image)
        image = sprite_sheet.subsurface(pygame.Rect(0,0,40,64))
        self.walking_frames_r.append(image)

        # flipping to left in this block
        image = sprite_sheet.subsurface(pygame.Rect(40,64,40,64))
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.subsurface(pygame.Rect(0,64,40,64))
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.subsurface(pygame.Rect(40,0,40,64))
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.subsurface(pygame.Rect(0,0,40,64))
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()
        # phew
        
    def update(self):
        #fuck velocity. here's gravity
        # Apply gravity to the player's y velocity
        self.velocity.y += 0.2

        # Update the player's position based on its velocity
        self.rect.move_ip(self.velocity)
        
        self.handle_platform_collision()

        # Keep the player from falling through the bottom of the screen
        if self.rect.bottom > constants.DISPLAY_HEIGHT:
            self.rect.bottom = constants.DISPLAY_HEIGHT
            self.velocity.y = 0
        
        # Update the player's image based on its direction
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 24) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 24) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        
        """
        
            if isinstance(block, Credit):
                
                
        """
    # handle platform collisions
    def handle_platform_collision(self):  # sourcery skip: min-max-identity
        # reset on_platform flag
        self.on_platform = False
        for platform in self.level.platform_list:
            if self.rect.colliderect(platform.rect):
                # top and bottom collision
                if self.velocity.y > 0 and self.rect.bottom <= platform.rect.top + 10:
                    # Player is falling and colliding with the top of the platform
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.on_platform = True
                elif self.velocity.y < 0 and self.rect.top >= platform.rect.bottom - 10:
                    # Player is jumping and colliding with the bottom of the platform
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0
                # left and right collision
                    # if player is to the right of the platform
                elif self.velocity.x <= 0 and self.rect.left >= platform.rect.right - 10:
                    # set the player's x position to be to the right of the platform
                    self.rect.left = platform.rect.right
                    # if player is to the left of the platform
                elif self.velocity.x >= 0 and self.rect.right <= platform.rect.left + 10:
                    # set the player's x position to be to the right of the platform
                    self.rect.right = platform.rect.left
                else: self.on_platform = False        
                
                # handle moving platform collisions
                if isinstance(platform, MovingPlatform):
                    platform.passenger = self
                    self.on_platform = True
        
    #movements here
    def jump(self):
        # Check collision with platforms
        if self.on_platform or self.rect.bottom >= constants.DISPLAY_HEIGHT:
            self.velocity.y = -7

    def go_left(self):
        self.velocity.x = -3
        self.direction = "L"

    def go_right(self):
        self.velocity.x = 3
        self.direction = "R"

    def stop(self):
        self.velocity.x = 0