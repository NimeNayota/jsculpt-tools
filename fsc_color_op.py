import bpy

from bpy.types import Operator

#from . utils.fsc_select_mode_utils import *
#from .utils.fsc_bool_util  import *

class FSC_Color_Picker_Operator(Operator):

    bl_idname = "object.fsc_color_picker"
    bl_label = "Color_picker"
    bl_description = "Color Picker, Not working yet" 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        #self.x = event.mouse_x
        #self.y = event.mouse_z

        bpy.ops.paint.texture_paint_toggle()
        #bpy.ops.paint.sample_color(location=loc, merged=False, palette=False)
        bpy.ops.paint.sample_color(location=(550, 350), merged=False, palette=False)
        bpy.ops.sculpt.sculptmode_toggle()


        return {'FINISHED'}


class FSC_Color_Brush_Operator(Operator):

    bl_idname = "object.fsc_ot_color_brush"
    bl_label = "Color_brush"
    bl_description = "Color Brush" 
    bl_options = {'REGISTER', 'UNDO'} 
    def execute(self, context):

        brush_r = bpy.context.scene.tool_settings.unified_paint_settings.color.r
        brush_g = bpy.context.scene.tool_settings.unified_paint_settings.color.g
        brush_b = bpy.context.scene.tool_settings.unified_paint_settings.color.b

        r = bpy.context.scene.color.r
        g = bpy.context.scene.color.g
        b = bpy.context.scene.color.b

        bpy.data.scenes["Scene"].tool_settings.unified_paint_settings.use_unified_color

        if r != brush_r and g != brush_g and b != brush_b:
            bpy.context.scene.tool_settings.unified_paint_settings.color = (r, g, b)


        return {'FINISHED'}
#        if bpy.context.scene.color == (0.0, 0.0, 0,0) 



 



class FSC_OT_Color_Add_And_Remove_Operator(Operator):
    bl_idname = "object.fsc_ot_color_remove_add"
    bl_label = "Color_Remove Add"
    bl_description = "Color attribute remove and add" 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        
        r = bpy.context.scene.color.r
        g = bpy.context.scene.color.g
        b = bpy.context.scene.color.b


        if bpy.ops.geometry.color_attribute:
            bpy.ops.geometry.color_attribute_remove()
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        elif not bpy.ops.geometry.color_attribute:
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))

        return {'FINISHED'}



class FSC_OT_Fill_Color_Operator(Operator):
    bl_idname = "object.fsc_ot_fill_color"
    bl_label = "Color_Fiil"
    bl_description = "uses a color filter" 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        
        r = bpy.context.scene.color.r
        g = bpy.context.scene.color.g
        b = bpy.context.scene.color.b

        if bpy.ops.geometry.color_attribute:
            bpy.ops.sculpt.color_filter(start_mouse=(1, 1), strength=2.0, fill_color=(r, g, b))
        elif not bpy.ops.geometry.color_attribute:
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
            bpy.ops.sculpt.color_filter(start_mouse=(1, 1), strength=2.0, fill_color=(r, g, b))

        return {'FINISHED'}
        
