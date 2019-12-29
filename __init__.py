import bpy
import bpy_extras.io_utils
from bpy.types import Operator, AddonPreferences
from bpy.props import *
from bpy_extras.io_utils import ExportHelper, ImportHelper

bl_info = {
    "name": "Enfusion",
    "author": "Jacob_Mango",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "File > Import",
    "description": "Import Enfusion File",
    "wiki_url": "https://github.com/Jacob-Mango/IO_Enfusion_Blender",
    "tracker_url": "https://github.com/Jacob-Mango/IO_Enfusion_Blender/issues",
    "support": "COMMUNITY",
    "category": "Import-Export"
}

class ImportENFANM(bpy.types.Operator, ImportHelper):
    bl_idname = "import_anim.anm"
    bl_label = "Import Enfusion Animation"
    bl_description = "Import one or more Enfusion Animation files"
    bl_options = {'PRESET'}

    filename_ext = ".anm"
    filter_glob = StringProperty(default="*.anm", options={'HIDDEN'})

    files = CollectionProperty(type=bpy.types.PropertyGroup)

    def execute(self, context):
        from . import import_anm
        result = import_anm.load(
            self, context, **self.as_keywords(ignore=("filter_glob", "files")))
        if result:
            self.report({'INFO'}, 'ANM has been loaded')
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, 'Failed to load ANM')
            return {'CANCELLED'}

    @classmethod
    def poll(self, context):
        return True


def menu_func_import_anm(self, context):
    self.layout.operator(ImportENFANM.bl_idname, text="Enfusion Animation (.anm)")

__classes__ = (
    ImportENFANM,
)

def register():
    for c in __classes__:
        bpy.utils.register_class(c)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_anm)


def unregister():
    for c in reversed(__classes__):
        bpy.utils.unregister_class(c)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_anm)


if __name__ == "__main__":
    register()