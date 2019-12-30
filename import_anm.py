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
            for trans_frame_num in bone.translations.Keys:
                translation = bone.translations.Keys[trans_frame_num]
                # bpy.context.scene.frame_set(trans_frame_num)

                pose.bones[bone.name].location = [translation.X, translation.Y, translation.Z]
                pose.bones[bone.name].keyframe_insert(data_path="location", index = -1, frame = trans_frame_num)

                # print("frame %s" % (trans_frame_num))
                # print("location %s" % (pose.bones[bone.name].location))

            for rot_frame_num in bone.rotations.Keys:
                rotation = bone.rotations.Keys[rot_frame_num]
                # bpy.context.scene.frame_set(rot_frame_num)

                pose.bones[bone.name].rotation_quaternion = [rotation.X, rotation.Y, rotation.Z, rotation.W]
                pose.bones[bone.name].keyframe_insert(data_path="rotation_quaternion", index = -1, frame = rot_frame_num)

                # print("frame %s" % (rot_frame_num))
                # print("rotation %s" % (pose.bones[bone.name].rotation_quaternion))

            #for x in range(bone.num_scales - 1):
            #    frame_num = bone.scales.FrameNum[x]
            #    bpy.context.scene.frame_set(frame_num)

            #    key = bone.scales.Keys[x]
            #    pose.bones[bone.name].scale =[key.X, key.Y, key.Z]

            #    pose.bones[bone.name].keyframe_insert(data_path="scale", index = -1, frame = frame_num)

            #    print("frame %s" % (frame_num))
            #    print("scale %s" % (pose.bones[bone.name].location))
        else:
            print("bone doesn't exist in pose")

    print("finished adding animation")

    return True
