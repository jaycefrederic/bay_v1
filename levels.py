import pygame
import player
import sys
from platforms import Platform, MovingPlatform, SlowPlatform, BouncyPlatform
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, WHITE, BLACK

class Level():
    #superclass for all levels, baby classes for each level

    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.moving_platform_group = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.background = None
        self.level_limit = -9200
        self.world_shift = 0
    
    def update(self):
        self.platform_list.update()
        self.moving_platform_group.update()
        self.enemy_list.update()

    def draw(self, screen):
        #blit blit blit i still don't know what that means
        #bg scrolls less than headman moves
        screen.blit(self.background, (self.world_shift // 3,0))
        #platforms
        self.platform_list.draw(screen)
        self.moving_platform_group.draw(screen)
        #enemies, whenever we get around to adding that
        self.enemy_list.draw(screen)
        #update each platform before calling shift_world method
        for platform in self.platform_list:
            platform.update()
        for moving_platform in self.moving_platform_group:
            moving_platform.update()
        self.shift_world(self.world_shift)

    def create_level(self, level):
        #creating a block/collision for each platform in the level
        for platform in level:
        #Platform(x, y, text)
            if platform[3] == 'Platform':
                block = Platform(platform[0], platform[1], platform[2])
            elif platform[3] == 'MovingPlatform':
                block = MovingPlatform(platform[0], platform[1], platform[2], platform[4], platform[5], platform[6])
            elif platform[3] == 'SlowPlatform':
                block = SlowPlatform(platform[0], platform[1], platform[2])
            elif platform[3] == 'BouncyPlatform':
                block = BouncyPlatform(platform[0], platform[1], platform[2])
            ###block.player = self.player
            #add the platform in there
            self.platform_list.add(block)
    
    def check_collisions(self):
        #idk how this one really works tbh
        for platform in self.platform_list:
            platform.check_collision(self.player)
        for moving_platform in self.moving_platform_group:
            moving_platform.check_collision(self.player)

    def shift_world(self, shift_x):
        # bc it's actually a side-scroller, we're scrollin
        self.world_shift += (shift_x*0.6) # keep track of world shift
        # adjusting platform and enemy sprite lists to match the scroll
        for platform in self.platform_list:
            platform.rect.x += (shift_x*0.6)
            platform.rect.move_ip((shift_x*0.6), 0)
            platform.update()
            #if isinstance(platform, MovingPlatform):
            #     MovingPlatform.update(platform)
            #elif isinstance(platform, Platform):
            #    Platform.update(platform)

        #reset the world shift so it doesn't infintitely snowball and cause an error
        self.world_shift = 0
        ###for enemy in self.enemy_list:
            ###enemy.rect = enemy.rect.move(shift_x, 0)


class Lvl_01(Level):
    
    def __init__(self, player):
        Level.__init__(self, player)

        self.background = pygame.image.load("bg.png").convert()
        self.background.set_colorkey(BLACK)
        self.level_limit = -4200

        self.platform_list = pygame.sprite.Group() #create a sprite group to hold platforms
        self.moving_platform_group = pygame.sprite.Group()

        level = [
            Platform(4, 580, "i keep waking up here...", False),
            Platform(265, 565, "with every step i feel the echo of", False),
            SlowPlatform(500, 565, "what i once wrote", False),
            Platform(800, 560, ".....", False),
            Platform(860, 530, ".....", False),
            BouncyPlatform(910, 500, ".....", False),
            Platform(1010, 400, "much of it belonged to me", False),
            Platform(1260, 550, "but some of it was the work of my idols.", False),
            MovingPlatform(1645, 550, ".....", [1,0], [1645,550], [1870,550]),
            Platform(1900, 550, "poets, mainly. i always wanted to be a poet.", False),
            MovingPlatform(2335, 550, "i'm not sure", [0, 1], [2335,550], [2335,405]),
            Platform(2455, 405, "if i ever was", False),
            MovingPlatform(2605, 405, ".....", [1, 0], [2605,405], [2890,405]),
            Platform(2915, 370, "i'm not sure what became of me at all", False),
            BouncyPlatform(3310, 320, "am i really here?", False),
            MovingPlatform(3520, 480, "was i ever really here?", [1, 0], [3520,480], [4685,480]),
            Platform(4900, 580, "next----->", True)
        ]

        #add each platform to platform_list
        for platform in level:
            self.platform_list.add(platform)
        for moving_platform in level:
            self.moving_platform_group.add(moving_platform)
            