import pygame
import math
from pygame import gfxdraw


class Renderer:
    nodes = [] # a list of all nodes. Needed for click selection
    selectedNode = None

    class Node:
        rad = 16
        font = None

        def __init__(self, node, x, y):
            self.key = node.key
            self.value = node.value
            self.x = x
            self.y = y
            self.color = (0, 0, 0)                
            if node.color:
                self.color = (255, 0, 0)

            self.font = pygame.font.SysFont(None, 2 * self.rad)
            
        def draw(self, screen, selectedNode):
            
            if selectedNode is None or selectedNode.key != self.key:
                gfxdraw.circle(
                    screen,
                    self.x + int(self.rad // 2),
                    self.y + int(self.rad // 2),
                    self.rad,
                    self.color,
                )
                gfxdraw.circle(
                screen,
                self.x + int(self.rad // 2),
                self.y + int(self.rad // 2),
                self.rad + 1,
                self.color,
            )
            else:
                transparentBackground = (self.color[0],self.color[1],self.color[2],100)
                gfxdraw.filled_circle(
                    screen,
                    self.x + int(self.rad // 2),
                    self.y + int(self.rad // 2),
                    self.rad + 1,
                    pygame.Color(transparentBackground),
                )
                #render value of Node
                img = self.font.render(str(self.value), True, "Black")
                screen.blit(img,(10,10))

            img = self.font.render(self.key, True, self.color)
            screen.blit(img, (self.x, self.y))

    def __init__(
        self,
        width,
        height,
        caption="Graph-plot",
        rad=16,
        backgroundColour=(255, 255, 255),
    ):
        pygame.init()
        self.backgroundColour = backgroundColour
        self.width = width
        self.height = height
        self.rad = rad
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)
        self.screen.fill(self.backgroundColour)
        pygame.display.flip()
        

    def treeToList(self, node):
        treeList = []
        running = True
        itt = 0
        size = 1

        if node != None:
            treeList.append([node])
        else:
            running = False

        while running:
            depth = []
            for x in range(size):
                if treeList[itt][x] != None:
                    if treeList[itt][x].left != None:
                        depth.append(treeList[itt][x].left)
                    else:
                        depth.append(None)
                    if treeList[itt][x].right != None:
                        depth.append(treeList[itt][x].right)
                    else:
                        depth.append(None)
                else:
                    depth.append(None)
                    depth.append(None)
            isEmpty = True

            for x in depth:
                if x != None:
                    isEmpty = False

            if not isEmpty:
                treeList.append(depth)
            else:
                running = False
            itt = itt + 1
            size = size * 2
        return treeList

    def listToGraph(self, list):
        coordinate = []
        self.nodes = [] #reset nodes
        rowNumber = 0

        for row in list:
            rowVector = []
            step = self.width // (pow(2, rowNumber) + 1)
            x = step - self.rad // 2
            y = (4 + 6 * rowNumber) * self.rad
            for node in list[rowNumber]:
                if node != None:
                    newNode = self.Node(node, x, y)
                    newNode.draw(self.screen, self.selectedNode)
                    self.nodes.append(newNode)
                rowVector.append((x, y))
                x = x + step
            coordinate.append(rowVector)
            rowNumber += 1

        rowNumber = 0
        collumn = 0

        for x in list:
            for y in x:
                if y != None:
                    if y.left != None:
                        self.line(
                            (
                                coordinate[rowNumber][collumn][0] - self.rad // 4,
                                coordinate[rowNumber][collumn][1] + 1.2 * self.rad,
                            ),
                            (
                                coordinate[rowNumber + 1][collumn * 2][0] + self.rad // 2,
                                coordinate[rowNumber + 1][collumn * 2][1] - self.rad // 2,
                            ),
                            y.left.color,
                        )
                    if y.right != None:
                        self.line(
                            (
                                coordinate[rowNumber][collumn][0] + 5 * self.rad // 4,
                                coordinate[rowNumber][collumn][1] + 1.2 * self.rad,
                            ),
                            (
                                coordinate[rowNumber + 1][collumn * 2 + 1][0] + self.rad // 2,
                                coordinate[rowNumber + 1][collumn * 2 + 1][1] - self.rad // 2,
                            ),
                            y.right.color,
                        )
                collumn += 1
            rowNumber += 1
            collumn = 0
        return pygame.display.update()

    def treeToGraph(self, node):
        self.listToGraph(self.treeToList(node))

    def printList(self, list):
        print("-------------------")
        for x in list:
            lstring = ""
            for y in x:
                if y != None:
                    lstring = lstring + y.key + " ,"
                else:
                    lstring = lstring + " " + " ,"
            
            print(lstring)

    def clear(self):
        self.screen.fill(self.backgroundColour)


    def selectNodeAtCoord(self,x,y): #returns a node at the given coordinates
        if self.selectedNode is not None:
            self.selectedNode = None

        for node in self.nodes:
            difX = node.x - x
            difY = node.y - y
            distance = math.sqrt(difX ** 2 + difY ** 2)
            if distance <= node.rad * 2:
                self.selectedNode = node
                return node
        return None

    def line(self, cord1, cord2, isRed):
        color = (0, 0, 0)
        if isRed:
            color = (255, 0, 0)
        gfxdraw.aapolygon(
            self.screen, [cord1, cord1 + (0, 1), cord2, cord2 + (0, 1)], color
        )

    def circle(self, r, g, b, x, y, rad):
        pygame.draw.circle(
            self.screen,
            (r, g, b),
            (int(x * self.width), int(y * self.height)),
            int(rad * self.width),
        )
