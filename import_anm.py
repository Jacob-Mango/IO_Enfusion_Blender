import bpy
import bmesh
import os
import array
from mathutils import *
from math import *

import anm

def read(self, context, filepath=""):
    ob = bpy.context.object
    scene = bpy.context.scene
    anim_name = os.path.splitext(os.path.basename(filepath))[0]

    try:
        file = open(filepath, "rb")
    except IOError:
        print("Could not open file for reading:\n %s" % filepath)
        return

    animation = anm.ANM()
    animation.read(filepath, file)

    try:
        file = open(filepath, "rb")
    except IOError:
        print("Could not open file for reading:\n %s" % filepath)
        return False

    return True
