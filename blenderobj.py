import bpy
import time
import math
import numpy as np
import os

user_home_dir = os.path.expanduser("~")
# from bpy import data

bl_info = {
    "name": "blenderobj",
    "description": "blenderobj",
    "author": "Marc Otten",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "category": "Scripts",
    "location": "Scripts > blenderobj",
}


def show_popup_message(title, message):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon="ERROR")


def bprint(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == "CONSOLE":
                override = {"window": window, "screen": screen, "area": area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")


def setViewport():
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    space.shading.type = "MATERIAL"


def deleteall():
    bprint("Running Delete All...")

    # Deselect all objects
    bpy.ops.object.select_all(action="DESELECT")

    # Select all objects in the scene and delete them
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    try:
        # Delete all materials and textures
        for material in bpy.data.materials:
            bpy.data.materials.remove(material)
        for texture in bpy.data.textures:
            bpy.data.textures.remove(texture)

        # Delete all images
        for image in bpy.data.images:
            bpy.data.images.remove(image)

        # Delete all meshes and curves
        for mesh in bpy.data.meshes:
            bpy.data.meshes.remove(mesh)
        for curve in bpy.data.curves:
            bpy.data.curves.remove(curve)

        # Delete all lamps
        for lamp in bpy.data.lamps:
            bpy.data.lamps.remove(lamp)

        # Delete all cameras
        for camera in bpy.data.cameras:
            bpy.data.cameras.remove(camera)

        # Delete all worlds
        for world in bpy.data.worlds:
            bpy.data.worlds.remove(world)
    except:
        pass


def importObj():
    bprint("Running importObj...")
    obj_file_path = os.path.join(user_home_dir, "import.obj")
    bpy.ops.import_scene.obj(filepath=obj_file_path)


def exportObj():
    bprint("Running ExportObj...")
    # Define the file path of the OBJ file
    obj_file_path = os.path.join(user_home_dir, "export.obj")
    obj = bpy.context.active_object

    # Export the selected object as an OBJ file
    bpy.ops.export_scene.obj(filepath=obj_file_path, use_selection=True)


class blenderobj_custom_menu(bpy.types.Panel):
    bl_idname = "SCRIPTS_PT_blenderobj"
    bl_label = "blenderobj"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "blenderobj"

    def draw(self, context):
        layout = self.layout
        layout.separator()
        layout.operator("object.blenderobj_operator", text="ImportExport Obj")


class blenderobj_Operator(bpy.types.Operator):
    bl_idname = "object.blenderobj_operator"
    bl_label = "blenderobj"
    bl_description = "blenderobj"

    def execute(self, context):
        bprint("Running blenderobj...")
        try:
            deleteall()
            importObj()
            exportObj()
            show_popup_message("blenderobj", "Finished")
        except Exception as e:
            bprint(e)
        return {"FINISHED"}


classes = [blenderobj_Operator, blenderobj_custom_menu]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
