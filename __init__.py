bl_info = {
    "name": "Draw Axes Addon",
    "author": "Shari Klotzkin",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object",
    "description": "Display and axes at the origin.  Includes arrows and axis labels",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

import bpy
import bmesh
from mathutils import Vector
import math
from bpy.types import Operator,PropertyGroup

axis_size=10   #  Adjust this number to get desired axes size

def object_copy(obj,name):
    new_obj=obj.copy()
    new_obj.data=obj.data.copy()
    new_obj.name=name
    bpy.context.collection.objects.link(new_obj)
    return(new_obj)

def add_label(string,label_name,location,rotation,dimensions):
    label_text = bpy.data.curves.new(type="FONT",name=label_name)
    label_text.body = string
    new_label = bpy.data.objects.new(label_name, label_text)
    bpy.context.collection.objects.link(new_label)
    new_label.location=location
    new_label.rotation_euler=rotation
    new_label.dimensions=dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
#    new_label.hide_select = True
    return(new_label) 

def draw_axes(axis_size):

    mat = bpy.data.materials.new(name="Material Axis")
    mat.diffuse_color=[0.02, 0.8, 0.46, 1]
 
# put objects used to create axes in a separate collection
    scene_collection = bpy.context.view_layer.layer_collection.children[0]
    if bpy.data.collections.get('Axes'): #make sure the axes have not yet been drawn
        return{'FINISHED'}
    axes_collection = bpy.data.collections.new("Axes")
    bpy.context.scene.collection.children.link(axes_collection)
# Add new objects to this collection collection
    axes_coll_view=bpy.context.view_layer.layer_collection.children["Axes"]
    bpy.context.view_layer.active_layer_collection=axes_coll_view

    bpy.ops.mesh.primitive_cylinder_add(radius=axis_size/100, depth=axis_size, location=(axis_size/2, 0, 0), rotation=(0,math.pi/2,0))
    xline=bpy.context.active_object
    xline.name="x_axis"
    bpy.ops.mesh.primitive_cone_add(radius1=axis_size/8, radius2=0, depth=axis_size/10, location=(axis_size, 0, 0), rotation=(0,math.pi/2,0), scale=(0.3, 0.3, 1))
    xarrow=bpy.context.active_object
#https://blender.stackexchange.com/questions/13986/how-to-join-objects-with-python
    c={}
    c["object"] = c["active_object"] = xline
    c["selected_objects"] = c["selected_editable_objects"] = [xline, xarrow]
    bpy.ops.object.join(c)
    xline.data.materials.append(mat)
    xline.hide_select=True

    yaxis=object_copy(xline,"y_axis")       
    yaxis.rotation_euler[2]=math.pi/2
    yaxis.location = (0,axis_size/2,0)

    zaxis =object_copy(xline,"z_axis")
    zaxis.rotation_euler[1]=0
    zaxis.scale=(1,1,0.5)
    zaxis.location = (0,0,axis_size/4)

    xlabel=add_label("X","x_axis_label",(axis_size*0.95,0,axis_size*0.05),(math.pi/2,0,math.pi),(axis_size/15,axis_size/15,0))
    ylabel=add_label("Y","y_axis_label",(0,axis_size*0.95,axis_size*0.05),(math.pi/2,0,math.pi),(axis_size/15,axis_size/15,0))
    zlabel=add_label("Z","z_axis_label",(0,axis_size*0.05,axis_size*0.95/2),(math.pi/2,0,math.pi),(axis_size/15,axis_size/15,0))
    xlabel.data.materials.append(mat)
    ylabel.data.materials.append(mat)
    zlabel.data.materials.append(mat)

# Set active collection back to main scene collection
    bpy.context.view_layer.active_layer_collection = scene_collection 

class OBJECT_OT_DrawAxes(bpy.types.Operator):
    """Draw Axes"""
    bl_idname = "myops.draw_axes"
    bl_label = "Draw Axes"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        axis = bpy.context.scene.objects.get("x_axis")
        return not axis

    def execute(self, context):
        draw_axes(axis_size)
        return {'FINISHED'}

def custom_draw(self, context):
    self.layout.operator("myops.draw_axes", icon='OBJECT_ORIGIN', text="Draw Axes")

def register():
    bpy.utils.register_class(OBJECT_OT_DrawAxes)
    bpy.types.VIEW3D_MT_object.append(custom_draw) # Object menu

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_DrawAxes)
    bpy.types.VIEW3D_MT_object.remove(custom_draw)

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.myops.draw_axes()
