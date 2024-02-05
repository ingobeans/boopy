import contextlib

with contextlib.redirect_stdout(None):
    import pygame


from pygame import Font
from pygame.constants import *
import csv, typing, pkg_resources, time

pygame.init()

screen = None
clock = None
default_font = Font(pkg_resources.resource_filename(__name__, "monobit.ttf"),16)
key_states = {}
current_framerate = 0
FPS = 60
running = False

class Sprite:
    _register:list = []
    def __init__(self, sprite:str|pygame.Surface):
        "Create a new sprite object from a filepath string or directly pass a pygame Surface."
        self.sprite_filename = sprite
        Sprite._register.append(self)
        if type(sprite) == str:
            self.sprite = None
            if running:
                self.preload_sprite()
        elif type(sprite) == pygame.Surface:
            self.sprite = sprite
    
    def preload_sprite(self):
        if self.sprite != None:
            return
        s = pygame.image.load(self.sprite_filename)
        self.sprite = s
        self.width = s.get_width()
        self.height = s.get_height()

class Spritesheet:
    _register = []

    def __init__(self, sprite:str, sprite_width:int=8, sprite_height:int=8):
        self.sprite = pygame.image.load(sprite)
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.sprites_per_row = self.sprite.get_width() // sprite_width
        Spritesheet._register.append(self)
        if running:
            self.preload_sprites()

    def preload_sprites(self):
        surfaces = []
        sprites = []
        for index in range(self.sprites_per_row * (self.sprite.get_height() // self.sprite_height)):
            row = index // self.sprites_per_row
            col = index % self.sprites_per_row
            x = col * self.sprite_width
            y = row * self.sprite_height
            surface = self.sprite.subsurface(pygame.Rect(x, y, self.sprite_width, self.sprite_height))
            surface = surface.convert_alpha()
            surfaces.append(surface)
            sprites.append(Sprite(surface)) 
        
        self.surfaces = surfaces
        self.sprites = sprites

    def get_sprite_index_by_coordinate(self,x:int,y:int)->int:
        index = y * self.sprites_per_row + x
        return index

    def get_sprite_coordinate_by_index(self,index:int):
        x = index % self.sprites_per_row
        y = index // self.sprites_per_row
        return x, y

    def get_sprite_surface(self, index:int)->pygame.Surface:
        "Gets the pygame Surface of a sprite in the spritesheet by index. Used by Tilemaps"
        return self.surfaces[index]
    
    def get_sprite(self, index:int)->Sprite:
        "Gets a Sprite from spritesheet by index. To use a coordinate, use the get_sprite_index_by_coordinate() function to get index first."
        return self.sprites[index]

class Tilemap:
    _register:list = []
    def __init__(self, tileset, map_data, transparency_color:tuple=None):
        self.tileset = tileset
        self.map_data = map_data
        self.tile_width = tileset.sprite_width
        self.tile_height = tileset.sprite_height
        self.transparency_color = transparency_color
        Tilemap._register.append(self)
        if running:
            self.preload_tilemap()

    def preload_tilemap(self):
        self.map_width = len(self.map_data[0])
        self.map_height = len(self.map_data)
        surface = pygame.Surface((self.map_width * self.tile_width, self.map_height * self.tile_height))

        for row_index in range(self.map_height):
            for col_index in range(self.map_width):
                tile_index = self.map_data[row_index][col_index]
                if tile_index == -1:
                    continue
                tile_x = col_index * self.tile_width
                tile_y = row_index * self.tile_height
                sprite = self.tileset.surfaces[tile_index]
                surface.blit(sprite, (tile_x, tile_y))

        if self.transparency_color != None:
            surface.set_colorkey(self.transparency_color)
        self.map_surface = surface
    
    def get_tile(self,x:int,y:int)->int:
        if x < 0 or y < 0:
            return -1
        elif y >= self.map_height or x >= self.map_width:
            return -1
        return self.map_data[y][x]

def run(update_function, title:str="boopy", icon:str=None, screen_width:int=128, screen_height:int=128, scaling:int=None, fullscreen:bool=False, fps_cap:typing.Optional[int]=60, vsync:bool=False):
    """Runs game. Update_function is the function that will be called each frame. Parameter fps_cap can be an integer or set to None, which will unlock the frame rate.
    
    Scaling is how much to scale up the game window. If None, will autoscale to fit screen.
    If fullscreen is True, scaling will be ignored"""
    global screen, clock, FPS, current_framerate, running

    running = True

    FPS = fps_cap
    # set up the display
    pygame.display.set_caption(title)
    icon = icon if icon != None else pkg_resources.resource_filename(__name__, "icon.png")
    pygame.display.set_icon(pygame.image.load(icon))
    
    vsync = 1 if vsync else 0

    # the following mess is for setting up the screen
    if fullscreen:
        flags = SCALED | FULLSCREEN
        screen = pygame.display.set_mode((screen_width, screen_height), flags, vsync=vsync)
    else:
        if scaling != None:
            if scaling == 1:
                screen = pygame.display.set_mode((screen_width, screen_height), vsync=vsync)
            else:
                flags = HIDDEN | SCALED
                screen = pygame.display.set_mode((screen_width, screen_height), flags, vsync=vsync)
                window = pygame.Window.from_display_module()
                window.size = (screen_width * scaling, screen_height * scaling)
                window.position = WINDOWPOS_CENTERED
                window.show()
        else:
            flags = SCALED
            screen = pygame.display.set_mode((screen_width, screen_height), flags, vsync=vsync)

    # sprites, spritesheets & tilemaps's surfaces must be preloaded after boopy is ran, when the scale has been defined
    for t in Spritesheet._register:
        t.preload_sprites()
    for t in Sprite._register:
        t.preload_sprite()
    for t in Tilemap._register:
        t.preload_tilemap()

    clock = pygame.time.Clock()
    last_check = time.time()
    frames = 0

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
    
    screen.blit(text_surface,(x,y))

def draw_rect(from_x:int, from_y:int, to_x:int, to_y:int, color: tuple = (0, 0, 0)) -> None:
    pygame.draw.rect(screen, color, (from_x, from_y, to_x - from_x, to_y - from_y))

def draw_tilemap(x:int, y:int, tilemap: Tilemap):
    screen.blit(tilemap.map_surface, (x, y))   

def draw_sprite(x:int, y:int, sprite: Sprite):
    screen.blit(sprite.sprite, (x, y))

def draw_spritesheet(x:int, y:int,spritesheet:Spritesheet,sprite_index:int):
    screen.blit(spritesheet.get_sprite_surface(sprite_index), (x, y))

def draw_line(from_x:int, from_y:int, to_x:int, to_y:int, color: tuple = (0, 0, 0), width:int=1):
    pygame.draw.line(screen,color,(from_x,from_y),(to_x,to_y),width)

def draw_pixel(x:int, y:int, color: tuple = (0, 0, 0)):
    screen.set_at((x,y),color)