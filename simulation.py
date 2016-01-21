from Graphics import *
import random

class World(object):

    def __init__(self, nR, nW):
        ''' Create a simulated world with nR rabbits and nW wolves '''
        self.display = True
        self.nR = nR
        self.nW = nW
        self.animals = []

        self.win = Window("simulation", 400, 400)
        self.win.setBackground(Color("white"))

        self.gwin = Window("population size", 1000, 300)

        for i in range(nR):
            r = Rabbit(self)

        for i in range(nW):
            w = Wolf(self)
           
    def addAnimal(self, w):
        self.animals.append(w)
        
    def nearbyAnimals(self, a):
        ''' find all the nearby animals within sensing range of a'''
        nearby = []
        for o in self.animals:
            if o.alive and a.distance(o) < a.SENSING_RANGE and o != a:
                nearby.append(o)

        return nearby

    def closestNeighbor(self, a, t):
        ''' find the closest animal to animal a of type t; 
            return None if no closest exists'''
        closestDistance = 100000000
        neighbor = None
        for o in self.nearbyAnimals(a):
            if isinstance(o, t) and a.distance(o) < closestDistance:
                neighbor = o
                closestDistance = a.distance(o)
        return neighbor
               
    def run(self):
        ''' run the simulated world '''

        t = 0
        while t < self.gwin.getWidth() and self.nR > 0 and self.nW > 0:

            self.nR = 0
            self.nW = 0
            for a in self.animals:
                if a.alive:
                    a.takeAStep()
                    if isinstance(a, Rabbit):
                        self.nR += 1
                    elif isinstance(a, Wolf):
                        self.nW += 1
                else:                
                    self.animals.remove(a)
                    
            pr = Circle((t, self.gwin.getHeight() - self.nR), 1)
            pr.color = Color("blue")
            pr.draw(self.gwin)

            pw = Circle((t, self.gwin.getHeight() - self.nW), 1)
            pw.color = Color("red")
            pw.draw(self.gwin)

            t = t + 1
    
        print ("Simulation Done")

class Animal(object):
    SIZE = 5
    SENSING_RANGE = 30

    def __init__(self, world):
        ''' Create a new Animal'''
        self.world = world
        self.alive = True
        self.vx = 4
        self.vy = 4
        self.reproduction_prob = 0.02
        self.x = random.uniform(0, self.world.win.getWidth())
        self.y = random.uniform(0, self.world.win.getHeight())
        self.size = self.SIZE
        self.world.addAnimal(self)
        self.setAppearance()
    
    def setAppearance(self):
        self.appearance = Circle(Point(self.x, self.y), self.size)
        if self.world.display:
            self.appearance.draw(self.world.win)
    
    def eat(self):
        pass

    def reproduce(self):
        pass

    def die(self):
        '''remove this animal from the population'''
        if self.world.display:
            self.appearance.undraw()
        self.alive = False

    def takeAStep(self):
        ''' move the animal for one timestep'''
        dx = random.uniform(-self.vx, self.vx)
        dy = random.uniform(-self.vy, self.vy)
        if self.insideWindow(dx, dy):
            self.x = self.x + dx
            self.y = self.y + dy
            self.appearance.move(dx,dy)

    def distance(self, other):
        ''' find the distance between myself and the other animal'''
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    def insideWindow(self, dx, dy):
        ''' check to see if moving animal by (dx, dy) keeps it in the window'''
        tx = self.x + dx
        ty = self.y + dy
        if self.size/2 < tx < self.world.win.getWidth() - self.size/2 and\
           self.size/2 < ty < self.world.win.getHeight() - self.size/2:
            return True
        else:
            return False
                
    def __str__(self):
        return "Animal at (%d, %d)" % (self.x, self.y)

class Rabbit(Animal):

    SIZE = 7

    def __init__(self, world):
        Animal.__init__(self,world)
        self.reproduction_prob = 0.06

    def reproduce(self):
        rand = random.uniform(0,1)
        if rand <= self.reproduction_prob:
            Rabbit(self.world)

    def takeAStep(self):
        Animal.takeAStep(self)
        self.reproduce()

    def setAppearance(self):
        self.appearance = Circle(Point(self.x, self.y), self.size)
        self.appearance.color = Color("Blue")
        if self.world.display:
            self.appearance.draw(self.world.win)

class Wolf(Animal):

    hunger = 15
    SIZE = 10
    SENSING_RANGE = 30

    def __init__(self, world):
        Animal.__init__(self,world)
        self.reproduction_prob = 0.05

    def reproduce(self):
        rand = random.uniform(0,1)
        if rand <= self.reproduction_prob and self.hunger > 1.5:
            Wolf(self.world)

    def eat(self):
        self.hunger = self.hunger + 4

    def setAppearance(self):
        self.appearance = Circle(Point(self.x, self.y), self.size)
        self.appearance.color = Color("Red")
        if self.world.display:
            self.appearance.draw(self.world.win)

    def takeAStep(self):
        Animal.takeAStep(self)
        self.reproduce()
        self.hunger=self.hunger-1
        n=self.world.closestNeighbor(self, Rabbit)
        if n != None:
            if self.distance(n) <= self.SENSING_RANGE:
                self.eat()
                World.closestNeighbor(self.world, self, Rabbit).die()
        if self.hunger <= 0:
            self.die()

random.seed(15)
w = World(40, 20)
w.run()
