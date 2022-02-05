from tkinter import dialog
import pygame
from pygame.locals import *
import random
from camera import *
import sys

class mapHandler:
    
    
    def __init__(self):

        #caracteristics
        self.MAP_LENGTH = 30
        self.MAP_WIDTH = 30
        self.EXT_WALLS_SIZE = 1
        self.PATH_SIZE = int(((self.MAP_LENGTH * self.MAP_WIDTH)))

        #map data values /!\AND/!\ textures[] index
        self.SNOW = 2
        self.WALL = 1
        self.GRASS = 0


        #data declaration   map_data = 2D list
        self.map_data = []


        #textures caracteristics
        self.TILEWIDTH       = 64  #holds the tile width and height
        self.TILEHEIGHT      = 64
        self.TILEHEIGHT_HALF = self.TILEHEIGHT /2
        self.TILEWIDTH_HALF  = self.TILEWIDTH /2


        #here will be stored the loaded images
        self.textures = []
        
        self.map_areas_init()
        

    def map_areas_init(self):
        
        #   map example
        #   GRASS = 0   &   WALL = 1 

        """"
        map_data = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]  
        """
        
        #map data initialisation
        for row in range(self.MAP_WIDTH):
            row = []
            for col in range(self.MAP_LENGTH):
                row.append(1)
                
            self.map_data.append(row)
            
        self.pathMaking(self.GRASS, self.PATH_SIZE) 
        self.biomeCreation()
        self.printMap()
    



    def biomeCreation(self):

        #snowbiome
        snow_x = random.randint(1, self.MAP_LENGTH)
        snow_y = random.randint(1, self.MAP_WIDTH)

        self.pathMaking(self.SNOW, 15)
    
    #pathMaking algorithm
    #creates the navigable area on the map
    def pathMaking(self, TEXTURE, PATH_SIZE):
        row = int(self.MAP_WIDTH/2)
        col = int(self.MAP_LENGTH/2)
        
        self.map_data[int(row/2)][int(col/2)] = TEXTURE
        
        self.path(row, col)
        
        
    def path(self, row, col):
        
        path_size = self.PATH_SIZE

        for PATH_iterator in range(path_size):
            if (PATH_iterator%10 == 0):
                for i in range(12):
                    row, col = self.step(row, col)
            row, col = self.step(row, col)




            

    #moves the position of the path algorithm in a coherent direction
    def step(self, row, col):
        
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4
        

        while True:
            
            PATHChoice = random.randint(1, 4)           #   1 = up      2 = down    3 = left    4 = right
            
            if PATHChoice == UP:
                row += 1           
            elif PATHChoice == DOWN:
                row -= 1        
            elif PATHChoice == LEFT:
                col -= 1        
            else:
                col += 1
                
            #if the current path position is not into the exterior walls
            if row != (0 + self.EXT_WALLS_SIZE) and row != (self.MAP_WIDTH - self.EXT_WALLS_SIZE) and col != (0 + self.EXT_WALLS_SIZE) and col != (self.MAP_LENGTH - self.EXT_WALLS_SIZE):
                break
            else:
                if PATHChoice == UP:
                    row -= 1
                elif PATHChoice == DOWN:
                    row += 1
                elif PATHChoice == LEFT:
                    col += 1 
                else:
                    col -= 1

        self.map_data[row][col] = self.GRASS
        
        return row, col;
        
        
    def printMap(self):
        for row in range(self.MAP_WIDTH):
            print(self.map_data[row][:])     

    def getMap(self):
        return self.map_data    

    
    def cartesianToIso(self, cart_x, cart_y):

        #Isometric position of the texture
        iso_x  = int((cart_x - cart_y)) 
        iso_y  = int((cart_x + cart_y)/2)

        return iso_x, iso_y;


    def isoToCartesian(self, iso_x, iso_y):
        
        cart_x = int((2*iso_y - iso_x)/2)
        cart_y = int((2*iso_y + iso_x)/2)

        return cart_x, cart_y;



    #converts the 2D cartesian map to an isometric one and displays it
    def displayMap(self, WINDOW, camera):
        

        WINDOW.fill((0, 0, 0))

        cam_x, cam_y = self.isoToCartesian(camera.getXPosition(), camera.getYPosition())
        cam_x = int(cam_x/self.TILEWIDTH_HALF)
        cam_y = int(cam_y/self.TILEHEIGHT_HALF)  



        #data boundaries corresponding to camera position
        row_min = cam_y - 20
        if row_min < 0:
            row_min = 0

        col_min =  cam_x - 20
        if col_min < 0:
            col_min = 0


        row_max = cam_y + 20
        if row_max > self.MAP_WIDTH:
            row_max = self.MAP_WIDTH

        col_max = cam_x + 20
        if col_max > self.MAP_LENGTH:
            col_max = self.MAP_LENGTH
        
        
        #iterates throught the map data
        for row in range(row_min, row_max):
            for col in range(col_min, col_max):

                tile = self.map_data[row][col]

                #Cartesian position of the texture
                cart_x = row * self.TILEWIDTH_HALF
                cart_y = col * self.TILEHEIGHT_HALF                  

                #Isometric position of the texture
                iso_x, iso_y = self.cartesianToIso(cart_x, cart_y)
                    
                #choosing the texture to display
                if tile == self.WALL:
                    tileImage = self.textures[self.WALL]
                elif tile == self.GRASS:
                    tileImage = self.textures[self.GRASS]
                            
                #pos = center of the texture
                centered_x = WINDOW.get_rect().centerx + iso_x
                centered_y = WINDOW.get_rect().centery + iso_y
               
                #displays the texture    
                WINDOW.blit(tileImage, (centered_x - camera.getXPosition(), centered_y - camera.getYPosition()))  




    def loadTextures(self):
        
        #load each textures
        wall_texture  = pygame.image.load('Assets/wall.png').convert_alpha() 
        grass_texture = pygame.image.load('Assets/grass.png').convert_alpha()
        snow_texture = pygame.image.load('Assets/snow.png').convert_alpha()
        
        #add each textures to the textures list
        self.textures.append(grass_texture)
        self.textures.append(wall_texture)
        self.textures.append(snow_texture)
