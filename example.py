import boopy

player_x = 16*8
player_y = 16*8

spritesheet = boopy.Spritesheet("spritesheet.png",8,8)
player_sprite = boopy.Sprite("player.png")

tilemap_data = boopy.get_csv_file_as_lists("example_tiled_tilemap.csv")
# boopy expects tilemaps to be represented as a 2D list
# however, if you want to use a tilemap in CSV format (Like Tiled exports to - https://thorbjorn.itch.io/tiled):
# the get_csv_file_as_lists() function converts a csv file to a 2D list

tilemap = boopy.Tilemap(spritesheet,tilemap_data)

screen_width=128
screen_height=128

def update():
    global player_x, player_y

    if boopy.btn(boopy.K_RIGHT):
        player_x += 1
    if boopy.btn(boopy.K_LEFT):
        player_x -= 1
    if boopy.btn(boopy.K_DOWN):
        player_y += 1
    if boopy.btn(boopy.K_UP):
        player_y -= 1

    boopy.cls((0,0,0))
    boopy.draw_tilemap(-player_x + screen_width / 2, -player_y + screen_height / 2, tilemap)

    boopy.draw_sprite(screen_width / 2 - 4, screen_height / 2 - 4, player_sprite)
    # draw the player sprite in the center of the screen (-4 to account for sprite offset, since sprites originate from top left corner)

    boopy.draw_text(1,-5,f"{boopy.get_fps()} FPS")
    boopy.draw_text(1,8,f"{tilemap.get_tile(player_x//8,player_y//8)} - Tile at player")

boopy.run(update_function=update,screen_width=screen_width,screen_height=screen_height,scaling=7,fps_cap=None,vsync=True,fullscreen=False)