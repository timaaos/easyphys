import easyphys
from easyphys import Vector2,Color
from easyphys import StaticObject,PhysicObject,InteractivePhysicObject # default object classes

class Box(PhysicObject): # example physic object
    def __init__(self, x, y,width=50,height=50):
        super().__init__(x, y,width,height)

class BoomBox(InteractivePhysicObject): # example interactive physic object
    def __init__(self, x, y,width=50,height=50):
        super().__init__(x, y,width,height)
        self.color = Color(255,60,60)
        self.boomtimer = -1
        self.booming = False
    def click(self):
        if self.booming == True:
            return
        self.velocity = self.velocity.add(Vector2(0,-0.5))
        self.boomtimer = 0.7
        self.booming = True
    def simulate(self):
        super().simulate()
        if self.hover == True:
            self.color = Color(255,120,120)
        else:
            self.color = Color(255,60,60)
        self.boomtimer -= self.getDeltaTime()
        if self.boomtimer < 0 and self.booming:
            self.remove()

winScaleY = 450
winScaleX = 800

floor = StaticObject(0,winScaleY-50,winScaleX,50)

myPhysObj = PhysicObject(150,0,100,75)
myBox = Box(10,0)
myBoomBox = BoomBox(80,0)
bigBoomBox = BoomBox(300,0,100,100)
bigBoomBox.mass = 1.5

physwin = easyphys.PhysWindow(Vector2(winScaleX,winScaleY))
physwin.run()