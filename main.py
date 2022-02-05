import pygame
from pygame.locals import *
from src.mapHandler import mapHandler
from src.camera import Camera
from src.config import *
from src.music import Music
import sys


 
class Game:
    def __init__(self):
        
        self.runningState = True
        
        #pygame init
        pygame.init()
        pygame.display.set_caption('Le jeu bg')
        self.WINDOW   = pygame.display.set_mode((0, 0), FULLSCREEN)    #set the display mode, window title and FPS clock
        self.FPSCLOCK = pygame.time.Clock()
        
        #camera init
        self.camera = Camera()
        
        #map init
        self.map = mapHandler()
        self.map.map_areas_init()
        self.map_data = self.map.getMap() 
        self.map.loadTextures()            
        self.map.displayMap(self.WINDOW, self.camera)
        
        #camera positioning
        self.camera.setPosition(int(self.map.MAP_LENGTH/2), int(self.map.MAP_WIDTH/2))
        
        
        #music init & start
        self.music = Music()
        self.music.startMusic(self.music.musics['grass'], MUSIC_VOLUME)
        
      
    def main(self):
        while self.isRunning():
            
            #updates gamestate
            self.update()
            
            #game exit handle
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.runningState = False
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.runningState = False
                        pygame.quit()
                        sys.exit()

            #clock
            self.FPSCLOCK.tick(60)
        
    def update(self):
        self.movement()
        self.draw()

        
    def draw(self):
        
        #sets the map textures to the surface (screen)
        self.map.displayMap(self.WINDOW, self.camera)
        
        #displays the surface content
        pygame.display.flip()
        
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.camera.setPosition(self.camera.getXPosition(), self.camera.getYPosition() + 20)
        if keys[pygame.K_z]:
            self.camera.setPosition(self.camera.getXPosition(), self.camera.getYPosition() - 20)
        if keys[pygame.K_q]:
            self.camera.setPosition(self.camera.getXPosition() - 20, self.camera.getYPosition())
        if keys[pygame.K_d]:
            self.camera.setPosition(self.camera.getXPosition() + 20, self.camera.getYPosition())

    def isRunning(self):
        return self.runningState
            
game = Game()
game.main()

 
 
