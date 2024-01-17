import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from pygame.locals import *
from screeninfo import get_monitors

pygame.init()

screen = None
clock = None
scale = 1
key_states = {}
FPS = 60

class Spritesheet:
    def __init__(self, sprite:str, sprite_width:int=8, sprite_height:int=8):
        self.sprite = pygame.image.load(sprite)
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.sprites_per_row = self.sprite.get_width() // sprite_width
        self.sprites = self.cache_sprites()

    def cache_sprites(self):
        sprites = []
        for index in range(self.sprites_per_row * (self.sprite.get_height() // self.sprite_height)):
            row = index // self.sprites_per_row
            col = index % self.sprites_per_row
            x = col * self.sprite_width
            y = row * self.sprite_height
            sprite = self.sprite.subsurface(pygame.Rect(x, y, self.sprite_width, self.sprite_height))
            sprites.append(sprite)
        return sprites

    def spr(self, x, y, index):
        sprite = self.sprites[index]
        sprite = pygame.transform.scale(sprite, (sprite.get_width() * scale, sprite.get_height() * scale))
        screen.blit(sprite, (x*scale, y*scale))

def run(update_function, title:str="boopy", icon:str=None, screen_width:int=128, screen_height:int=128, scaling:int=1, fullscreen:bool=False):
    global screen, clock, scale

    scale = scaling

    # Set up the display
    pygame.display.set_caption(title)
    if icon:
        pygame.display.set_icon(pygame.image.load(icon))
    if fullscreen:
        width = get_monitors()[0].width
        height = get_monitors()[0].height
        scale = int(height/screen_height)
        screen = pygame.display.set_mode((screen_width * scale, screen_height * scale),pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen_width * scale, screen_height * scale))

    # Set up the clock
    clock = pygame.time.Clock()

    # Run the game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        update_function()

        pygame.display.flip()
        clock.tick(FPS)

def btn(key)->bool:
    """Return bool whether a key is pressed. Accepts either list of keys to check for, or single key.
    Examples: 
    
    `boopy.btn(boopy.K_RIGHT)` or `boopy.btn([boopy.K_RIGHT,boopy.K_d])`"""
    keys = pygame.key.get_pressed()
    any_pressed = False
    if type(key) == int:
        key = [key]
    for k in key:
        if keys[k]:
            any_pressed = True

    return any_pressed

def btnp(key:int|list[int])->bool:
    """Return bool whether a key was just pressed. Accepts either list of keys to check for, or single key.
    Examples: 
    
    `boopy.btnp(boopy.K_RIGHT)` or `boopy.btnp([boopy.K_RIGHT,boopy.K_d])`"""
    global key_states

    any_pressed = False
    if type(key) == int:
        key = [key]
    for k in key:
        keys = pygame.key.get_pressed()
        current_state = keys[k]

        if k not in key_states:
            key_states[k] = False

        pressed = current_state and not key_states[k]
        key_states[k] = current_state
        if pressed:
            any_pressed = True

    return any_pressed

def cls(color=(0, 0, 0)):
    screen.fill(color)

def load_spr(sprite:str):
    return pygame.image.load(sprite)

def spr(x, y, sprite):
    sprite = pygame.transform.scale(sprite, (sprite.get_width() * scale, sprite.get_height() * scale))
    screen.blit(sprite, (x * scale, y * scale))

def tilemap(x:int, y:int, tileset:Spritesheet, map_data:list[int], map_x:int=0, map_y:int=0, map_width:int=None, map_height:int=None):
    """Draws a tilemap to the screen. The parameters x and y specifies where on the screen to draw the tilemap, while map_x and map_y specifies where in the tilemap to read tiles from.
    Parameters map_width and map_height control how much of the tilemap to read. If left at None they will take the entire width of the tilemap."""
    tile_width = tileset.sprite_width
    tile_height = tileset.sprite_height

    if not map_data:
        return

    if map_width == None:
        map_width = len(map_data)
    if map_height == None:
        map_height = len(map_data[0])

    for row_index in range(map_y, map_y + map_height):
        for col_index in range(map_x, map_x + map_width):
            tile_index = map_data[row_index][col_index]
            tile_x = col_index * tile_width
            tile_y = row_index * tile_height
            sprite = tileset.sprites[tile_index]
            sprite = pygame.transform.scale(sprite, (tile_width * scale, tile_height * scale))
            screen.blit(sprite, ((x + tile_x - map_x * tile_width) * scale, (y + tile_y - map_y * tile_height) * scale))
