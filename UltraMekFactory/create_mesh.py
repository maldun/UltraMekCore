import os
import bpy
import json
import bmesh
import mathutils
import math
import numpy
from dataclasses import dataclass

PI = math.pi

class MekMeshFactory:
    NR_U_SEGMENTS=32
    NR_V_SEGMENTS=32
    
    @staticmethod
    def create_box(center=(0,0,0),dims=(1,1,1),rot=(0,0,0)):
        """
        Creates a box from a cube, with dimensions dims, and rotation rot at postion center.
        """
        bm = bmesh.new()
        eul = mathutils.Euler(rot, 'XYZ')
        dim_matrix = mathutils.Matrix.LocRotScale(center,eul,dims)
        bmesh.ops.create_cube(bm,size=1,matrix=dim_matrix,calc_uvs=True)
        return bm  
    
    @staticmethod
    def rot_line(points,rot=(0,0,0)):
        """
        Rotates a set of points (which define a line)
        by the given roation vector (rot).
        """
        if rot != (0,0,0):
            eul = mathutils.Euler(rot)
            Q = numpy.array(eul.to_matrix())
            for k, p in enumerate(points):
                points[k] = numpy.dot(Q,p)
            points = [tuple(p) for p in points]
        return points
    
    @staticmethod
    def box_points(center=(0,0,0),dims=(1,1,1),rot=(0,0,0)):
        """
        Creates and toates the points which determine the cube.
        """
        points = [(center[0],center[1],dims[2]/2+center[2]),
                  (center[0],center[1],center[2]-dims[2]/2)]
        
        points = MekMeshFactory.rot_line(points,rot=rot)
        return points
    
    @staticmethod
    def box(center=(0,0,0),dims=(1,1,1),rot=(0,0,0)):
        """
        Create a box mesh given by a center, dimensions (lengths of sides) 
        and rotation vector (Euler). Returns the mesh and the points used for
        connecting with other meshes.
        """
        mesh = MekMeshFactory.create_box(center=center,dims=dims,rot=rot)
        points = MekMeshFactory.box_points(center=center,dims=dims,rot=rot)
        return mesh, points
        
    @staticmethod
    def create_ball(center=(0,0,0),radius=1):
        bm = bmesh.new()
        dim_matrix = mathutils.Matrix.LocRotScale(center,None,(0,0,0))
        bmesh.ops.create_uvsphere(bm, u_segments=MekMeshFactory.NR_U_SEGMENTS, 
        v_segments=MekMeshFactory.NR_V_SEGMENTS, radius=radius)
        return bm
    
    @staticmethod
    def extrude_faces(bm, faces,height,normal=(0,0,1)):
        """
        Extrudes a set of faces from a mesh in direction of the normal
        vector and returns the extruded mesh.
        """
        reg = bmesh.ops.extrude_face_region(bm, geom=faces)
        verts = [e for e in reg['geom'] if isinstance(e, bmesh.types.BMVert)]
        
        bmesh.ops.translate(bm, vec=mathutils.Vector(normal)*height, verts=verts)
        return bm, verts
    
    @staticmethod
    def create_triangle(self,points):
        """
        points = (A,B,C) for a triangle in the plane.
        """
        bm = bmesh.new()
        verts = [bm.verts.new(co) for co in points]
        face = bm.faces.new(verts)
        return bm, verts, face
    
    @staticmethod
    def create_equilateral_triangle(self,base=1.0,side=-1):
        if side <= 0:
            side = base
        h = (side**2-base**2/4)**0.5
        coords = [[0,0,0],[base,0,0],[base/2,h,0]]
        bm, verts, face = MekPartCreator.create_triangle(coords)
        return bm,verts,face
    
    @staticmethod
    def move_face(bm,face,center=(0,0,0),rot=(0,0,0),matrix=None):
        """
        Moves a face from its center median to the given center
        point. It also adds rotation or a transform matrix which moves
        the faces accordingly.
        """
        c = face.calc_center_median()
        center = mathutils.Vector(center)
        if matrix is None:
            eul = mathutils.Euler(rot, 'XYZ')
            matrix = mathutils.Matrix.LocRotScale(center-c,eul,(1,1,1))

        bmesh.ops.transform(bm, matrix=matrix, verts=face.verts) #, space=T)
        return bm
    
    @staticmethod
    def create_regular_prism(self,center=(0,0,0),rot=(0,0,0),base=1.0,side=-1,height=1):
        """
        Creates a prism with equilateral triangle as base
        """
        center = (center[0],center[1],center[2]-height/2)
        bm, verts, face = MekPartCreator.create_equilateral_triangle(base=base,side=side)
        bm = self.move_face(face,center=center,rot=(0,0,0)) #rot)
        eul = mathutils.Euler(rot, 'XYZ')
        rot_matrix = mathutils.Matrix.LocRotScale((0,0,0),eul,(1,1,1))
        #normal = rot_matrix @ mathutils.Vector((0,0,1))
        bm, prism = MekPartCreator.extrude_faces(bm,[face],height,) #normal=normal)
        bmesh.ops.rotate(bm,verts=prism,cent=center,matrix=rot_matrix)
        return bm
    
    @staticmethod
    def join_mesh(bm1,bm2):
        """
        Joins two bmesh'es together to a single bmesh.
        """
        temp_mesh = bpy.data.meshes.new(".temp")
        bm2.to_mesh(temp_mesh)
        bm1from_mesh(temp_mesh)
        bpy.data.meshes.remove(temp_mesh)
        return bm1

    @staticmethod
    def bmesh2mesh(bm,name="Mesh"):
        """
        Creates a blender mesh from a bmesh.
        """
        me = bpy.data.meshes.new(name)
        bm.to_mesh(me)
        return me
        

    @staticmethod    
    def mesh2blender(bm,obj_name="Object",mesh=None):
        """
        Publishes a mesh as blender object.
        """
        if mesh is None:
            me = MekMeshFactory.bmesh2mesh(bm)        
        else:
            me = mesh
        
        obj = bpy.data.objects.new(obj_name, me)
        bpy.context.collection.objects.link(obj)

        # Select and make active
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        return obj
    
    creators = {"box":box}
    
    @staticmethod
    def produce(data):
        """
        Reads data from a dictionary and creates the mesh.
        This is WIP so nothing set in stone yet ...
        The meta-data format is implicitely defined by the 
        corresponding functions in the creators dictionary.
        """
        mtype = list(data.keys())[0]
        mparams = data[mtype]
        mesh, joints = MekMeshFactory.creators[mtype](**mparams)
        return mesh, joints

@dataclass
class MekMaterial:
    name: str
    mat: object
    bsdf: object

class MekMaterialFactory:
    """
    Creates material from a dictionary of data, which in return
    can be retrieved from JSONS
    """
    NAME_MAT = "name"
    PBSDF_KEYW = "Principled BSDF"
    PBSDF_PROPERTY_MAP = {
    "Base Color":0,
    "Metallic":1,
    "Roughness":2,
    "IOR":3,
    "Alpha":4,
    "Normal":5,
    "Weight":6,
    "Diffuse Roughness":7,
    "Subsurface Weight":8,
    "Subsurface Radius":9,
    "Subsurface Scale":10,
    "Subsurface IOR":11,
    "Subsurface Anisotropy":12,
    "Specular IOR Level":13,
    "Specular Tint":14,
    "Anisotropic":15,
    "Anisotropic Rotation":16,
    "Tangent":17,
    "Transmission Weight":18,
    "Coat Weight":19,
    "Coat Roughness":20,
    "Coat IOR":21,
    "Coat Tint":22,
    "Coat Normal":23,
    "Sheen Weight":24,
    "Sheen Roughness":25,
    "Sheen Tint":26,
    "Emission Color":27,
    "Emission Strength":28,
    "Thin Film Thickness":29,
    "Thin Film IOR":30
    }
    
    
    @staticmethod
    def create_material(name,material_data):
        """
        Creates material from data.
        """
        #name = material_data[MekMaterialFactory.NAME_MAT]
        
        mat = bpy.data.materials.new(name)
        bsdf = MekMaterialFactory.create_principled_bsdf_obj(mat)
        bsdf = MekMaterialFactory.apply_data(bsdf,material_data)

        #bpy.context.object.data.materials.append(mat)
        mater = MekMaterial(name,mat,bsdf)
        return mater
        
    @staticmethod
    def create_material_dict(material_data_dict):
        """
        Create a dict with MekMAterial objects for applycation
        on meshes.
        """
        mat_dict = {}
        for key,val in material_data_dict.items():
            mat = MekMaterialFactory.create_material(key,val)
            mat_dict[key] = mat
            
        return mat_dict
        

    @staticmethod        
    def create_principled_bsdf_obj(mat):
        """
        Creates a principled bsdf object.
        pbdsf is the only format Godot can 100% 
        support
        """
        mat.use_nodes = True
        mat_nodes = mat.node_tree.nodes
        bsdf = mat_nodes[MekMaterialFactory.PBSDF_KEYW]
        return bsdf

        
    @staticmethod
    def apply_data(bsdf,material_data):
        """
        Apply data to principled bsdf
        """
        m = MekMaterialFactory.PBSDF_PROPERTY_MAP # make short hand for map
        for key, i in m.items():
            # we allow some variants in the definition
            key_snake = key.replace(" ","_")
            key_usnake = key_snake.upper()
            key_lsnake = key_snake.lower()
            value = None
            if key in material_data.keys():
                value = material_data[key]
            elif key_snake in material_data.keys():
                value = material_data[key_snake]
            elif key_usnake in material_data.keys():
                value = material_data[key_usnake]
            elif key_lsnake in material_data.keys():
                value = material_data[key_lsnake]

            if value is not None:
                bsdf.inputs[i].default_value = value
                
        return bsdf
                
        
class MeshPart:
    """
    Class for Mesh parts.
    bmesh: bmesh of the part
    joints: list of point representing the joints used for connections 
    """
    MESH_SUFFIX = "_mesh"
    def __init__(self,bm,fpoints,tpoints,name):
        self.bmesh = bm
        self.from_points = fpoints
        self.to_points = tpoints
        self.name = name
        if bm != None:
            self.rotate_mesh_into_connection(self.bmesh,fpoints[0],fpoints[1],tpoints[0],tpoints[1])
            
        if bm is None:
            self.msh = None
        else:
            self.msh = MekMeshFactory.bmesh2mesh(self.bmesh,name=self.name+MeshPart.MESH_SUFFIX)
        
    def publish(self):
        """
        Publishes the part, i.e. a Blender object with the mesh is created.
        """
        if self.bmesh is None:
            return None
        
        obj = MekMeshFactory.mesh2blender(self.bmesh,self.name,mesh=self.msh)
        self.obj = obj
        return obj
    
    def apply_material(self,material):
        """
        Applies material to the part.
        """
        if self.msh is not None:
            self.msh.materials.append(material.mat)
        
    
    def __del__(self):
        """
        Frees the bmesh at end of live of the object to
        simplify cleanup.
        """
        self.bmesh.free()
    
    @staticmethod
    def _compute_transform_matrix(p1,p2,q1,q2):
        """
        Computes the transform matrix to fit a part properly between 2 joints
        """
        # scaling
        vec1 = mathutils.Vector(p2)-mathutils.Vector(p1)
        vec2 = mathutils.Vector(q2)-mathutils.Vector(q1)
        
        print(vec1)
        n1 = numpy.linalg.norm(vec1)
        n2 = numpy.linalg.norm(vec2)
        if n1 >0 and n2 >0:
            s = n2/n1
        else:
            raise Exception("Error: Zero Length vector!")
            
        # rotation
        w1 = vec1.normalized()
        w2 = vec2.normalized()
        
        # Q w1 = (x,0,0), x = +/-1
        # P w2 = (y,0,0), y = +/-1
        # sign(x) Q w1 = sign(y) P w2
        # w2 = sign(x)sign(y) P* Q w1
        # => rot = sign(x)sign(y) P* Q 
        
        w1a = numpy.array(w1).reshape((len(w1),1))
        w2a = numpy.array(w2).reshape((len(w2),1))
        
        Q, X = numpy.linalg.qr(w1a,mode="complete")
        P, Y = numpy.linalg.qr(w2a,mode="complete")
        x = X[0]; y = Y[0]
        rot = numpy.dot(P.T,Q)*numpy.sign(x)*numpy.sign(y)
        # translation        # Tpc -> qc
        pc = (mathutils.Vector(p2)+mathutils.Vector(p1))/2
        qc = (mathutils.Vector(q2)+mathutils.Vector(q1))/2
        translation_vec = numpy.array(qc) - numpy.dot(rot,pc)
        
        # convert into proper data types
        translation_vec = mathutils.Vector(translation_vec)
        rot = mathutils.Matrix(rot)
        trafo_matrix = mathutils.Matrix.LocRotScale(translation_vec,rot,(s,s,s))
        return trafo_matrix
        
    @staticmethod
    def rotate_mesh_into_connection(bm,p1,p2,q1,q2):
        # translate center of line (p1,p2) into origin 
        # to avoid problems with scaling
        p1v = mathutils.Vector(p1)
        p2v = mathutils.Vector(p2)
        pc = (p1v+p2v)/2
        p1s = p1v - pc
        p2s = p2v - pc
        T1 = MeshPart._compute_transform_matrix(p1,p2,p1s,p2s)
        bmesh.ops.transform(bm,matrix=T1,verts=bm.verts)
        T2 = MeshPart._compute_transform_matrix(p1s,p2s,q1,q2)
        bmesh.ops.transform(bm,matrix=T2,verts=bm.verts)
        return bm

    
           

if __name__ == "__main__":
    # test MekPart Creator
    # First clean up
    scene = bpy.context.scene
    bpy.data.scenes.new("Scene")
    bpy.data.scenes.remove(scene, do_unlink=True)
    bpy.data.scenes[0].name = "Scene"
    
    bm_boxx = MekMeshFactory.create_box(center=(0,0,0),dims=(1,2,3))
    boxx_msh = MekMeshFactory.bmesh2mesh(bm_boxx)
    boxx_obj = MekMeshFactory.mesh2blender(bm_boxx,"ColorBox",mesh=boxx_msh)  
    mat_data = {MekMaterialFactory.NAME_MAT: "mat1",
                "base_color": (1,0,0,1)}    
    
    mater = MekMaterialFactory.create_material(name,mat_data)
    boxx_msh.materials.append(mater.mat)
    
    
    bm_boxx.free() 
    
    #mek = Mek()
    #mek.create_box((0,0,0),[1,2,3])
    #mek.create_ball((5,5,5),1)
    coords = [[0,0,0],[0,1,0],[1,1,0]]
    #d_, face = mek.create_triangle(coords)
    #mek.move_face(face)
    #mek.create_prism(coords,2)
    #mek.create_regular_prism(rot=(PI/2,0,0))
    #mek.mesh2blender()
    
    bm_ball = MekMeshFactory.create_ball()
    MekMeshFactory.mesh2blender(bm_ball)
    bm_ball.free()  
    
    bm_box = MekMeshFactory.create_box(center=(0,0,0),dims=(1,2,3))
    box_obj = MekMeshFactory.mesh2blender(bm_box,"Box")    
    bm_box.free()    
    
    
    T = MeshPart._compute_transform_matrix((0,0,1),(0,0,-1),(1,0,0),(0,0,0))
    bm_box = MekMeshFactory.create_box(center=(0,0,0),dims=(1,2,3))
    bmesh.ops.transform(bm_box,matrix=T,verts=bm_box.verts)
    box_obj2 = MekMeshFactory.mesh2blender(bm_box,"BoxT") 
    bm_box.free()
    
    test_data = {"box":{"dims":[1,1,3],"rot":[0,numpy.pi/4,0]}}
    mesh, points = MekMeshFactory.produce(test_data)
    
    box_obj = MekMeshFactory.mesh2blender(mesh,"Box2")    
    mesh.free()
    
    pfrom = ((0,0,-2),(0,0,2))
    pto = ((1,0,0),(0,0,0))
    bm_box = MekMeshFactory.create_box(center=(0,0,0),dims=(1,2,4))
    box_part = MeshPart(bm_box,pfrom,pto,"BoxPart")
    box_part.publish()

    data = {"mesh":None,"axis": [[0,-0.75,1.05],[0,-0.75,1.1]]}
    bm = data["mesh"]
    q1,q2 = data['axis']
    MeshPart(bm,None,[q1,q2],'none')
    