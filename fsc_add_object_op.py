import bpy
import blf

from bpy.types import Operator

from mathutils import Vector

from bpy_extras import view3d_utils

from . utils.fsc_select_mode_utils import *

from . utils.fsc_common_utils import get_axis_no

from . utils.textutils import *



class FSC_OT_Add_Oject_Operator(Operator):
    bl_idname = "object.fsc_add_object"
    bl_label = "Add object"
    bl_description = "Add object in sculpt mode" 
    bl_options = {'REGISTER', 'UNDO'} 

    def __init__(self):
        self.draw_handle_2d = None

    def invoke(self, context, event):
        args = (self, context)
        context.window_manager.in_modal_mode = True
        self.register_handlers(args, context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def register_handlers(self, args, context):
        self.draw_handle_2d = bpy.types.SpaceView3D.draw_handler_add(
        self.draw_callback_2d, args, "WINDOW", "POST_PIXEL")
        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)

    def unregister_handlers(self, context):
        context.window_manager.in_modal_mode = False
        context.window_manager.event_timer_remove(self.draw_event)
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle_2d, "WINDOW")
        
        self.draw_handle_2d = None
        self.draw_event  = None

    def draw_callback_2d(self, op, context):

        # Draw text for add object mode
        header = "- Add Object Mode (Type: " + context.scene.add_object_type + ") -"
        text = "Shift + Left Click = Add | Esc = Exit"

        blf.color(1, 1, 1, 1, 1)
        blf_set_size(0, 20)
        blf_set_size(1, 16)

        region = context.region
        xt = int(region.width / 2.0)

        blf.position(0, xt - blf.dimensions(0, header)[0] / 2, 50 , 0)
        blf.draw(0, header)

        blf.position(1, xt - blf.dimensions(1, text)[0] / 2, 20 , 0)
        blf.draw(1, text)


    @classmethod
    def poll(cls, context): 

        if context.object is None:
            return False

        if context.window_manager.in_modal_mode:
            return False

        return True

    def finish(self):
        bpy.context.window_manager.in_modal_mode = False
        self.unregister_handlers(bpy.context)
        return {"FINISHED"}

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        if event.type == "ESC" and event.value == "PRESS":
            context.window_manager.in_modal_mode = False
            self.unregister_handlers(context)
            return {'FINISHED'}

        if event.value == "PRESS" and event.type == "LEFTMOUSE" and event.shift:
            mouse_pos = (event.mouse_region_x, event.mouse_region_y)
            self.add_object(context, mouse_pos)

        return {'PASS_THROUGH'}

    def get_raycast_param(self, view_layer):        
        if bpy.app.version >= (2, 91, 0):
            return view_layer.depsgraph
        else:
            return view_layer 

    def add_object(self, context, mouse_pos):
        if context.scene.join_and_mask_fill:

            bpy.ops.paint.mask_flood_fill(mode='VALUE', value=1)

        old_name = bpy.context.object.name

        scene = context.scene
        mode = get_mode()

        to_object()
        
        region = context.region
        region3D = context.space_data.region_3d

        view_vector = view3d_utils.region_2d_to_vector_3d(region,   region3D, mouse_pos)
        origin      = view3d_utils.region_2d_to_origin_3d(region,   region3D, mouse_pos)
        loc         = view3d_utils.region_2d_to_location_3d(region, region3D, mouse_pos, view_vector)
        rot         = (0,0,0)  

        raycast_param = self.get_raycast_param(context.view_layer)

        # Get intersection and create objects at this location if possible
        hit, loc_hit, norm, face, *_ = scene.ray_cast(raycast_param, origin, view_vector)
        if hit:
            loc = loc_hit
            z = Vector((0,0,1))
            
            if context.scene.align_to_face:
                rot = z.rotation_difference( norm ).to_euler()


        active_obj = bpy.context.active_object
        old_loc = active_obj.location.copy()

        obj_type = context.scene.add_object_type
        #size object
        obj_size = 0.001 * bpy.context.scene.tool_settings.unified_paint_settings.size

        obj_size_s = 0.02 * bpy.context.scene.tool_settings.unified_paint_settings.size

        

        vert = 3
        sigm = 3
        stat_size = 0.14
        mult_size = 0.03
        mult_size_C = 0.18

        BrushMir = "s"
        BrushMir2 = "s"
        BrushMir3 = "s"

        obj_vet = context.scene.vert_object_type
        obj_sigm = context.scene.sigm_object_type 

        orig_size0 = bpy.context.object.scale[0]
        orig_size1 = bpy.context.object.scale[1]
        orig_size2 = bpy.context.object.scale[2]

        #   color fattribute add
        r = bpy.context.scene.color.r 
        g = bpy.context.scene.color.g 
        b = bpy.context.scene.color.b 


        # TODO: Add more init options here

        if bpy.context.object.data.use_mirror_x == True:
            BrushMir = "X"

            BrushMir2 = "s"
            BrushMir3 = "s"
            if bpy.context.object.data.use_mirror_y == True:
                BrushMir2 = "Y"

                BrushMir3 = "s"
                if bpy.context.object.data.use_mirror_z == True:
                    BrushMir3 = "Z"

            elif bpy.context.object.data.use_mirror_z == True:
                BrushMir3 = "Z"

                BrushMir2 = "s"

        elif bpy.context.object.data.use_mirror_y == True:
            BrushMir2 = "Y"

            BrushMir = "s"
            BrushMir3 = "s"
            if bpy.context.object.data.use_mirror_z == True:
                BrushMir3 = "Z"

                BrushMir = "s"
        elif bpy.context.object.data.use_mirror_z == True:
            BrushMir3 = "Z"

            BrushMir = "s"
            BrushMir2 = "s"

        
        if obj_vet == "3":
            vert = 3
        elif obj_vet == "4":
            vert = 4
        elif obj_vet == "5":
            vert = 5
        elif obj_vet == "6":
            vert = 6
        elif obj_vet == "8":
            vert = 8
        elif obj_vet == "12":
            vert = 12
        elif obj_vet == "24":
            vert = 24
        elif obj_vet == "32":
            vert = 32
        elif obj_vet == "48":
            vert = 48

        if obj_sigm == "3":
            sigm = 3
        elif obj_vet == "4":
            sigm = 4
        elif obj_sigm == "5":
            sigm = 5
        elif obj_sigm == "6":
            sigm = 6
        elif obj_sigm == "8":
            sigm = 8
        elif obj_sigm == "14":
            sigm = 14
        elif obj_sigm == "24":
            sigm = 24
        elif obj_sigm == "32":
            sigm = 32
        elif obj_sigm == "48":
            sigm = 48

        if obj_type == "Sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(segments=vert, ring_count=sigm, radius=obj_size, enter_editmode=False, location=loc)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        if obj_type == "Plane":
            bpy.ops.mesh.primitive_plane_add(size=obj_size*2, enter_editmode=False, location=loc, rotation=rot)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
            
        elif obj_type == "Cube":  
            bpy.ops.mesh.primitive_cube_add(size=obj_size, enter_editmode=False, location=loc, rotation=rot)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        elif obj_type == "CubeS":  
            bpy.ops.mesh.primitive_cube_add(size=obj_size, enter_editmode=False, location=loc, rotation=rot)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
            bpy.ops.object.subdivision_set(level=2, relative=False)
        elif obj_type == "CubeC":  
            bpy.ops.mesh.primitive_cylinder_add(vertices=4, radius=obj_size, depth=obj_size*2, enter_editmode=False, location=loc, rotation=rot)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        elif obj_type == "Cylinder":
            bpy.ops.mesh.primitive_cylinder_add(vertices=vert, radius=obj_size, depth=obj_size*2, enter_editmode=False, location=loc, rotation=rot)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        elif obj_type == "CylinderX":
            bpy.ops.mesh.primitive_cylinder_add(vertices=vert,radius=stat_size, depth=obj_size_s*mult_size_C, enter_editmode=False, location=loc, rotation=rot)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        elif obj_type == "Torus":
            bpy.ops.mesh.primitive_torus_add(align='WORLD', location=loc, rotation=rot, major_radius=obj_size, minor_radius=obj_size_s*mult_size, abso_major_rad=obj_size_s, abso_minor_rad=obj_size_s)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        elif obj_type == "TorusI":
            bpy.ops.mesh.primitive_torus_add(align='WORLD', location=loc, rotation=rot, major_segments=vert, minor_segments=sigm, major_radius=obj_size*0.05, minor_radius=obj_size_s*0.1, abso_major_rad=obj_size_s, abso_minor_rad=obj_size_s)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        elif obj_type == "TorusX":
            bpy.ops.mesh.primitive_torus_add(align='WORLD', location=loc, rotation=rot, major_segments=vert, minor_segments=sigm, major_radius=stat_size, minor_radius=obj_size_s*mult_size, abso_major_rad=obj_size_s, abso_minor_rad=obj_size_s)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        elif obj_type == "Cone":
            bpy.ops.mesh.primitive_cone_add(vertices=vert, radius1=obj_size, radius2=0, depth=obj_size*2, enter_editmode=False, location=loc, rotation=rot)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        elif obj_type == "ConeX":
            bpy.ops.mesh.primitive_cone_add(vertices=vert, radius1=stat_size, radius2=0, depth=obj_size_s*mult_size_C, enter_editmode=False, location=loc, rotation=rot)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        elif obj_type == "Icosphere":
            bpy.ops.mesh.primitive_ico_sphere_add(radius=obj_size, enter_editmode=False, location=loc, rotation=rot)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        elif obj_type == "Grid":
            bpy.ops.mesh.primitive_grid_add(x_subdivisions=vert, y_subdivisions=sigm, size=obj_size, enter_editmode=False, align='WORLD', location=loc, rotation=rot)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
        elif obj_type == "Circle":
            bpy.ops.mesh.primitive_circle_add(vertices=vert, radius=obj_size*8, fill_type='NGON', enter_editmode=False, align='WORLD', location=loc, rotation=rot)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
            bpy.ops.object.modifier_add(type='WIREFRAME')
            bpy.context.object.modifiers["Wireframe"].use_boundary = True
        elif obj_type == "Ring":
            bpy.ops.mesh.primitive_cylinder_add(vertices=vert, radius=stat_size, depth=obj_size_s*mult_size_C, end_fill_type='NOTHING', enter_editmode=False, location=loc, rotation=rot)
            bpy.ops.geometry.color_attribute_add(color=(r, g, b, 1))
            bpy.ops.object.modifier_add(type='SOLIDIFY')

        elif obj_type == "Scene":
            custom_obj = context.scene.add_scene_object
            if custom_obj:

                deselect_all()
                make_active(custom_obj)

                bpy.context.object.scale[0] = obj_size
                bpy.context.object.scale[1] = obj_size
                bpy.context.object.scale[2] = obj_size
            
                bpy.ops.object.duplicate(linked=True)
                clone_custom = bpy.context.view_layer.objects.active
                bpy.ops.object.make_single_user(object=True, obdata=True)

                clone_custom.location = loc
                clone_custom.rotation_euler = rot

                deselect_all()
                make_active(clone_custom)

                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
        

        if BrushMir or BrushMir2 or BrushMir3 != "s":

            active_obj_m = bpy.context.active_object



            bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)


            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            

            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
            mirror_mod = active_obj_m.modifiers.new(type="MIRROR", name="FSC_MIRROR")
            mirror_mod.use_axis[0] = False
            if BrushMir == "X":
                mirror_mod.use_axis[get_axis_no(BrushMir)] = True
            if BrushMir2 == "Y":
                mirror_mod.use_axis[get_axis_no(BrushMir2)] = True
            if BrushMir3 == "Z":
                mirror_mod.use_axis[get_axis_no(BrushMir3)] = True

            mirror_mod.mirror_object = bpy.data.objects[old_name]

        to_mode(mode)

        if context.scene.join_and_mask_fill:
            if bpy.context.object.modifiers["FSC_MIRROR"].use_axis[0] ==  True:#0 = x, 1 = y, 2 = z
                bpy.context.object.data.use_mirror_x = True

                bpy.context.object.data.use_mirror_y = False
                bpy.context.object.data.use_mirror_z = False
                if bpy.context.object.modifiers["FSC_MIRROR"].use_axis[1] ==  True:
                    bpy.context.object.data.use_mirror_y = True

                    bpy.context.object.data.use_mirror_z = False

                    if bpy.context.object.modifiers["FSC_MIRROR"].use_axis[2] ==  True:
                        bpy.context.object.data.use_mirror_z = True

                elif bpy.context.object.modifiers["FSC_MIRROR"].use_axis[2] ==  True:
                    bpy.context.object.data.use_mirror_z = True

                    bpy.context.object.data.use_mirror_y = False

            elif bpy.context.object.modifiers["FSC_MIRROR"].use_axis[1] ==  True:#0 = x, 1 = y, 2 = z
                bpy.context.object.data.use_mirror_y = True

                bpy.context.object.data.use_mirror_x = False
                bpy.context.object.data.use_mirror_z = False
                if bpy.context.object.modifiers["FSC_MIRROR"].use_axis[2] ==  True:
                    bpy.context.object.data.use_mirror_z = True

                    bpy.context.object.data.use_mirror_x = False

            elif bpy.context.object.modifiers["FSC_MIRROR"].use_axis[2] ==  True:#0 = x, 1 = y, 2 = z
                bpy.context.object.data.use_mirror_z = True

                bpy.context.object.data.use_mirror_x = False
                bpy.context.object.data.use_mirror_y = False



            bpy.ops.object.convert(target='MESH')

            bpy.data.objects[old_name].select_set(True)
            bpy.ops.object.join()

            bpy.context.scene.cursor.location = old_loc

            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')



            bpy.ops.sculpt.face_sets_init(mode='UV_SEAMS')
            bpy.ops.sculpt.set_pivot_position(mode='UNMASKED')

        bpy.ops.wm.tool_set_by_id(name="builtin.scale")



class FSC_OT_Origin_Set_GEOMETRY_Operator(Operator):
    bl_idname = "object.origin_set_geometry"
    bl_label = "Set origin geometry"
    bl_description = "Set origin geometry" 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        bpy.ops.sculpt.sculptmode_toggle()
        obj = bpy.context.object
        if obj.modifiers:
            if bpy.context.object.modifiers["FSC_MIRROR"].use_axis[0] ==  True:#0 = x, 1 = y, 2 = z
                bpy.context.object.data.use_mirror_x = True

                bpy.context.object.data.use_mirror_y = False
                bpy.context.object.data.use_mirror_z = False
                if bpy.context.object.modifiers["FSC_MIRROR"].use_axis[1] ==  True:
                    bpy.context.object.data.use_mirror_y = True

                    bpy.context.object.data.use_mirror_z = False

                    if bpy.context.object.modifiers["FSC_MIRROR"].use_axis[2] ==  True:
                        bpy.context.object.data.use_mirror_z = True

                elif bpy.context.object.modifiers["FSC_MIRROR"].use_axis[2] ==  True:
                    bpy.context.object.data.use_mirror_z = True

                    bpy.context.object.data.use_mirror_y = False

            elif bpy.context.object.modifiers["FSC_MIRROR"].use_axis[1] ==  True:#0 = x, 1 = y, 2 = z
                bpy.context.object.data.use_mirror_y = True

                bpy.context.object.data.use_mirror_x = False
                bpy.context.object.data.use_mirror_z = False
                if bpy.context.object.modifiers["FSC_MIRROR"].use_axis[2] ==  True:
                    bpy.context.object.data.use_mirror_z = True

                    bpy.context.object.data.use_mirror_x = False

            elif bpy.context.object.modifiers["FSC_MIRROR"].use_axis[2] ==  True:#0 = x, 1 = y, 2 = z
                bpy.context.object.data.use_mirror_z = True

                bpy.context.object.data.use_mirror_x = False
                bpy.context.object.data.use_mirror_y = False

            bpy.ops.object.convert(target='MESH')
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

            bpy.ops.sculpt.sculptmode_toggle()
        
        return {'FINISHED'}

execute_counter = 0 




class FSC_OT_Object_Dub_Operator(Operator):
    bl_idname = "object.dub"
    bl_label = "object dub"
    bl_description = "object dub" 
    bl_options = {'REGISTER', 'UNDO'} 
    
    def execute(self, context):
        to_sculpt()
        C = bpy.context
        src_obj = bpy.context.active_object
        old_name = bpy.context.object.name

        if context.scene.join_and_mask_fill:
            
            bpy.ops.sculpt.face_sets_create(mode='MASKED')
            bpy.ops.mesh.paint_mask_extract(add_boundary_loop=False, smooth_iterations=0, apply_shrinkwrap=False, add_solidify=False)
            bpy.data.objects[old_name].select_set(True)
            bpy.ops.object.join()

        else:
            for i in range (0,1):
                new_obj = src_obj.copy()
                new_obj.data = src_obj.data.copy()
                new_obj.animation_data_clear()
                C.collection.objects.link(new_obj)
        bpy.ops.sculpt.sculptmode_toggle()
        return {'FINISHED'}
class FSC_OT_Object_Subb_Level_UP_Operator(Operator):
    bl_idname = "object.subb_level_up"
    bl_label = "subb_level_up"
    bl_description = "Move subb_level_up" 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        bpy.context.object.modifiers["Multires"].sculpt_levels += 1
        return {'FINISHED'}

class FSC_OT_Object_Subb_Level_DOWN_Operator(Operator):
    bl_idname = "object.subb_level_down"
    bl_label = "subb_level_down"
    bl_description = "Move subb level down" 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        bpy.context.object.modifiers["Multires"].sculpt_levels -= 1
        return {'FINISHED'}


