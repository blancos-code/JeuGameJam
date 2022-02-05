import pygame
from pygame.locals import *


class Music:
    
    def __init__(self):
        
        self.musics = {
            'grass':'Assets/Musics/terraria.mp3'
            
            
            
            }
    
    
    
    
    def startMusic(self, music, MUSIC_VOLUME):
        
        pygame.mixer.music.unload()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)     # If the loops is -1 then the music will repeat indefinitely.
        pygame.mixer.music.set_volume(MUSIC_VOLUME)