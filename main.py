#spend money to build on lot
#industrial - more money but less housing - slows pop growth by 0.1x
#residential - more housing but less money - slows pop growth by 0.05x
#slum (randomly generated - more of them as housing pressure increases) - no contributions (essentially dead lot)

import pygame
import os

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 30)

WIDTH, HEIGHT = 900, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Running out of space")

#width 60px height 40px
class Lot:
    def __init__(self, pos):
        self.type = None
        self.pos = pos
        self.buildable = True
    
    #print the pos of lot for debug
    def __str__(self):
        return str((self.pos[0], self.pos[1]))
    
    def build(self, type):
        if self.type == "slum":
            return

        if type == "residential":
            self.type = "residential"
            self.buildable = False
        elif type == "industrial":
            self.type = "industrial"
            self.buildable = False
    
    def draw(self):
        if self.type:
            colour = ()
            if self.type == "slum":
                colour = (255, 0, 0)
            elif self.type == "residential":
                colour = (0, 255, 0)
            elif self.type == "industrial":
                colour = (0, 0, 255)
            pygame.draw.rect(window, colour, pygame.Rect(self.pos[0], self.pos[1], 60, 40))
            
def createGrid():
    global lotPoss
    xs = [140, 220, 300, 380, 460, 540, 620, 700]
    ys = [20, 80, 140, 200, 260, 320, 380, 440]
    lotPoss = []
    grid = []
    for x in xs:
        for y in ys:
            grid.append(Lot((x, y)))
            lotPoss.append((x, y))
    return grid

#returns the amount of each lot type
def getLotNos(grid):
    slumCount = 0
    resCount = 0
    indusCount = 0
    for i in grid:
        if i.type == "slum":
            slumCount += 1
        elif i.type == "residential":
            resCount += 1
        elif i.type == "industrial":
            indusCount += 1
    return slumCount, resCount, indusCount

def drawMainMenu():
    window.fill((85,212,0))
    pygame.draw.rect(window, (70, 70, 70), pygame.Rect(350, 250, 200, 100))
    playTxt = font.render("Play", True, (255, 255, 255))
    window.blit(playTxt, (425, 290))

def drawWin(grid, money):
    bg = pygame.image.load(os.path.join("assets", "bg.png"))
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    window.blit(bg, (0, 0))
    for i in grid:
        i.draw()
    moneyTxt = font.render(str(money), True, (0, 0, 0))
    window.blit(moneyTxt, (5, 5))
    popTxt = font.render(str(population), True, (0, 0, 0))
    window.blit(popTxt, (5, 25))

def main():
    #make an array that represents the grid
    #yes i know i should use a 2d array but that's too much effort for me
    grid = createGrid()
    PUPos = (0, 0)

    #initalise starting values
    money = 10000
    global population
    population = 0
    global housingPress
    housingPress = 0
    industrialPress = 0
    growthSpeed = 1

    #keep track of the current stage
    stageCount = 0

    #timer to update the population etc. every second
    update = pygame.USEREVENT + 0
    pygame.time.set_timer(update, 1000)

    running = True
    while running:
        if stageCount == 0:
            drawMainMenu()
        else:
            drawWin(grid, money)

        moveBuildPU = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #update population and stuff
            #this does not work yet
            elif stageCount == 1 and event.type == update:
                population += round(100 * growthSpeed)
                growthSpeed += 0.01
                slumCount, resCount, indusCount = getLotNos(grid)
                if growthSpeed < 0: growthSpeed = 0
                print(growthSpeed)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if stageCount == 0 and 350 <= mouseX <= 550 and 250 <= mouseY <= 350:
                    stageCount += 1
                elif stageCount == 1:
                    if PUPos[0] <= mouseX <= PUPos[0]+50 and PUPos[1] <= mouseY <= PUPos[1]+65:
                        lotPos = (PUPos[0]+20, PUPos[1]+50)
                        for i in grid:
                            if i.pos == lotPos and i.buildable:
                                i.build("residential")
                                money -= 1000
                        #don't move the build pop-up if it's clicked but the mouse is over another lot
                        moveBuildPU = False
                    elif PUPos[0]+50 <= mouseX <= PUPos[0]+100 and PUPos[1] <= mouseY <= PUPos[1]+65:
                        lotPos = (PUPos[0]+20, PUPos[1]+50)
                        for i in grid:
                            if i.pos == lotPos and i.buildable:
                                i.build("industrial")
                                money -= 1000
                        moveBuildPU = False

                    if moveBuildPU:
                        #initialise build pop-up
                        for i in lotPoss:
                            #i[0] is the x, i[1] is the y
                            if i[0] <= mouseX <= i[0]+60 and i[1] <= mouseY <= i[1]+40:
                                for j in grid:
                                    if j.pos == (i[0], i[1]):
                                        PUPos = (j.pos[0]-20, j.pos[1]-50)
                         
        #draw build pop-up
        if stageCount == 1 and PUPos != (0, 0):
            buildPU = pygame.image.load(os.path.join("assets", "buildPU.png"))
            buildPU = pygame.transform.scale(buildPU, (100, 65))
            window.blit(buildPU, PUPos)

        pygame.display.update()

if __name__ == "__main__":
    main()
