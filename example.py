import boopy, json

player_x = 16*8
player_y = 16*8

spritesheet = boopy.Spritesheet("spritesheet.png",8,8)
player_sprite = boopy.load_spr("player.png")

screen_width=184
screen_height=160

with open("tilemap.json") as f:
    tilemap = json.load(f)
    # Currently there's no proper way to create tilemaps
    # I created this tilemap using https://edwardscamera.github.io/array-map-creator/
    # Export to python and you're all good!

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

    boopy.cls((0,0,0)) #clear the screen    
    boopy.tilemap(-player_x+screen_width/2,-player_y+screen_height/2,spritesheet,tilemap)
    
    boopy.spr(screen_width/2,screen_height/2,player_sprite)

boopy.run(update_function=update,screen_width=screen_width,screen_height=screen_height,scaling=5)