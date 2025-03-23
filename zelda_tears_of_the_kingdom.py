# -------------------------------- import packages --------------------------------------------
import requests
import os
import cv2
import numpy as np
import time


# ----------------------------------- functions -----------------------------------------------

def get_tiles(which_map, start_col, end_col, start_row, end_row):
    tiles = []    

    for row in range(start_row, end_row):
        for col in range(start_col, end_col):
            tiles.append(f"https://www.zeldadungeon.net/maps/totk/tiles/{which_map}/6/{col}_{row}.jpg")
    
    # print(tiles) # to check

    folder = "{which_map}_map_tiles"
    os.makedirs(folder, exist_ok = True)  # if folder doesn't exist, make it

    for index, url in enumerate(tiles):
        print(f"downloading {url}...")
        col_section, row_section = url.split("_")
        col = col_section.split("/")[-1]
        row = row_section.split(".")[0]

        # if the image already exists in the folder, skip it
        image_filename = os.path.join(folder, f"{col}_{row}.jpg")

        if os.path.exists(image_filename):
            print(f"Image {image_filename} already exists, skipping download.")
            continue  # Skip downloading this image
        
        # send a HTTP GET request to URL
        response = requests.get(url)

        # check if the request was successful (status code 200)
        if response.status_code == 200:
            # file path to save image in
            image_filename = os.path.join(folder, f"{col}_{row}.jpg")
            with open(image_filename, 'wb') as file:
                file.write(response.content)
            print(f"tile {col}_{row} downloaded")
        else:
            print(f"couldn't download tile {col}_{row} from {url}. status code: {response.status_code}")
        time.sleep(0.01)

        # break # try one

def stitch_images_to_big_picture(which_map, start_col, end_col, start_row, end_row):
    folder = "{which_map}_map_tiles"
    tiles = []
    
    for row in range(start_row, end_row):
        row_tiles = []
        for col in range(start_col, end_col):
            # find the tile
            tile_path = os.path.join(folder, f"{col}_{row}.jpg")
            tile = cv2.imread(tile_path)
            
            if tile is None:
                print(f"couldn't load tile {tile_path}")
                return
            
            row_tiles.append(tile)
        
        # stitch this row horizontally
        stitched_row = np.hstack(row_tiles)
        tiles.append(stitched_row)

        # break # try one
    
    # stitch all rows
    stitched_big_picture = np.vstack(tiles)

    # save the big picture
    big_picture_filename = f"zelda_tears_of_the_kingdom_{which_map}_map.jpg"
    cv2.imwrite(big_picture_filename, stitched_big_picture)
    print(f"big picture saved as {big_picture_filename}")

def crop_big_picture(which_map, start_col, end_col, start_row, end_row):
    folder = "{which_map}_map_tiles"
    tiles_to_delete = []

    # find tiles
    for row in range(start_row, end_row):
        for col in range(start_col, end_col):
            tile = f"{col}_{row}.jpg"
            tiles_to_delete.append(tile)

    # delete the tiles
    for tile in tiles_to_delete:
        image_path = os.path.join(folder, tile)
        
        # if the tile exists, delete it
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
                print(f"deleted: {image_path}")
            except Exception as e:
                print(f"couldn't delete {image_path}: {e}")
        else:
            print(f"image {image_path} doesn't exist.")


# -------------------------------- function calls --------------------------------------------

# # for depths map
# which_map = "depths"
# start_col, end_col = 5, 15
# start_row, end_row = 10, 54

# # for sky map
# which_map = "sky"
# start_col, end_col = 1, 60
# start_row, end_row = 6, 57

# # get images
# get_tiles(which_map, start_col, end_col, start_row, end_row)

# # stitch images together
# stitch_images_to_big_picture(which_map, start_col, end_col, start_row, end_row)

# # delete extraneous tiles from folder
# start_col, end_col = 5, 57
# start_row, end_row = 55, 59
# crop_big_picture(which_map, start_col, end_col, start_row, end_row)