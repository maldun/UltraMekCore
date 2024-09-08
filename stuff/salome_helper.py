from collections import deque
import numpy as np
import os
import json
from functools import reduce

import salome
salome.salome_init_without_session()
import GEOM
from salome.geom import geomBuilder
from salome.smesh import smeshBuilder
import SMESH
geompy = geomBuilder.New()
smesh = smeshBuilder.New()
gg = salome.ImportComponentGUI("GEOM")

ORIGIN = (0,0,0)
from math import sin, cos, pi

def compute_weighted_normal(mesh,nid):
    faces = mesh.GetElementsByNodes([nid]) 
    faces = [eid for eid in faces if mesh.GetElementType(eid) == SMESH.FACE]
    if len(faces) == 0: # does not border a face
        return None
    n = np.zeros(3)
    for fid in faces:
        nf = np.array(mesh.GetFaceNormal(fid,normalized=False))
        af = mesh.GetArea(fid)
        n =n+nf*af
    n /= len(faces)
    n /= np.linalg.norm(n)
    return n.tolist()

class Hexagon:
    HEX=6
    def __init__(self,length,height,unit_height=0.5,origin=ORIGIN,nr_segments=2,name="hex"):
        self.length = length
        self.height = height
        self.origin = origin
        self.unit_height = unit_height
        self.nr_segments = nr_segments
        self.name = name
    def create_hex_in_local_coords(self):
        self.o = geompy.MakeVertex(*self.origin)
        self.verts = []
        self.lines = []
        self.faces = []
        alpha = pi/3
        for k in range(self.HEX):
            x = self.origin[0] + self.length*cos(k*alpha)
            y = self.origin[1] + self.length*sin(k*alpha)
            z = self.origin[2]
            p = geompy.MakeVertex(x,y,z)
            self.verts += [p]
            #self.lines += [geompy.MakeLineTwoPnt(o, p)]
            
        d = [self.verts[-1]] + self.verts[:-1]
        for p1,p2 in zip(self.verts,d):
            self.lines += [geompy.MakeLineTwoPnt(p1, p2)]
        # create Wire
        self.outline = geompy.MakePolyline(self.verts+[self.verts[0]])
        # create face 
        self.face = geompy.MakeFace(self.outline, True)

    def publish(self):
        geompy.addToStudy(self.o,self.name+"_OO")
        for k,p in enumerate(self.verts):
            geompy.addToStudy(p,self.name+f"_point{k}")
        for k,l in enumerate(self.lines):
            geompy.addToStudy(l,self.name+f"_line{k}")
        geompy.addToStudy(self.outline,self.name+"_outline")
        geompy.addToStudy(self.face,self.name+"_face")
        
    def create_base_mesh(self):
        self.base_mesh = smesh.Mesh(self.face, self.name)
        algo1D = self.base_mesh.Segment()
        algo1D.NumberOfSegments(self.nr_segments)
        algo2d = self.base_mesh.Triangle() 
        algo2d.LengthFromEdges() 
        if not self.base_mesh.Compute(): raise Exception("Error when computing Mesh")
        self.b_group = self.base_mesh.CreateEmptyGroup(SMESH.FACE, self.name)
        self.b_group.AddFrom(self.base_mesh.mesh)
        self.bn_group = self.base_mesh.CreateEmptyGroup(SMESH.NODE, self.name+'_nodes')
        self.bn_group.AddFrom(self.base_mesh.mesh)
        self.c_group = self.base_mesh.CreateEmptyGroup(SMESH.NODE, self.name+'_center')
        cfilter = smesh.GetFilter(SMESH.NODE, SMESH.FT_LyingOnGeom, self.o,self.length/(2*self.nr_segments))
        ids = self.base_mesh.GetIdsFromFilter(cfilter)
        self.c_group.Add(ids)
        
    def extrude_base_mesh(self,debug=False):
        if not hasattr(self,"base_mesh"):
            self.create_base_mesh()
        
        obj        = self.base_mesh
        stepVector = [0.,0.,self.unit_height]
        nbSteps    = self.height
        groups = self.base_mesh.ExtrusionSweepObject2D( obj, stepVector, nbSteps, MakeGroups=True )
        self.b_group.SetName(self.name+'_bot')
        self.bn_group.SetName(self.name+'_nodes_bot')
        self.t_group = [g for g in groups if g.GetName()==self.name+"_top"]
        self.tn_group = [g for g in groups if g.GetName()==self.name+"_nodes_top"]
        
        f_group = self.base_mesh.CreateEmptyGroup(SMESH.FACE, self.name+'_temp')
        f_group.AddFrom(self.base_mesh.mesh)
        self.base_mesh.QuadToTri(f_group.GetIDs(), SMESH.FT_MinimumAngle)
        
        self.f_group = self.base_mesh.CreateEmptyGroup(SMESH.FACE, self.name)
        self.f_group.AddFrom(self.base_mesh.mesh)
        
        nbrev = self.base_mesh.Reorient2DBy3D([ self.f_group, ], self.base_mesh, theOutsideNormal=True)
        
        self.n_group = self.base_mesh.CreateEmptyGroup(SMESH.NODE, self.name)
        self.n_group.AddFrom(self.base_mesh.mesh)
        
        if debug is True:
            print("Reoriented:", nbrev)
            return groups
        
    def remove_volumes(self):
        v_group = self.base_mesh.CreateEmptyGroup(SMESH.VOLUME, self.name+'_vols')
        v_group.AddFrom(self.base_mesh.mesh)
        vids = v_group.GetIDs()
        self.base_mesh.RemoveElements(vids)
        self.base_mesh.RemoveOrphanNodes()
        
    def to_json(self,fname='hexa1.json'):
        self.remove_volumes()
        msh = self.base_mesh
        nids = self.n_group.GetIDs()
        node_id_map = {nid:k for k,nid in enumerate(nids)}
        vert_dic = {node_id_map[nid]: msh.GetNodeXYZ(nid) for nid in nids}
        normal_dic = {node_id_map[nid]: compute_weighted_normal(msh,nid) for nid in nids}
        
        dic = {}
        dic['verts'] = [vert_dic[k] for k in range(len(nids))]
        dic['normals'] = [normal_dic[k] for k in range(len(nids))]
        dic['center_id'] = node_id_map[self.c_group.GetIDs()[0]]
        dic['center_coord'] = msh.GetNodeXYZ(self.c_group.GetIDs()[0])
        
        dic['order'] = reduce(lambda a,b: a+b,[msh.GetElemNodes(fid) for fid in self.f_group.GetIDs()])
        dic['order'] = [node_id_map[nid] for nid in dic['order']]
        with open(fname,'w') as f:
            json.dump(dic,f,indent=4)
        return dic
        
        
            
if __name__ == "__main__":
    hexa = Hexagon(1.0,5)
    hexa.create_hex_in_local_coords()
    hexa.publish()
    hexa.create_base_mesh()
    groups = hexa.extrude_base_mesh(True)
    hexa.to_json("/home/maldun/Games/Godot/UltraMek/hexa.json")
