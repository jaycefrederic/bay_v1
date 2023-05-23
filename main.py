from multiprocessing import Value
import pygame
import constants
import levels
import platforms
from player import Player

#trying a new method for the game loop bc the other one wasn't working ):
def main():  # sourcery skip: merge-comparisons
    pygame.init()

    #set the display size & setup the screen
    size = [constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Bay of Verses - v1.01")

    #headman comes in
    player = Player()
    #and the levels
    level_list = [levels.Lvl_01(player)]
    level_list.append(levels.Lvl_01(player))

    current_level_no = 0
    current_level = level_list[current_level_no]
    current_level = levels.Lvl_01(player)

    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(player)

    player.level = current_level
    player.rect.x = 120
    player.rect.y = constants.DISPLAY_HEIGHT - player.rect.height - 200


    done = False

    clock = pygame.time.Clock()

    #dictionary
    key_action = {
        pygame.K_LEFT: player.go_left,
        pygame.K_a: player.go_left,
        pygame.K_RIGHT: player.go_right,
        pygame.K_d: player.go_right,
        pygame.K_w: player.jump,
        pygame.K_SPACE: player.jump,
        pygame.K_ESCAPE: lambda: setattr(done, "value", True),
    }

    while not done:
        for event in pygame.event.get():
            # quitters r losers
            if event.type == pygame.QUIT:
                done = True

            # key calls
            if event.type == pygame.KEYDOWN:
                if action := key_action.get(event.key):
                    action()


            # stop when key stops being pressed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.stop()
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    player.stop()      

        # update player
        active_sprite_list.update()
        #update platforms
        for platform in current_level.platform_list:
            platform.update()
        #update level
        current_level.update()
        #update screen
        current_level.draw(screen)
        for platform in current_level.platform_list:
            platform.draw(screen)
        active_sprite_list.draw(screen)

        # optional reset is   player.rect.y = constants.DISPLAY_HEIGHT - player.rect.height - 200


        #scrolliollio
        #check if player is close to the right border and move screen accordingly
        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.shift_world(-diff)
        #check if player is close to the left border and move screen accordingly
        if player.rect.x <= 50:
            diff = 50 - player.rect.x
            player.rect.x = 50
            current_level.shift_world(diff)

        #update player
        player.update()

        #update platforms again bc plz
        platform.update()


        #fps
        clock.tick(30)

        #update screen
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
