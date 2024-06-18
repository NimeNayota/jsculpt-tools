import bpy

from bpy.types import Operator

from . utils.fsc_select_mode_utils import *
from .utils.fsc_bool_util  import *

class FSC_OT_Mask_Invert_Transform_Operator(Operator):
    bl_idname = "object.fsc_ot_invert_transform"
    bl_label = "Invert mask transform"
    bl_description = "Invert a mask and activate transform tool" 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        to_sculpt()
        bpy.ops.paint.mask_flood_fill(mode='INVERT')
        bpy.ops.wm.tool_set_by_id(name="builtin.transform")
        bpy.ops.sculpt.set_pivot_position('INVOKE_DEFAULT', mode='UNMASKED')
        return {'FINISHED'}

class FSC_OT_Move_Gizmo_Operator(Operator):
    bl_idname = "object.fsc_ot_move_transform_gizmo"
    bl_label = "move transform"
    bl_description = "Move transform gizmo" 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        to_sculpt()
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)
        bpy.ops.paint.mask_flood_fill(mode='INVERT')
        bpy.ops.wm.tool_set_by_id(name="builtin.transform")
        return {'FINISHED'}



class FSC_OT_Mask_Extract_Operator(Operator):
    bl_idname = "object.fsc_ot_mask_extract"
    bl_label = "Extract mask"
    bl_description = "Extract a mask as mesh" 
    bl_options = {'REGISTER', 'UNDO'} 


    def invoke(self, context, event):

        #target_obj = context.object
        bpy.ops.mesh.paint_mask_extract()


        r = bpy.context.scene.color.r
        g = bpy.context.scene.color.g
        b = bpy.context.scene.color.b

        if not bpy.ops.geometry.color_attribute: 
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        elif not bpy.ops.geometry.color_attribute == True:
            bpy.ops.geometry.color_attribute_remove()
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        
        #smoth = bpy.context.scene.tool_settings.unified_paint_settings.size*0.01
#bpy.context.object.modifiers["geometry_extract_solidify"].thickness = -0.22
#bpy.context.object.modifiers["geometry_extract_solidify"].offset = -0.74026
#bpy.context.scene.bevel_depth = 0.09
#bpy.context.scene.loop_cuts = 16
        to_sculpt()
#bpy.context.object.modifiers["geometry_extract_solidify"].thickness = -0.22
#bpy.context.object.modifiers["geometry_extract_solidify"].offset = -0.74026
        #self.report({'INFO'}, "Mask extracted")
        return {'FINISHED'}
