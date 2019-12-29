import sys

sys.path.append('H:/Blender/IO_Enfusion_Blender')
sys.path.append('__path__')

import bpy
import bmesh
import os
import array
from mathutils import *
from math import *

import anm

def load(self, context, filepath=""):
    ob = bpy.context.object
    scene = bpy.context.scene
    anim_name = os.path.splitext(os.path.basename(filepath))[0]

    try:
        file = open(filepath, "rb")
    except IOError:
        print("Could not open file for reading:\n %s" % filepath)
        return

    animation = anm.ANM()
    animation.load(filepath, file)

    try:
        file = open(filepath, "rb")
    except IOError:
        print("Could not open file for reading:\n %s" % filepath)
        return
    

if __name__ == "__main__":
    load(None, None, "P:/DZ/anims/anm/player/attacks/2hd/p_2hd_light_erc_attack_L_02.anm")