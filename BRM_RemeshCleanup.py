#this script is dedicated to the public domain under CC0 (https://creativecommons.org/publicdomain/zero/1.0/)
#do whatever you want with it! -Bram

# BRM REMESH CLEANUP

# This script will:
# -Clean up degenerate vertices
# -Delete loose geometry
# -Collapse very small faces
# -Create a mesh that can be properly sculpted on
# -Create a mesh that can be decimated

# WARNING!
# Very dense meshes (+2 million tris) will potentially take a long time to clean (~60 seconds)
# and could cause Blender to crash if it can't page enough RAM. Make sure you have plenty of
# free memory and save before use.

bl_info = {
    "name": "BRM_RemeshCleanup",
    "category": "3D View",
    "author": "Bram Eulaers",
    "description": "Clean up non-manifold geometry that is usually generated from the Remesh Modifier",
    "version": (0, 2)
    }

import bpy
import bmesh

class BRM_RemeshCleanup(bpy.types.Operator):
    """Remesh Cleanup"""
    bl_idname = "brm.remeshcleanup"
    bl_label = "BRM_RemeshCleanup"
    bl_options = {"UNDO"}
    
    def execute(self, context):
        
        cleaning = True

        #cleaning loop
        while cleaning:
        #{  
     
            bpy.ops.object.mode_set(mode='OBJECT')
            me = bpy.context.object.data       
            bm = bmesh.new()  
            bm.from_mesh(me)
            
            # Find average edge size
            average_lenght = 0
            edgecount = 0
            for e in bm.edges:
                average_lenght+=e.calc_length()
                edgecount+=1
            average_lenght=average_lenght/edgecount
        
            # Collapse short edges
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles(threshold=(average_lenght/3))
            
            # Count non-manifold verts          
            nmvcount = 0
            for v in bm.verts:
                if not v.is_manifold:
                    nmvcount+=1
            if nmvcount is 0:
                cleaning = False
            else:
                cleaning = True
            
                # MACRO - dissolve and patch up broken vertices 
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                context.tool_settings.mesh_select_mode = (True, False, False)
                bpy.ops.mesh.select_non_manifold()
                bpy.ops.mesh.dissolve_verts()
                bpy.ops.mesh.poke()
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_non_manifold()
                bpy.ops.mesh.delete(type='VERT')
                bpy.ops.mesh.fill_holes(sides=0)
                
                #fix non planar faces                
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.vert_connect_nonplanar(angle_limit=0.333)       
                bpy.ops.mesh.select_all(action='SELECT')
                context.tool_settings.mesh_select_mode = (False, False, True)
                bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
            
        #}    
        
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
            
        return {'FINISHED'}

def register():
    bpy.utils.register_class(BRM_RemeshCleanup)

def unregister():
    bpy.utils.unregister_class(BRM_RemeshCleanup)
    
if __name__ == "__main__":
    register()