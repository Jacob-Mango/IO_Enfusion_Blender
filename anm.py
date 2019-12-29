import time
import struct
import bpy

class ANM(object):    
    version = bpy.props.IntProperty(name="Version", default=6)
    fps = bpy.props.IntProperty(name="FPS", default=60)

    def load(self, path, file):
        # Ascii		    form;				// "FORM"
        # bigEndian	    remaining_bytes;	// useless. 8 less that actual file size
        # Ascii		    anmiset;			// "ANIMSET5" or "ANIMSET6"
        # bigEndian	    remaining_bytes; 	// useless 20 less that actual file size
        # Ascii		    fpsstr;				// a constant "FPS\0" 
        # bigEndian	    num6;				// a constant 0x0004
        # uint32		fps;				// frames per second (normally 1e 00 00 00))

        form = file.read(4).decode("utf-8")
        if form != "FORM":
            raise RuntimeError("File type not FORM")
        
        file.read(4)

        bytes = file.read(7)
        animset = bytes.decode("utf-8")

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

        bytes = file.read(8)
        print(bytes)
        self.fps = struct.unpack("=Q", bytes)[0]
        print(self.fps)




    def save(self, file):
        print("not implemented")

if __name__ == "__main__":
    filepath = "P:/DZ/anims/anm/player/attacks/2hd/p_2hd_light_erc_attack_L_02.anm"
    try:
        file = open(filepath, "rb")
    except IOError:
        print("Could not open file for reading:\n %s" % filepath)
    
    animation = ANM()
    animation.load(filepath, file)