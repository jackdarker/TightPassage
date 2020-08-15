import pygame
from os.path import abspath
from pygame import Rect
import os, sys
import json
from stat import *

class TileMapCreator():
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((640,480), pygame.HWSURFACE | pygame.DOUBLEBUF  )
        pass

    def walktree(self,top, callback):
        '''recursively descend the directory tree rooted at top,
           calling the callback function for each regular file'''

        for f in os.listdir(top):
            pathname = os.path.join(top, f)
            mode = os.stat(pathname).st_mode
            if S_ISDIR(mode):
                # It's a directory, recurse into it
                callback(pathname,True)
                self.walktree(pathname, callback)
            elif S_ISREG(mode):
                # It's a file, call the callback function
                if(top!=self.basedir): callback(pathname,False)
            else:
                # Unknown file type, print a message
                print('Skipping %s' % pathname)
        pass

    def SpritesToTilemap(self, basedir):
        '''creates a combined tilemap from single images located in one-directory-per-animation
        The images must have the same size.
        The tilemap has the name of <basedir>.png and it contains one row per animation
        A Jsonfile is created as descriptor of the animations (sprite-size,count,...)
        '''
        self.dir=""
        self.allfiles={}
        self.maxFiles=0
        self.FileCounter=0
        self.basedir = basedir
        self.walktree(basedir, self.visitfile)
        data = {}
        animName = ""
        countAnims = len(self.allfiles)
        
        y=0
        textureTile=None
        for anim in self.allfiles:
            x=0
            for f in self.allfiles[anim]:
                animName = os.path.basename(os.path.dirname(f))
                Sprite = pygame.image.load(abspath(f)).convert_alpha()
                if(textureTile==None):
                    size = Sprite.get_size()    #assume that sprites are equal in size
                    textureSize = (size[0]*self.maxFiles,size[1]*countAnims)
                    textureTile = pygame.Surface(textureSize,pygame.SRCALPHA)
                textureTile.blit(Sprite,(Sprite.get_width()*x,Sprite.get_height()*y))
                x+=1
            y+=1
            data[animName] = {"size":size,"count":x}    #build a anim-description-block
        filename = os.path.basename(basedir)+".png"
        pygame.image.save(textureTile,abspath(os.path.join(basedir,filename)))
        #write the anim-description-blocks
        filename = os.path.basename(basedir)+".json"
        with open(abspath(os.path.join(basedir,filename)), 'w') as outfile:
            json.dump(data, outfile)

    def visitfile(self,file,isDir):
        print(file)
        if(isDir==True):
            self.dir=file
            self.FileCounter=0
        else:
            files=self.allfiles.get(self.dir)
            if not files: 
                files=[]

            files.append(file)
            self.allfiles[self.dir]=files
            self.FileCounter+=1
            if(self.FileCounter>self.maxFiles): self.maxFiles=self.FileCounter

if __name__ == '__main__':
    creator = TileMapCreator()
    creator.SpritesToTilemap(abspath("C:/tmp/Fox"))
    pass


#with open('data.txt') as json_file:
#    data = json.load(json_file)
#    for p in data['people']:
#        print('Name: ' + p['name'])
#        print('Website: ' + p['website'])
#        print('From: ' + p['from'])
#        print('')