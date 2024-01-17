import sys

args = sys.argv
print(args)
if len(args) != 5:
    print('''Error. Wrong amount of arguments.
Usage:
`python tilemap_editor.py <spritesheet image path> <spritesheet sprite width> <spritesheet sprite height> <tilemap output path`>

Ex: python tilemap_editor.py spritesheet.png 8 8 tilemap.json''')
    quit()

import boopy

spritesheet = boopy.Spritesheet("spritesheet.png",8,8)

def update():
    global player_x
    global player_y
    if boopy.btn(boopy.K_RIGHT):
        player_x += 1
    if boopy.btn(boopy.K_LEFT):
        player_x -= 1
    if boopy.btn(boopy.K_DOWN):
        player_y += 1
    if boopy.btn(boopy.K_UP):
        player_y -= 1

    boopy.cls((255,241,155)) #clear the screen
    spritesheet.spr(player_x,player_y,0)
    tilemap_data = [
        [1, 3, 1],
        [2, 3, 2],
        [1, 3, 1]
    ]
    boopy.tilemap(0,0,spritesheet,tilemap_data)

boopy.run(update_function=update,screen_width=384,screen_height=216,scaling=4)