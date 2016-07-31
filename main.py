import bpy
from bpy.props import (StringProperty,
                       PointerProperty,
                       BoolProperty,
                       CollectionProperty)
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup)
from blendernudtool import *
bl_info = {
    "name": "Nud Tool",
    "author": "Astril & Smb123w64gb",
    "version": (0, 4),
    "blender": (2, 75, 0),
    "location": "Properties > Scene",
    "description": "Tool for working with NUD files",
    "warning": "Only mesh editing/importing currently available",
    "wiki_url": "https://github.com/AstrilKnight/Blender-NUD-Tool",
    "category": "User Interface",
}

class MySettings(PropertyGroup):
    name_positioner = StringProperty(
        name="",
        description="name position var",
        default='[]')
    path = StringProperty(
        name="",
        description="Location of model files",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')
    out = StringProperty(
        name="",
        description="Location of output files",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')
    vbnEnable = BoolProperty(
        name="VBN",
        description="Enables import of bones from from vbn file",
        default=False
    )
    colormult = BoolProperty(
        name="colormult",
        description="",
        default=True
    )


class ClearScene(bpy.types.Operator):
    bl_label = "Clear Scene"
    bl_idname = "clearscene.operator"
    bl_description = "Clear the entire scene"

    def execute(self, context):
        bpy.ops.object.select_all()
        bpy.ops.object.delete()
        bpy.ops.object.select_all()
        bpy.ops.object.delete()
        return {'FINISHED'}


class RunImportCode(bpy.types.Operator):
    bl_label = "Import"
    bl_idname = "runimport.operator"
    bl_description = "Import Model data"

    def execute(self, context):
        readModel()
        return {'FINISHED'}


class RunInjectCode(bpy.types.Operator):
    bl_label = "Inject"
    bl_idname = "runinject.operator"
    bl_description = "Inject vertex data into file"

    def execute(self, context):
        injectModel()
        return {'FINISHED'}


class OBJECT_PT_my_panel(Panel):
    bl_idname = "ui.sm4shimporter"
    bl_label = "NUD Tool"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="MESH_CUBE")

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        mytool = scn.SSB4UMT

        row = layout.column(align=True)
        row.label("Model Directory")
        row.prop(scn.SSB4UMT, "path", text="")
        row.label("Output Directory")
        row.prop(scn.SSB4UMT, "out", text="")
        
        #row = layout.row(align=True)
        #layout.prop(mytool, "vbnEnable", text="VBN")
        #layout.prop(mytool, "colormult", text="ColorMult")

        row = layout.row(align=True)
        row.operator("clearscene.operator")

        row = layout.row(align=True)
        row.operator("runimport.operator")
        row.operator("runinject.operator")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.SSB4UMT = PointerProperty(type=MySettings)


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.SSB4UMT


if __name__ == "__main__":
    register()
