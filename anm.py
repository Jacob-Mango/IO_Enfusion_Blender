import time
import struct
import bpy

class ANMKey(object):
    X = 0
    Y = 0
    Z = 0
    W = 0

class ANMKeys(object):
    FrameNum = {}
    Keys = {}

    def read(self, path, file, version, num, amount, bias, multipler):
        self.FrameNum = struct.unpack("=%dh" % (1 * num), file.read(2 * num))

        for x in range(num):
            data = struct.unpack("=%dh" % (amount), file.read(2 * amount))
            self.Keys[x] = ANMKey()
            self.Keys[x].X = (data[0] * multipler) + bias
            if amount > 1:
                self.Keys[x].Y = (data[1] * multipler) + bias
            if amount > 2:
                self.Keys[x].Z = (data[2] * multipler) + bias
            if amount > 3:
                self.Keys[x].W = (data[3] * multipler) + bias

    def write(self, path, file, version):
        print("not implemented")

class ANMBone(object):
    name = ""
    translation_bias = 0.0
    translation_multiplier = 0.0
    rotation_bias = 0.0
    rotation_multiplier = 0.0
    scale_bias = 0.0
    scale_multiplier = 0.0
    num_frames = 0
    num_translations = 0
    num_rotations = 0
    num_scales = 0
    translations = ANMKeys()
    rotations = ANMKeys()
    scales = ANMKeys()
    flag = 0

    def read(self, path, file, version):
        if version == 5:
            self.name = file.read(32).decode("utf-8")
        
        self.translation_bias = struct.unpack("=f", file.read(4))[0]
        self.translation_multiplier = struct.unpack("=f", file.read(4))[0]

        self.rotation_bias = struct.unpack("=f", file.read(4))[0]
        self.rotation_multiplier = struct.unpack("=f", file.read(4))[0]

        if version >= 6:
            self.scale_bias = struct.unpack("=f", file.read(4))[0]
            self.scale_multiplier = struct.unpack("=f", file.read(4))[0]

        self.num_frames = struct.unpack("=H", file.read(2))[0]

        self.num_translations = struct.unpack("=H", file.read(2))[0]

        self.num_rotations = struct.unpack("=H", file.read(2))[0]

        if version >= 6:
            self.num_scales = struct.unpack("=H", file.read(2))[0]

        self.flag = file.read(1)[0]

        if version == 5:
            file.read(1)
        elif version >= 6:
            len = file.read(1)[0] # struct.unpack("=h", file.read(2))[0]
            self.name = file.read(len).decode("utf-8")

        print("name: " + self.name)
        # print("translation_bias: " + str(self.translation_bias))
        # print("translation_multiplier: " + str(self.translation_multiplier))
        # print("rotation_bias: " + str(self.rotation_bias))
        # print("rotation_multiplier: " + str(self.rotation_multiplier))
        # print("scale_bias: " + str(self.scale_bias))
        # print("scale_multiplier: " + str(self.scale_multiplier))
        print("num_frames: " + str(self.num_frames))
        print("num_translations: " + str(self.num_translations))
        print("num_rotations: " + str(self.num_rotations))
        print("num_scales: " + str(self.num_scales))
        print("flag: " + str(self.flag))
        print("\n")

    def write(self, path, file, version):
        print("not implemented")

class ANMHEAD(object):
    anm = None
    bones = {}

    def __init__(self, _anm=None):
        self.anm = _anm

    def read(self, path, file, version):
        form = file.read(4).decode("utf-8")
        if form != "HEAD":
            raise RuntimeError("Didn't find HEAD at expected place")

        bytes_remaining = struct.unpack(">i", file.read(4))[0]
        target_position = file.tell() + bytes_remaining

        idx = 0
        while file.tell() < target_position:
            self.bones[idx] = ANMBone()
            self.bones[idx].read(path, file, version)
            idx = idx + 1

    def write(self, path, file, version):
        print("not implemented")

class ANMDATA(object):
    anm = None

    def __init__(self, _anm=None):
        self.anm = _anm

    def read(self, path, file, version):
        form = file.read(4).decode("utf-8")
        if form != "DATA":
            raise RuntimeError("Didn't find DATA at expected place")

        bytes_remaining = struct.unpack(">i", file.read(4))[0]

        for idx in self.anm.bones():
            bone = self.anm.bones()[idx]
            bone.translations.read(path, file, version, bone.num_translations, 3, bone.translation_bias, bone.translation_multiplier)
            bone.rotations.read(path, file, version, bone.num_rotations, 4, bone.rotation_bias, bone.rotation_multiplier)
            bone.scales.read(path, file, version, bone.num_scales, 3, bone.scale_bias, bone.scale_multiplier)

    def write(self, path, file, version):
        print("not implemented")

class ANM(object):    
    version = 0
    fps = 0
    head = None
    data = None

    def bones(self):
        return self.head.bones

    def read(self, path, file):
        form = file.read(4).decode("utf-8")
        if form != "FORM":
            raise RuntimeError("File type not FORM")
        
        file.read(4)

        animset = file.read(7).decode("utf-8")

        print(animset)

        self.version = 5
        str_version = file.read(1).decode("utf-8")
        self.version = int(str_version)

        print(self.version)

        file.read(4)

        bytes = b''
        b = file.read(1)
        while not b == b'\x00':
            bytes += b
            b = file.read(1)

        file.read(4)

        self.fps = struct.unpack("=L", file.read(4))[0]

        self.head = ANMHEAD(self)
        self.head.read(path, file, self.version)

        self.data = ANMDATA(self)
        self.data.read(path, file, self.version)

    def write(self, path, file):
        print("not implemented")