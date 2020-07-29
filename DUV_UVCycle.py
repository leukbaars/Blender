import bpy
import math
import bmesh
from mathutils import Vector


class DREAMUV_OT_uv_cycle(bpy.types.Operator):
    """Rotate UVs but retain uv edge positions"""
    bl_idname = "dream_uv.uvcycle"
    bl_label = "3D View UV Cycle"
    bl_options = {"UNDO"}

    def execute(self, context):
        mesh = bpy.context.object.data
        bm = bmesh.from_edit_mesh(mesh)
        bm.faces.ensure_lookup_table()
        uv_layer = bm.loops.layers.uv.active
        
        #do this again
        faces = list()
        #MAKE FACE LIST
        for face in bm.faces:
            if face.select:
                faces.append(face)   
        
        #get original size
        xmin, xmax = faces[0].loops[0][uv_layer].uv.x, faces[0].loops[0][uv_layer].uv.x
        ymin, ymax = faces[0].loops[0][uv_layer].uv.y, faces[0].loops[0][uv_layer].uv.y
        
        for face in faces: 
            for vert in face.loops:
                xmin = min(xmin, vert[uv_layer].uv.x)
                xmax = max(xmax, vert[uv_layer].uv.x)
                ymin = min(ymin, vert[uv_layer].uv.y)
                ymax = max(ymax, vert[uv_layer].uv.y)

        for face in faces:
                for loop in face.loops:

                    loop[uv_layer].uv.x -= xmin
                    loop[uv_layer].uv.y -= ymin
                    loop[uv_layer].uv.x /= (xmax-xmin)
                    loop[uv_layer].uv.y /= (ymax-ymin)

                    newx = -loop[uv_layer].uv.y + 1.0
                    newy = loop[uv_layer].uv.x 
                    loop[uv_layer].uv.x = newx
                    loop[uv_layer].uv.y = newy

                    loop[uv_layer].uv.x *= xmax-xmin
                    loop[uv_layer].uv.y *= ymax-ymin
                    loop[uv_layer].uv.x += xmin
                    loop[uv_layer].uv.y += ymin                

        bmesh.update_edit_mesh(mesh, False, False)
        return {'FINISHED'}