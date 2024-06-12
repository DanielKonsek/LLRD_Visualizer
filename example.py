#these files need to be in the directory
from DSA import *
from Queue import Queue
from RedBlack import RBT
from LLRB_Vis import Renderer
#these files need to be or are installed on the system
import pygame
import random
import time


rbt = RBT()
	
window = Renderer(800,600,"LLRB",16)
example = "abcd" #initial graph
i = 0
for c in example:
    rbt.put(c,i)
    i += 1

window.printList(window.treeToList(rbt.root))
window.treeToGraph(rbt.root)


#main loop listening for keyboard presses
pygame.init()
clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #close game on quit event (for example pressing x on upper right) 
            running = False
        if event.type == pygame.KEYDOWN:
            print(event.unicode)
            if rbt.get(event.unicode) != None: #check if key already in rbt, if yes delete, if no add to rbt 
                rbt.delete(event.unicode)
            else: 
                rbt.put(event.unicode, random.randint(0,99))
            window.clear()
            window.treeToGraph(rbt.root)
            window.printList(window.treeToList(rbt.root))


    clock.tick(60)