import bpy
from bpy.types import Panel


class FSC_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "JSculpt"
    bl_category = "JSculpt"
    
    def draw(self, context):
        pass

class FSC_Color_Picker_Panel(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Color Picker"
    bl_idname = "OBJECT_PT_color_picker"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "JSculpt"
 
    def draw(self, context): 

        layout = self.layout 
        row = layout.row()
        row.prop(context.scene, "color", text="Color")

        row = layout.row()
        row.operator('object.fsc_ot_color_remove_add', text="New color")
        row.operator('object.fsc_ot_fill_color', text="Fill")
        row = layout.row()
        row.operator("object.fsc_ot_color_brush", text="ColorBrush")
        row = layout.row()
        row.operator("object.fsc_color_picker", text="ColorPicker")



class FSC_PT_Bool_Objects_Panel(FSC_PT_Panel, Panel):
    bl_parent_id = "FSC_PT_Panel"
    bl_label = "Bool objects"
    
    def draw(self, context): 

        layout = self.layout

        row = layout.row()
        row.prop_search(context.scene, "target_object", context.scene, "objects", text="Target")

        row = layout.row()
        row.operator('object.fsc_bool_union', text='Bool Union')

        row = layout.row()
        row.operator('object.fsc_bool_diff', text='Bool Difference')

class FSC_PT_Add_Objects_Panel(Panel):
    bl_parent_id = "FSC_PT_Panel"
    bl_label = "Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context): 

        layout = self.layout

        row = layout.row()
        row.prop(context.scene, "add_object_type", text="Type")

        row = layout.row()
        row.prop(context.scene, "vert_object_type", text="Pro2")
        row.prop(context.scene, "sigm_object_type", text="Pro1")

        row = layout.row()
        row.prop(context.scene, "add_scene_object", text="Scene")

        row = layout.row()
        row.prop(context.scene, "align_to_face", text="Align to face orientation")

        layout = self.layout

        row = layout.row()
        row.prop_search(context.scene, "mror_target_object", context.scene, "objects", text="Mirror Object")

        row = layout.row()
        row.operator('object.fsc_add_object', text="Add object mode")
        row.operator("object.dub", text="Dubl")

        row = layout.row()
        row.operator('object.origin_set_geometry', text="Apply")






class FSC_PT_Extract_Mask_Panel(Panel):
    bl_parent_id = "FSC_PT_Panel"
    bl_label = "Mask utils"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context): 

        layout = self.layout 

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "extract_thickness", text="Thickness")

        col = row.column()
        col.prop(context.scene, "extract_offset", text="Offset")

        row = layout.row()
        row.operator('object.fsc_ot_mask_extract', text="Extract Mask")

        row = layout.row()
        row.operator('object.fsc_ot_invert_transform', text="Invert Transform")
        row.operator("object.fsc_ot_move_transform_gizmo", text="Move Gizmo")


class FSC_PT_Remesh_Panel(Panel):
    bl_parent_id = "FSC_PT_Panel"
    bl_label = "Remeshing"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context): 

        layout = self.layout

        row = layout.row()
        row.prop(context.scene, "remesh_after_extract", text="Remesh after extract")

        row = layout.row()
        row.prop(context.scene, "remesh_fix_poles", text="Fix poles")

        row = layout.row()
        row.prop(context.scene, "remesh_voxel_size", text="Voxel size")

        row = layout.row()
        col = row.column()
        col.operator('object.fsc_remesh', text="Remesh")

        col = row.column()
        col.operator('object.fsc_remesh', text="Join & Remesh").join_b4_remesh = True


class FSC_PT_Retopo_Panel(Panel):
    bl_parent_id = "FSC_PT_Panel"
    bl_label = "Retopo"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context): 

        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "retopo_object", text="Target")

        row = layout.row()
        row.prop(context.scene, "retopo_mesh", text="Mesh")

        row = layout.row()
        row.prop(context.scene, "add_retopo_mirror", text="Mirror")

        row = layout.row()
        col = row.column()
        col.operator('object.fsc_draw_retopo', text="Draw Mesh")

        col = row.column()
        col.operator('object.fsc_retopo_ring', text="Draw Ring")

        row = layout.row()
        col = row.column()
        col.operator('mesh.fsc_flipnormals', text="", icon="ORIENTATION_NORMAL")

        col = row.column()
        col.operator('object.fsc_subsurf', text="", icon="MOD_SUBSURF")

        col = row.column()
        col.operator('object.fsc_shrinkwrap', text="", icon="MOD_SHRINKWRAP")

        col = row.column()
        col.operator('object.fsc_solidify', text="", icon="MOD_SOLIDIFY")

        col = row.column()
        col.operator('object.fsc_apply_all_mod_op', text="", icon="NLA_PUSHDOWN")      
