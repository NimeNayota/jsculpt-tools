import bpy
from bpy.types import Panel


class FSC_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "JSculpt"
    bl_category = "JSculpt"
    
    def draw(self, context):
        pass

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
        row.prop(context.scene, "add_scene_object", text="Scene")

        row = layout.row()
        row.prop(context.scene, "align_to_face", text="Align to face orientation")

        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "add_object_mirror", text="Mirror")

        row = layout.row()
        row.operator('object.fsc_add_object', text="Add object mode")

        row = layout.row()
        row.prop(context.scene, "add_object_size", text="Size")

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
