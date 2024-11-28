import os
import bpy
import json
import bmesh
import mathutils
import math
import numpy

PI = math.pi

class Mek:
    NR_U_SEGMENTS=32
    NR_V_SEGMENTS=32
    NR_BALL_DIVISIONS=2
    def __init__(self):
        self.mesh = bmesh.new()
    
    def add_mesh(self,bm):
        temp_mesh = bpy.data.meshes.new(".temp")
        bm.to_mesh(temp_mesh)
        self.mesh.from_mesh(temp_mesh)
        bpy.data.meshes.remove(temp_mesh)
    
    
    def _create_box(self,center=(0,0,0),dims=(1,1,1),rot=(0,0,0)):
        """
        Creates a box from a cube, with dimensions dims, and rotation rot at postion center.
        """
        bm = bmesh.new()
        eul = mathutils.Euler(rot, 'XYZ')
        dim_matrix = mathutils.Matrix.LocRotScale(center,eul,dims)
        bmesh.ops.create_cube(bm,size=1,matrix=dim_matrix,calc_uvs=True)
        return bm
    
    def create_box(self,center=(0,0,0),dims=(1,1,1),rot=(0,0,0)):
        bm = self._create_box(center=center,dims=dims,rot=rot)
        self.add_mesh(bm)
    
    def _create_ball(self,center=(0,0,0),radius=1):
        bm = bmesh.new()
        dim_matrix = mathutils.Matrix.LocRotScale(center,None,(0,0,0))
        bmesh.ops.create_uvsphere(bm, u_segments=self.NR_U_SEGMENTS, 
        v_segments=self.NR_V_SEGMENTS, radius=radius)
        return bm
    
    def create_ball(self,center=(0,0,0),radius=1):
        bm = self._create_ball(center=center,radius=radius)
        self.add_mesh(bm)
        
    def _extrude_faces(self,faces,height,normal=(0,0,1)):
        bm = bmesh.new()
        reg = bmesh.ops.extrude_face_region(bm, geom=faces)
        verts = [e for e in reg['geom'] if isinstance(e, bmesh.types.BMVert)]
        
        bmesh.ops.translate(bm, vec=mathutils.Vector(normal)*height, verts=verts)
        return bm, verts
    
    def extrude_faces(self,faces,height,normal=(0,0,0)):
        bm, verts = self._extrude_faces(faces,height,normal=normal)
        self.add_mesh(bm)
        return verts
        
    def _create_triangle(self,points):
        """
        points = (A,B,C) for a triangle in the plane.
        """
        bm = bmesh.new()
        verts = [bm.verts.new(co) for co in points]
        face = bm.faces.new(verts)
        return bm, verts, face
    
    def create_triangle(self,points):
        bm, verts, face = self._create_triangle(points)
        self.add_mesh(bm)
        return verts, face
        
    def create_prism(self,coords,height):
        verts, face = self.create_triangle(coords)
        self.extrude_faces([face],height)
    
    def _create_prism_like(self,face,height):
        self.extrude_faces([face],height)
        
    def move_face(self,face,center=(0,0,0),rot=(0,0,0),matrix=None):
        bm = self.mesh
        c = face.calc_center_median()
        center = mathutils.Vector(center)
        if matrix is None:
            eul = mathutils.Euler(rot, 'XYZ')
            matrix = mathutils.Matrix.LocRotScale(center-c,eul,(1,1,1))

        bmesh.ops.transform(bm, matrix=matrix, verts=face.verts) #, space=T)
    
    def create_equilateral_triangle(self,base=1.0,side=-1):
        if side <= 0:
            side = base
        h = (side**2-base**2/4)**0.5
        coords = [[0,0,0],[base,0,0],[base/2,h,0]]
        _, face = self.create_triangle(coords)
        return face
    
    def create_regular_prism(self,center=(0,0,0),rot=(0,0,0),base=1.0,side=-1,height=1):
        bm = self.mesh
        center = (center[0],center[1],center[2]-height/2)
        face = self.create_equilateral_triangle(base=base,side=side)
        self.move_face(face,center=center,rot=(0,0,0)) #rot)
        eul = mathutils.Euler(rot, 'XYZ')
        rot_matrix = mathutils.Matrix.LocRotScale((0,0,0),eul,(1,1,1))
        #normal = rot_matrix @ mathutils.Vector((0,0,1))
        prism = self.extrude_faces([face],height,) #normal=normal)
        bmesh.ops.rotate(bm,verts=prism,cent=center,matrix=rot_matrix)
        
    def mesh2blender(self):
        me = bpy.data.meshes.new("Mesh")
        self.mesh.to_mesh(me)
        
        obj = bpy.data.objects.new("Object", me)
        bpy.context.collection.objects.link(obj)

        # Select and make active
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

    def __del__(self):
        self.mesh.free()        
    


if __name__ == "__main__":
    mek = Mek()
    #mek.create_box((0,0,0),[1,2,3])
    #mek.create_ball((5,5,5),1)
    coords = [[0,0,0],[0,1,0],[1,1,0]]
    d_, face = mek.create_triangle(coords)
    #mek.move_face(face)
    #mek.create_prism(coords,2)
    #mek.create_regular_prism(rot=(PI/2,0,0))
    mek.mesh2blender()
        
