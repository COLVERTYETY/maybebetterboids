import pygame as py
import numpy as np


class boid(object):
    SURFACE = py.Surface((10,10))  # pylint: disable=too-many-function-args
    ARRAY=[]
    def __init__(self,x,y):
        self.pos=Vector(x,y)
        self.vel=Vector(0,0)
        self.acc=Vector(0,0)
        self.maxspeed=2
        self.maxforce=0.2
        self.shape="line"
        self.radius=5
        self.vrange=300
        self.color=(42, 180, 235)
        boid.ARRAY.append(self)

    def center(self,strength):
        (w, h) = boid.SURFACE.get_size()
        # arenasize = 200
        # arena = Vector(w/2,h/2)
        # arena-=self.pos
        # dist = arena.norm()
        # if dist>arenasize:
        #     arena.autonorm((dist-arenasize)*strength)
        #     self.vel+=arena
        self.pos.x=(self.pos.x+w)%w
        self.pos.y =(self.pos.y+h)%h

    def apply(self):
        self.center(self.maxspeed/300)
        self.vel+=self.acc
        #limit
        if self.vel.norm()>self.maxspeed:
            self.vel.autonorm(self.maxspeed)
        self.pos+=self.vel
        self.pos.x=self.pos.x
        self.pos.y=self.pos.y
        self.acc=Vector(0,0)
        
    def align(self,arr):
        steering=Vector(0,0)
        total=0
        avg_vec=Vector(0,0)
        for i in arr:
            dis=i.pos-self.pos
            if dis.norm()<self.vrange and i!=self:
                avg_vec+=i.vel
                total+=1
        if total>0:
            avg_vec.div(total)
            avg_vec.autonorm(self.maxspeed)
            steering= avg_vec -self.vel
        return steering

    def cohesion(self,arr):
        steering = Vector(0,0)
        total = 0  
        avg_pos = Vector(0,0)
        for i in arr:
            dis=i.pos-self.pos
            if dis.norm()<self.vrange:
                avg_pos+=i.pos
                total+=1
        if total> 0 :
            avg_pos.div(total)
            tempvec = avg_pos - self.pos
            py.draw.line(boid.SURFACE,(255,0,0),(self.pos.tint()),(avg_pos.tint()))
            if tempvec.norm()>0.01:
                tempvec.autonorm(self.maxspeed)
            steering = tempvec - self.vel
            if steering.norm()>self.maxforce:
                steering.autonorm(self.maxforce)
        return steering

    def separation(self,arr):
        steering = Vector(0,0)
        total=0
        avg_vect = Vector(0,0)
        for i in arr:
            dis=i.pos-self.pos
            if dis.norm()<self.vrange and self.pos!=i.pos:
                diff = self.pos - i.pos
                diff.div(dis.norm())
                avg_vect+=diff
                total+=1
        if total>0:
            avg_vect.div(total)
            avg_vect.autonorm(self.maxspeed)
            steering = avg_vect - self.vel
            if steering.norm()>self.maxforce:
                steering.autonorm(self.maxforce*2)
        return steering


    def draw(self):
        if self.shape == "circle":
            py.draw.circle(boid.SURFACE,self.color,self.pos.tint(),int(self.radius))
        if self.shape == "line":
            vecc=self.pos+self.vel
            py.draw.line(boid.SURFACE,self.color,self.pos.tint(),vecc.tint(),1)
        py.draw.circle(boid.SURFACE,(0,255,0),(self.pos.tint()),int(self.vrange/2),1)

    @staticmethod
    def generaterandompos(quantity):
        (w, h) = boid.SURFACE.get_size()
        for _ in range(quantity):
            boid(np.random.random_integers(0,w),np.random.random_integers(0,h))

    @staticmethod 
    def drawall():
        for i in boid.ARRAY:
            #alignement = i.align(boid.ARRAY)
            cohesion = i.cohesion(boid.ARRAY)
            #separation = i.separation(boid.ARRAY)
            i.acc+=cohesion
            i.apply()
            i.draw()








class Vector():
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def norm(self):
        return np.sqrt((self.x*self.x)+(self.y*self.y))

    def autonorm(self,mult=1):
            self.x=(self.x/self.norm())*mult
            self.y=(self.y/self.norm())*mult

    def __add__(self,other):
        return Vector(self.x+other.x,self.y+other.y)

    def __sub__(self,other):
        return Vector(self.x-other.x,self.y-other.y)

    def __mul__(self, other):
        return self.x*other.y-other.x*self.y 
    
    def __ne__(self,other):
        return (self.x!=other.x) and (self.y!=other.y)
       
    def tint(self):
        return (int(self.x),int(self.y))

    def tfloat(self):
        return (self.x,self.y)

    def div(self,l):
        self.x/=l
        self.y/=l
