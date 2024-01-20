import contextlib

with contextlib.redirect_stdout(None):
    import pygame

from pygame.locals import *
from pygame.font import *
from screeninfo import get_monitors

import csv, typing, pkg_resources, time

pygame.init()

screen = None
clock = None
scale = 1
default_font = Font(pkg_resources.resource_filename(__name__, "monobit.ttf"),16)
key_states = {}
current_framerate = 0
FPS = 60
running = False

class Spritesheet:
    _register = []

    def __init__(self, sprite:str, sprite_width:int=8, sprite_height:int=8):
        self.sprite = pygame.image.load(sprite)
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.sprites_per_row = self.sprite.get_width() // sprite_width
        Spritesheet._register.append(self)
        if running:
            self.preload_sprites(scale)

    def preload_sprites(self,scale):
        sprites = []
        for index in range(self.sprites_per_row * (self.sprite.get_height() // self.sprite_height)):
            row = index // self.sprites_per_row
            col = index % self.sprites_per_row
            x = col * self.sprite_width
            y = row * self.sprite_height
            sprite = self.sprite.subsurface(pygame.Rect(x, y, self.sprite_width, self.sprite_height))
            sprites.append(pygame.transform.scale(sprite, (sprite.get_width() * scale, sprite.get_height() * scale)))
        self.sprites = sprites

    def get_sprite(self, index):
        return self.sprites[index]


class Sprite:
    _register:list = []
    def __init__(self, sprite:str):
        self.sprite_filename = sprite
        self.sprite = None
        Sprite._register.append(self)
        if running:
            self.preload_sprite(scale)
    
    def preload_sprite(self,scale):
        s = pygame.image.load(self.sprite_filename)
        self.sprite = pygame.transform.scale(s, (s.get_width() * scale, s.get_height() * scale))

class Tilemap:
    _register:list = []
    def __init__(self, tileset, map_data):
        self.tileset = tileset
        self.map_data = map_data
        self.tile_width = tileset.sprite_width
        self.tile_height = tileset.sprite_height
        Tilemap._register.append(self)
        if running:
            self.preload_tilemap(scale)

    def preload_tilemap(self,scale:int):
        map_width = len(self.map_data[0])
        map_height = len(self.map_data)
        surface = pygame.Surface((map_width * self.tile_width, map_height * self.tile_height))

        for row_index in range(map_height):
            for col_index in range(map_width):
                tile_index = self.map_data[row_index][col_index]
                tile_x = col_index * self.tile_width
                tile_y = row_index * self.tile_height
                sprite = self.tileset.sprites[tile_index]
                sprite = pygame.transform.scale(sprite, (self.tile_width, self.tile_height))
                surface.blit(sprite, (tile_x, tile_y))

        
        self.map_surface = pygame.transform.scale(surface, (surface.get_width()*scale,surface.get_height()*scale))
    
    def get_tile(self,x:int,y:int)->int:
        return self.map_data[y][x]

def run(update_function, title:str="boopy", icon:str=None, screen_width:int=128, screen_height:int=128, scaling:int=1, fullscreen:bool=False, fps_cap:typing.Optional[int]=60, vsync:bool=False):
    """Runs game. Update_function is the function that will be called each frame. Parameter fps_cap can be an integer or set to None, which will unlock the frame rate.
    
    Scaling is how much to scale up the game window. If fullscreen is True, this will be ignored."""
    global screen, clock, scale, FPS, current_framerate, running

    running = True

    FPS = fps_cap
    scale = scaling
    
    # set up the display
    pygame.display.set_caption(title)
    
    icon = icon if icon != None else pkg_resources.resource_filename(__name__, "icon.png")
    pygame.display.set_icon(pygame.image.load(icon))
    
    flags = pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED if fullscreen else pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED
    vsync = 1 if vsync else 0

    if fullscreen:
        height = get_monitors()[0].height
        scale = height//screen_height
    screen = pygame.display.set_mode((screen_width * scale, screen_height * scale), flags, vsync=vsync)

    for t in Spritesheet._register:
        t.preload_sprites(scale)
    for t in Sprite._register:
        t.preload_sprite(scale)
    for t in Tilemap._register:
        t.preload_tilemap(scale)
    
    # sprites, spritesheets & tilemaps's surfaces must be preloaded after boopy is ran, when the scale has been defined

    clock = pygame.time.Clock()
    last_check = time.time()
    frames = 0

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        if FPS != None:
            current_framerate = clock.get_fps()
        else:
            frames += 1
            current_time = time.time()
            if current_time - last_check >= 1:
                last_check = current_time
                current_framerate = frames
                frames = 0
        update_function()
        pygame.display.flip()
        if FPS:
            clock.tick(FPS)

def get_csv_file_as_lists(filename:str)->list[list]:
    csv_reader = csv.reader(open(filename))
    return [[int(value) for value in row if value] for row in csv_reader]

def mouse()->tuple:
    """Return the mouse position relative to the game window as a tuple"""
    pygame.mouse.get_pos()

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
    
def get_fps()->int:
    return int(current_framerate)

def cls(color=(0, 0, 0)):
    screen.fill(color)

def draw_text(x:int,y:int,text:str,color:tuple=(255,255,255),font:Font=default_font):
    """Draw text to the screen. Uses Font objects."""
    text_surface = font.render(text,False,color)
    
    screen.blit(pygame.transform.scale(text_surface, (text_surface.get_width() * scale, text_surface.get_height() * scale)),(x*scale,y*scale))

def draw_rect(x: int, y: int, x2: int, y2: int, color: tuple = (0, 0, 0)) -> None:
    pygame.draw.rect(screen, color, (x*scale, y*scale, x2*scale - x*scale, y2*scale - y*scale))

def draw_tilemap(x:int, y:int, tilemap: Tilemap):
    screen.blit(tilemap.map_surface, (x * scale, y * scale))   

def draw_sprite(x:int, y:int, sprite: Sprite):
    screen.blit(sprite.sprite, (x * scale, y * scale))

def draw_spritesheet(x:int, y:int,spritesheet:Spritesheet,sprite_index:int):
    screen.blit(spritesheet.get_sprite(sprite_index), (x * scale, y * scale))