import math
import pyray as pr
_objects = []
class Vector2():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def add(self,toadd):
        return Vector2(self.x+toadd.x,self.y+toadd.y)
    def getFloor(self):
        return Vector2(math.floor(self.x),math.floor(self.y))
    def getInvert(self):
        return Vector2(-self.x,-self.y)
    def __repr__(self):
        return f"vec2, x: {str(self.x)}, y: {str(self.y)}"
    def collides(self,otherObj):
        point = self
        if point.x >= otherObj.position.x and point.x <= otherObj.position.x+otherObj.size.x:
            if point.y >= otherObj.position.y and point.y <= otherObj.position.y+otherObj.size.y:
                return True
        return False

class Color():
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b
        self.a = 255
    def getPyRay(self):
        return pr.Color(self.r,self.g,self.b,self.a)

class PhysicObject():
    def __init__(self,x,y,width,height):
        self.position = Vector2(x,y)
        self.size = Vector2(width,height)
        self.velocity = Vector2(0,0)
        self.mass = 1
        self.color = pr.Color(255,255,255,255)
        self.active = True
        self.add()
    def getDeltaTime(self):
        return pr.get_frame_time()
    def add(self):
        global _objects
        _objects.append(self)
    def remove(self):
        global _objects
        _objects.remove(self)
    def draw(self):
        col = self.color
        if type(col) == Color:
            col = col.getPyRay()
        pr.draw_rectangle(self.position.getFloor().x,self.position.getFloor().y,self.size.x,self.size.y,col)
    def simulate(self):
        if self.active == False:
            return
        dt = pr.get_frame_time()
        self.velocity.y += dt*self.mass
        self.position = self.position.add(self.velocity)
        global _objects
        for object in _objects:
            if object == self:
                continue
            if self.collides(object) == True:
                self.position = self.position.add(self.velocity.getInvert())
                self.velocity.y = 0
                break
    def collides(self,other):
        points = []
        points.append(self.position)
        points.append(self.position.add(self.size))
        for point in points:
            if point.x >= other.position.x and point.x <= other.position.x+other.size.x:
                if point.y >= other.position.y and point.y <= other.position.y+other.size.y:
                    return True
        return False
class InteractivePhysicObject(PhysicObject):
    def __init__(self, x, y,width,height):
        super().__init__(x, y,width,height)
        self.hover = False
    def click(self):
        pass

class StaticObject(PhysicObject):
    def __init__(self, x, y,width,height):
        super().__init__(x, y,width,height)
    def simulate(self):
        dt = pr.get_frame_time()

def getMouseVector2():
    return Vector2(pr.get_mouse_x(),pr.get_mouse_y())

def castMouseRay():
    mousePos = getMouseVector2()
    for object in _objects:
        if mousePos.collides(object) == True:
            return object
    return None
class PhysWindow():
    def __init__(self,winScale):
        self.winScale = winScale
        self.title = "EasyPhysics"
    def run(self):
        background = pr.Color(0, 0, 0,255)
        pr.init_window(self.winScale.x, self.winScale.y, self.title)
        while not pr.window_should_close():
            self.winScale.x,self.winScale.y = pr.get_screen_width(),pr.get_screen_height()
            pr.begin_drawing()
            pr.clear_background(background)
            for object in _objects:
                object.simulate()
                object.draw()
                try:
                    object.hover = False
                except:
                    pass
            castData = castMouseRay()
            if castData != None:
                try:
                    if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
                        castData.click()
                    castData.hover = True
                except:
                    pass
            pr.end_drawing()
        pr.close_window()
