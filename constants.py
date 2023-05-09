""" constants (^: """
import pygame

#i copied this file from the old game but we're going to change some things

#set the display size
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# don't need a camera
# since we're making the world "move" and keeping the player "still"
#uh maybe i can incorporate a camera this time

#define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
lightgray = (200,200,200)
mediumgray = (100,100,100)
darkgray = (50,50,50)
red = (255,0,0)
BLUE = (0,0,225)
yellow = (255,255,0)
green = (0,255,0)
cyan = (0,255,255)
purple = (255,0,255)

#now let's load a font
FONT_NAME = "fonts/long-cang.ttf"
FONT_COLOR = WHITE
FONT_SIZE = 20

#gravity is important
GRAVITY = 0.5
JUMP_SPEED = -10

#platform speed i guess
PLATFORM_SPEED = 1