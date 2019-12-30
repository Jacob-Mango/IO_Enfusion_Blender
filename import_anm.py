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

    print("finished reading anm")

    obj = bpy.data.objects["DayZCharacter"]
    pose = obj.pose
    # bpy.context.scene.objects.active = obj

    for idx in animation.bones():
        bone = animation.bones()[idx]

        print("processing bone %s" % (bone.name))
        if bone.name in pose.bones:
            for x in range(bone.num_translations):
                frame_num = bone.translations.FrameNum[x]
                bpy.context.scene.frame_set(frame_num)

                key = bone.translations.Keys[x]
                pose.bones[bone.name].location =[key.X, key.Y, key.Z]

                pose.bones[bone.name].keyframe_insert(data_path="location", index = -1, frame = frame_num)

                print("frame %s" % (frame_num))
                print("location %s" % (pose.bones[bone.name].location))
        else:
            print("bone doesn't exist in pose")

    print("finished adding animation")

    return True
