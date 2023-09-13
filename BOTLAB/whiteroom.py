from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math
# import pygame 
import numpy as np
from sklearn.preprocessing import normalize

from quaternion import Quaternion as qt
from jax import grad,jacobian
from pyassimp import load

position = [1000,1000,1000]
heading = []
position = [position[0],position[1],position[2]]



mesh_pin100 = []
mesh_pin150 = []
mesh_pin200 = []


def loadStl_pin100():
    global mesh_pin100
    with load('./stls/pin100.stl') as scene:
        assert len(scene.meshes)
        mesh_pin100 = scene.meshes[0]

def renderStl_pin100():
        glBegin(GL_LINES); 
        for v in mesh_pin100.vertices:
          glVertex3fv(v);      
        glEnd(); 




def loadStl_pin150():
    global mesh_pin150
    with load('./stls/pin150.stl') as scene:
        assert len(scene.meshes)
        mesh_pin150 = scene.meshes[0]

def renderStl_pin150():
        glBegin(GL_LINES); 
        for v in mesh_pin150.vertices:
          glVertex3fv(v);      
        glEnd(); 




def loadStl_pin200():
    global mesh_pin200
    with load('./stls/pin200.stl') as scene:
        assert len(scene.meshes)
        mesh_pin200 = scene.meshes[0]

def renderStl_pin200():
        glBegin(GL_LINES); 
        for v in mesh_pin200.vertices:
          glVertex3fv(v);      
        glEnd(); 


loadStl_pin100();
loadStl_pin150();
loadStl_pin200();


# print(len(mesh.vertices))
# print(mesh.vertices)    
# print(dir(stl_pin100.mesh));
# print(stl_pin100.args.count);
# print(stl_pin100.kwds.values);

class Haal(object):
    def __init__(self):
        self.rotation_Q = qt.from_axisangle(0.0,(0,0,1))
        self.position_P = [0,0,0]
    def locate(self,x,y,z):
        self.position_P = [x,y,z]

class Thing(object):
    def __init__(self,draw_function,draw_args):
        self.draw_function = draw_function
        self.draw_args = draw_args
        self.haal = Haal()
    def make(self):
        # Q_filterred = self.Q_filterred
        w, v = self.haal.rotation_Q.get_axisangle()
        w_degrees = w*180/math.pi
        location = self.haal.position_P
        glPushMatrix()
        glTranslatef(location[0],location[1],location[2])
        print(location)
        glRotatef(w_degrees,v[0],v[1],v[2])
        self.draw_function(*self.draw_args)
        glPopMatrix()
    def locate(self,x,y,z):
        self.haal.locate(x,y,z)

class Scene(object):
    def __init__(self):
        self.objects = []
        self.scenes = []
        self.scales = []
        self.coordinates = [0.,0.,0.]
    def add_object(self,thing):
        self.objects.append(thing)
    def add_scene(self,scene,x,y,z):
        self.scenes.append(scene)
        self.scales.append([x,y,z])
    def fix_position(self,coords):
        self.coordinates = coords
    def make_scene(self,depth=0):
        if depth > 10:
            return
        glPushMatrix()
        glTranslatef(self.coordinates[0],self.coordinates[1],self.coordinates[2])
        for o in self.objects:
            print(o)
            o.make()
        for s in range(len(self.scenes)):
            scale = self.scales[s]
            glPushMatrix()
            glScalef(scale[0],scale[1],scale[2])
            self.scenes[s].make_scene(depth+1)
            glPopMatrix()
        glPopMatrix()

thread_len1 = 1;
thread_len2 = 1;


def renderStl(model_name):
    return eval("renderStl" + "_" + model_name + "()");
# import numpy as np
class Gripper(object):
    def __init__(self):
        name = "box_gripper"
        # self.sections = [
        #     (0.5,0.25,2.),
        #     (0.35,0.15,1),
        # ]
        self.joints = []
        self.constraints = []
    def make_gripper(self,Mount_rotation,init_pos,init_rotation):
        global mesh
        # j1
        sections = [
            (-0,10,200),
            (-0,10,150),
            (-0,10,150),
            (-0,10,100),
        ]
        n = 90*math.pi/180;

        # glPushMatrix()


        glRotatef(Mount_rotation,0,0,1)
        glTranslatef(50,0,0)
        # w2, v2 = init_rotation.get_axisangle()
        # w2_degrees = w2*180/math.pi   

        # # j2
        # glPushMatrix()
        # glTranslatef(init_pos[0],init_pos[1],init_pos[2])
        # glRotatef(w2_degrees,v2[0],v2[1],v2[2])



        rotation_PI2X = qt.from_axisangle(n,(1,0,0))
        rotation_PI2Y = qt.from_axisangle(n,(0,1,0))
        rotation_PI2Z = qt.from_axisangle(n,(0,0,1))

        rotation_J1 = qt.from_axisangle(thread_len1,(0,1,0))
        rotation_J2 = qt.from_axisangle(thread_len2,(0,1,0))
        rotation_J2 = rotation_J1._multiply_with_quaternion(rotation_J2);

        rotation_PI2X = rotation_PI2X*rotation_PI2Z


        xa, xv = rotation_PI2X.get_axisangle()
        x_degrees = xa*180/math.pi
        ya, yv = rotation_PI2Y.get_axisangle()
        y_degrees = ya*180/math.pi
        za, zv = rotation_PI2Z.get_axisangle()
        z_degrees = za*180/math.pi


        k = 2 # 

        j_pos = [0,0,0]

        rotation_J = []
        for i in range(len(sections)):
            rotation_Jn = qt.from_axisangle(thread_len1*k/(k + i),(0,1,0))
            rotation_J.append(rotation_Jn)

        # rotation_J.append(rotation_Jn)
        # glPopMatrix();

        rotation_CURR = rotation_J[0];

        for i in range(len(sections)):

            w2, v2 = rotation_CURR.get_axisangle()
            w2_degrees = w2*180/math.pi   

            # j2
            glPushMatrix()
            glTranslatef(j_pos[0],j_pos[1],j_pos[2])
            glRotatef(w2_degrees,v2[0],v2[1],v2[2])
            glTranslatef(sections[i][0]/2,sections[i][1]/2,0)

            glRotatef(x_degrees,xv[0],xv[1],xv[2]);
            renderStl("pin" + str(sections[i][2]));
            glPopMatrix()
            

            j_pos = j_pos + rotation_CURR*sections[i]
            rotation_CURR = rotation_J[i]._multiply_with_quaternion(rotation_CURR);
            # j2_pos = j2_pos + rotation_J[i]*sections[i]

        # glPopMatrix();
        # 

    def makeContactPad():
        pass
        # glPushMatrix();


gp1 = Gripper();


# def bot_grab_arm():
#     glPushMatrix()
#     glScalef(0.5,0.25,2.)
#     glutWireCube(1.)


#     glScalef(0.5,0.25,2.)
#     glutWireCube(1.)




#     glPopMatrix()










rotation_PIby4 = qt.from_axisangle(0,(1,0,0))



_CELESTIAL_SPHERE_ = Thing(glutWireSphere,(.1,20,20))


# _BOT_GRABBER_1 = Thing(gp1.make_gripper,[0]);

SCENE_1 = Scene()



# SCENE_1.add_object(_CELESTIAL_SPHERE_)
# SCENE_1.add_object(_BOT_GRABBER_)
# SCENE_1.add_object(_BOT_GRABBER_1)

glist = [ 0 , 90 , 180, 270 ]
glist.extend([ 0  + 45, 90  + 45, 180 + 45, 270 + 45 ])

for i in glist:     
    _BOT_GRABBER_2 = Thing(gp1.make_gripper,[i,[100,100,100],rotation_PIby4]);
    SCENE_1.add_object(_BOT_GRABBER_2)
# SCENE_1.add_object(_CUBE_2)
# SCENE_1.add_object(_PLANE_)


SCENE_1.fix_position([0,0,0])

SCENE_TWO_ADJACENT_CUBES = Scene()
SCENE_TWO_ADJACENT_CUBES.add_scene(SCENE_1,1,1,1)

SCENE_TABLE = Scene()




class Room(object):
    def __init__(self,DRAW_SCENE):
        self.window_name = "Empty"
        self.camera_heading = [0,0,0]
        self.window_function()
        self.DRAW_SCENE = DRAW_SCENE
    def update(self):
        self.draw_function()
    def look_at_scene(self):
        # glMatrixMode(GL_PROJECTION)
        d = math.sqrt(sum([x*x for x in position]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.,1.,d/100.,4*d)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(position[0],position[1],position[2],
          0,0,0,
          0,0,1)
    def draw_room(self):
        glPushMatrix()
        # glTranslatef(position[0],position[1],position[2])
        glutWireCube(1000.0)
        glPopMatrix()
    def keyboard_funtion(self,*args):
        global position,thread_len1,thread_len2
        d = math.sqrt(sum([x*x for x in position]))
        key = str(args[0],'utf-8')
        print(key)
        if key == ' ':
            snap_zero = True
        if key == 'w':
            position = [position[0]*(1-0.1),position[1]*(1-0.1),position[2]*(1-0.1)]
        if key == 's':
            position = [position[0]*(1+0.1),position[1]*(1+0.1),position[2]*(1+0.1)]
        if key == 'd':
            position = np.add(position,np.cross(position,[0,0,1])*0.1)
        if key == 'a':
            position = np.subtract(position,np.cross(position,[0,0,1])*0.1)
        if key == 'r':
            position = [2,2,0]
        if key == '\'':
            thread_len1 += 0.1
        if key == '/':
            thread_len1 -= 0.1
        if key == ';':
            thread_len2 += 0.1
        if key == '.':
            thread_len2 -= 0.1
        print(key)
        print("\t\tThread len 1: %f",thread_len1)
        print("\t\tThread len 2: %f",thread_len2)
        # print(position)
    def draw_display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        color = [1.0,0.,0.,1.]
        self.look_at_scene()
        glPushMatrix()
        self.draw_room()
        self.DRAW_SCENE.make_scene()
        glPopMatrix()
        glutSwapBuffers()
        return
    def window_function(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(300,300)
        glutCreateWindow(self.window_name)

        glClearColor(0.,0.,0.,1.)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glutKeyboardFunc(self.keyboard_funtion)
        glutDisplayFunc(self.draw_display)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(40.,1.,1.,40.)
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0,0,10,
                  0,0,0,
                  0,1,1)
        glPushMatrix()
        # glutMainLoop()
        return
    def draw_function(self):
        glutPostRedisplay()
        glutMainLoopEvent()

R = Room(SCENE_TWO_ADJACENT_CUBES)
while 21:
    R.update()
    for i in range(1000000):
        pass