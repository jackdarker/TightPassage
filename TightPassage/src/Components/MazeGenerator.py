import sys, os
import random
from lxml import etree
import numpy as np
import src.Const as Const
import src.Support as Support

class MazeGenerator():
    """generates a list of nodes that represents a maze by there connection to each other"""
    def __init__(self):
        pass

    def setParams(self,numberofRooms,gridBuilder):
        self.possibleNumberofRooms = numberofRooms
        self.gridBuilder = gridBuilder

    def createMap(self):
        if(type(self.possibleNumberofRooms)==int):
            self.numberofRooms = self.possibleNumberofRooms
        else:   #the variable should be a int or a function returning an int
            self.numberofRooms = self.possibleNumberofRooms()
        
        self.nodes = self.gridBuilder.createGrid()
        self.walkstack = []
        self.roomscarved = 0
        self._randomizeStart()
        while(not self._carve()):
            pass
        
        self._addMoreDoors()
        self._randomizeExit()
        self._print()

    def _randomizeStart(self):
        self.startnode = self.currentnode = random.choice(self.nodes)
        self.startnode.isPlayerSpawn = True
        self.startnode.isRoom = True

    def _randomizeExit(self):
        #todo designate a plain room as exit, the room should be in a good distance from start
        pass

    def _carve(self):
        """carve out rooms until numberofrooms met or not possible to carve anymore
        returns True if done
        """
        if(self.roomscarved>=self.numberofRooms): 
            return True
        directions =self.currentnode.neighbors.copy()
        random.shuffle(directions)
        
        for node in directions:
            if(node.isRoom==False):
                self.gridBuilder.createDoor(node,self.currentnode)
                self.walkstack.append(self.currentnode)
                self.currentnode = node
                node.isRoom=True
                self.roomscarved+=1
                break
        else: #all possible directions already have rooms, so go back to previous room
            self.currentnode = self.walkstack.pop()
            if(self.currentnode==self.startnode):
                return True #its not possible to carve anymore room
        
        return False

    def _addMoreDoors(self):
        #now we have nodes with rooms connected by doors to other rooms
        #but maybe we want to add additional doors between rooms that 
        #are positioned right next to each other and have no doors yet
        self.currentnode = self.startnode
        for n in self.nodes:
            self.currentnode = n
            directions =self.currentnode.neighbors.copy()
            for node in directions:
                if(node.isRoom==True and self.currentnode.isRoom==True
                   and node.doors.count(self.currentnode)==0 and
                   random.random()<0.5):    #todo maybe some more rules when to add doors
                    self.gridBuilder.createDoor(node,self.currentnode)
        pass

    def _print(self):
        roomarray = {}
        max_x = max_y = 0
        for node in self.nodes:
            name = '{0}_{1}'.format(node.x,node.y)
            if(max_x<node.x): max_x=node.x
            if(max_y<node.y): max_y=node.y
            info = {'W':' ','E':' ','N':' ','S':' ','R':'_'}
            if(node.isRoom==True):
                info['R'] = 'O'
            if(node.isPlayerSpawn==True):
                info['R'] = 'P'
            for door in node.doors:
                if(door.x < node.x):
                    info['W'] = '<'
                if(door.x > node.x):
                    info['E'] = '>'
                if(door.y < node.y):
                    info['N'] = '^'
                if(door.y > node.y):
                    info['S'] = 'v'

            roomarray[name] = info

        y=0
        while(y<=max_y):
            x =0
            line1=''
            line2=''
            line3=''
            while(x<=max_x):
                name = '{0}_{1}'.format(x,y)
                info = roomarray[name]
                line1 = line1 +'  {0}  '.format(info['N'])
                line2 = line2 +'{0}{1}{2}'.format(info['W'],
                                           '{0}{1}{2}'.format(x,info['R'],y),info['E'])
                line3 = line3 +'  {0}  '.format(info['S'])
                #print(text,sep='', end=' ')
                x+=1
            print(line1)
            print(line2)
            print(line3)
            y+=1

class TestMazeGenerator(MazeGenerator):
    """generates non-Random-maze for testing all possible roomlayouts
                
            o   o---o
            |   |
            o---o---o---o---o   o
                        |   |   |
            o---o   o---P   o---o
                |   |       |
                o---o   o---o---o
                    |       |
                    o       o

    """
    def createMap(self):
        gridBuilder = GridBuilderRect()
        gridBuilder.setParams(6,6)
        self.setParams(6,gridBuilder)
        self.nodes = self.gridBuilder.createGrid()
        for node in self.nodes:
            if(node.x==0 and node.y==0):
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x,node.y+1),node)
                node.isRoom=True
            elif(node.x==1 and node.y==0):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x+1,node.y),node)
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x,node.y+1),node)
            elif(node.x==2 and node.y==0):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x-1,node.y),node)

            elif(node.x==0 and node.y==1):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x+1,node.y),node)
            elif(node.x==1 and node.y==1):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x+1,node.y),node)
            elif(node.x==2 and node.y==1):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x+1,node.y),node)
            elif(node.x==3 and node.y==1):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x+1,node.y),node)
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x,node.y+1),node)
            elif(node.x==4 and node.y==1):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x,node.y+1),node)
            elif(node.x==5 and node.y==1):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x,node.y+1),node)
            elif(node.x==0 and node.y==2):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x+1,node.y),node)
            elif(node.x==1 and node.y==2):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x,node.y+1),node)
            elif(node.x==2 and node.y==2):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x+1,node.y),node)
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x,node.y+1),node)
            elif(node.x==3 and node.y==2):
                node.isPlayerSpawn=True
                node.isRoom=True
            elif(node.x==4 and node.y==2):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x+1,node.y),node)
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x,node.y+1),node)
            elif(node.x==5 and node.y==2):
                node.isRoom=True
            elif(node.x==1 and node.y==3):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x+1,node.y),node)
            elif(node.x==2 and node.y==3):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x,node.y+1),node)
            elif(node.x==3 and node.y==3):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x+1,node.y),node)
            elif(node.x==4 and node.y==3):
                node.isRoom=True
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x+1,node.y),node)
                gridBuilder.createDoor(gridBuilder._getNodeByGrid(node.x,node.y+1),node)
            elif(node.x==5 and node.y==3):
                node.isRoom=True
            elif(node.x==2 and node.y==4):
                node.isRoom=True
            elif(node.x==4 and node.y==4):
                node.isRoom=True
        self._print()

class MapNode():
    """represents a node in a map"""

    @staticmethod
    def getPlayerSpawnNode(nodes):
        for node in nodes:
            if(node.isPlayerSpawn==True):
                return node
        return None

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.neighbors = []
        self.doors = []
        #a function doorResolver(nodes,actualnode,doorlabel) that returns the target-node of the door in the actualnode f.e. north-door connects to south-node
        self.doorResolver = None
        self.isRoom=False
        self.isPlayerSpawn = False
        self.fileName = ""

class GridBuilder():
    def __init__(self):
        pass

    def createGrid(self):
        """returns a list of nodes that have a list to which nodes they are connected"""
        self.nodes= list()

    def createDoor(self,nodeA,nodeB):
        if(nodeA.doors.count(nodeB)==0):
            nodeA.doors.append(nodeB)
        if(nodeB.doors.count(nodeA)==0):
            nodeB.doors.append(nodeA)
        return


class GridBuilderRect(GridBuilder):

    @staticmethod
    def doorResolverNESW(nodes,actualnode,doorlabel):
        #find the targetnode of the specified exitdoor
        if(doorlabel == 'north'):
            x=0
            y=-1
        elif(doorlabel == 'south'):
            x=0
            y=1
        elif(doorlabel == 'east'):
            x=1
            y=0
        elif(doorlabel == 'west'):
            x=-1
            y=0
        for door in actualnode.doors:
            if(door.x == actualnode.x+x and door.y == actualnode.y+y ):
                return door
        raise Exception()

    def __init__(self):
        super().__init__()

    def setParams(self,width, height):
        self.width = width
        self.height = height

    def createGrid(self):
        self.nodes= list()
        i=0
        #from left to right, from top to bottom
        while(i<self.height):
            k=0
            while(k<self.width):
                node = MapNode(k,i)
                node.doorResolver = GridBuilderRect.doorResolverNESW
                self.nodes.append(node)
                k+=1
            i+=1

        for node in self.nodes:
            node.neighbors = list()
            if(node.x>0):
                node.neighbors.append(self._getNodeByGrid(node.x-1,node.y))
            if(node.x<self.width-1):
                node.neighbors.append(self._getNodeByGrid(node.x+1,node.y))
            if(node.y>0):
                node.neighbors.append(self._getNodeByGrid(node.x,node.y-1))
            if(node.y<self.height-1):
                node.neighbors.append(self._getNodeByGrid(node.x,node.y+1))
        
        return(self.nodes)

    def _getNodeByGrid(self,x,y):
        n = y*self.width +x
        return self.nodes[n]

class RoomDesigner():
    """this uses a list of MapNodes and decides which Level-design should be loaded
    f.e. if a room has 3 doors it will search for a level-file that has 3 doors
    """
    def __init__(self):
        pass

    def setMapNodes(self,nodes):
        self.nodes = nodes

    def parseLevelTemplates(self,filelist): #todo uses actually Tiled-maps only
        #todo expecting rectangular leveldesing where the doors are tagged with north,south,east,west

        #read the files and detect what doors they have 
        #create a lookuptable with the entrys as keys
        #there can be multiple entrys per key to allow different designs
        self.roomlayouts = {}
        for filename in filelist:
            root = etree.parse(filename)
            #todo "./objectgroup[@name='Navigation']/object[@type='Warp']/properties/property[@name='target']"
            #doors should be an object with type=Warp and a property with name=target
            doors=root.findall("./objectgroup/object[@type='Warp']/properties/property[@name='target']")
            directions=[]
            for door in doors:
                dir = door.attrib.get('value')
                if(dir=='north'): dir='N'
                elif(dir=='south'): dir='S'
                elif(dir=='west'): dir='W'
                elif(dir=='east'): dir='E'
                directions.append(dir)
            directions.sort()
            key = "".join(directions)   #creates something like NS
            if(key in self.roomlayouts):
                self.roomlayouts[key].append(filename)
            else:
                self.roomlayouts[key]=[filename]
        pass

    def createWorld(self):
        """uses the set MapNodes and parsed LevelTemplates to 
        select which Mapnode should be represented by which leveldesign 
        assign the design to the mapnode
        """
        max_x = max_y = 0
        for node in self.nodes:
            if(max_x<node.x): max_x=node.x
            if(max_y<node.y): max_y=node.y
            directions=[]
            if(node.isRoom==True):
                for door in node.doors:
                    if(door.x > node.x):
                        directions.append('E')
                    if(door.y < node.y):
                        directions.append('N')
                    if(door.y > node.y):
                        directions.append('S')
                    if(door.x < node.x):
                       directions.append('W')
                
                directions.sort()#key has to be in alphabetic order !
                key = "".join(directions)
                files = self.roomlayouts[key]   #todo improve erroroutput '...maybe you didnt parse the maps or there is no map with this layout'
                node.fileName = random.choice(files)
        pass

def test():
    filename=Const.resource_path("assets/levels/Level0.tmx")
    root = etree.parse(filename)
    designer = RoomDesigner()
    designer.parseLevelTemplates([filename])

    #root = etree.Element("root")
    #root.append( etree.Element("child1") )
    print(etree.tostring(root,pretty_print=True))

def test2():
    gbuilder = GridBuilderRect()
    gbuilder.setParams(5, 4)
    mzbuilder = MazeGenerator()
    mzbuilder.setParams(10, gbuilder)
    mzbuilder.createMap()
    mzbuilder._print()
    designer = RoomDesigner()
    designer.setMapNodes(mzbuilder.nodes)
    designer.parseLevelTemplates([Const.resource_path("assets/levels/Level0.tmx"),
                                        Const.resource_path("assets/levels/Level1.tmx"),
                                        Const.resource_path("assets/levels/Level2.tmx"),
                                        Const.resource_path("assets/levels/Level3.tmx"),
                                        Const.resource_path("assets/levels/Level4.tmx"),
                                        Const.resource_path("assets/levels/Level5.tmx"),
                                        Const.resource_path("assets/levels/Level6.tmx"),
                                        Const.resource_path("assets/levels/Level7.tmx"),
                                        Const.resource_path("assets/levels/Level8.tmx"),
                                        Const.resource_path("assets/levels/Level9.tmx"),
                                        Const.resource_path("assets/levels/Level10.tmx"),
                                        Const.resource_path("assets/levels/Level11.tmx"),
                                        Const.resource_path("assets/levels/Level12.tmx"),
                                        Const.resource_path("assets/levels/Level13.tmx"),
                                        Const.resource_path("assets/levels/Level14.tmx")])
    designer.createWorld()
    pass


if __name__ == "__main__" :
    test2()