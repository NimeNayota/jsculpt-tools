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


class FSC_OT_Mask_Extract_Operator(Operator):
    bl_idname = "object.fsc_ot_mask_extract"
    bl_label = "Extract mask"
    bl_description = "Extract a mask as mesh" 
    bl_options = {'REGISTER', 'UNDO'} 


    def invoke(self, context, event):

        target_obj = context.object

        r = bpy.data.brushes["PaintSH"].color.r 
        g = bpy.data.brushes["PaintSH"].color.g 
        b = bpy.data.brushes["PaintSH"].color.b 

        to_sculpt()

        # Invert the mask and hide the masked area
        bpy.ops.paint.mask_flood_fill(mode='INVERT')
        bpy.ops.paint.hide_show(action='HIDE', area='MASKED')

        # select the unmasked part in edit mode and duplicate it
        to_edit()
        select_mesh()
        bpy.ops.mesh.duplicate_move()

        # separate a new object from the selection
        bpy.ops.mesh.separate(type='SELECTED')
        
        # get the new created/separated object
        new_objs = [obj for obj in bpy.context.selected_objects if obj != bpy.context.object]
        new_obj = new_objs[0]
        

        # unhide the target and get rid of the mask
        to_sculpt()
        bpy.ops.paint.hide_show(action='SHOW', area='ALL')
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0.0)

        # make the new object the active one and extrude it with solidify
        make_active(new_obj)

        solid_mod = new_obj.modifiers.new(type="SOLIDIFY", name="FSC_SOLIDIFY")
        solid_mod.offset = context.scene.extract_offset
        solid_mod.use_even_offset = True
        solid_mod.use_quality_normals = True
        bpy.ops.geometry.color_attribute_remove()
        bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))


        # Control the thickness with a scene variable
        solid_mod.thickness = context.scene.extract_thickness
        bpy.ops.object.modifier_apply(modifier=solid_mod.name)

        to_sculpt()

        if context.scene.remesh_after_extract:
            execute_remesh(context)
            bpy.ops.geometry.color_attribute_remove()
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))

        self.report({'INFO'}, "Mask extracted")
        return {'FINISHED'}
