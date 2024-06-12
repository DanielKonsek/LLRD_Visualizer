import pygame
from pygame import gfxdraw


class Renderer:
    font = None
    rad = 16

    def __init__(
        self,
        width,
        height,
        caption="Graph-plot",
        rad=16,
        backgroundColour=(255, 255, 255),
    ):
        pygame.display.init()
        pygame.init()
        self.backgroundColour = backgroundColour
        self.width = width
        self.height = height
        self.rad = rad
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)
        self.screen.fill(self.backgroundColour)
        pygame.display.flip()
        self.font = pygame.font.SysFont(None, 2 * self.rad)

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
        row = 0

        for node in list:
            rowVector = []
            step = self.width // (pow(2, row) + 1)
            x = step - self.rad // 2
            y = (4 + 6 * row) * self.rad
            for z in list[row]:
                if z != None:
                    self.node(z.key, x, y, z.color)
                rowVector.append((x, y))
                x = x + step
            coordinate.append(rowVector)
            row = row + 1

        row = 0
        collumn = 0

        for x in list:
            for y in x:
                if y != None:
                    if y.left != None:
                        self.line(
                            (
                                coordinate[row][collumn][0] - self.rad // 4,
                                coordinate[row][collumn][1] + 1.2 * self.rad,
                            ),
                            (
                                coordinate[row + 1][collumn * 2][0] + self.rad // 2,
                                coordinate[row + 1][collumn * 2][1] - self.rad // 2,
                            ),
                            list[row + 1][collumn * 2].color,
                        )
                    if y.right != None:
                        self.line(
                            (
                                coordinate[row][collumn][0] + 5 * self.rad // 4,
                                coordinate[row][collumn][1] + 1.2 * self.rad,
                            ),
                            (
                                coordinate[row + 1][collumn * 2 + 1][0] + self.rad // 2,
                                coordinate[row + 1][collumn * 2 + 1][1] - self.rad // 2,
                            ),
                            list[row + 1][collumn * 2 + 1].color,
                        )
                    collumn = collumn + 1
            row = row + 1
            collumn = 0
        return pygame.display.update()

    def treeToGraph(self, node):
        self.listToGraph(self.treeToList(node))

    def printList(self, list):
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

    def blit(self, img, x, y):
        self.screen.blit(img, (x, y))

    def node(self, key, x, y, isRed):
        color = (0, 0, 0)
        if isRed:
            color = (255, 0, 0)

        img = self.font.render(key, True, color)
        self.blit(img, x, y)
        gfxdraw.circle(
            self.screen,
            x + int(self.rad // 2),
            y + int(self.rad // 2),
            self.rad,
            color,
        )
        gfxdraw.circle(
            self.screen,
            x + int(self.rad // 2),
            y + int(self.rad // 2),
            self.rad + 1,
            color,
        )

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
