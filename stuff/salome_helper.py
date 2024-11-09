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
        self.t_group = [g for g in groups if g.GetName()==self.name+"_top"][0]
        self.tn_group = [g for g in groups if g.GetName()==self.name+"_nodes_top"][0]
        
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
        
        dic['order'] = reduce(lambda a,b: a+b,[msh.GetElemNodes(fid) for fid in self.f_group.GetIDs() if fid not in self.t_group.GetIDs()])
        dic['order'] = [node_id_map[nid] for nid in dic['order']]
        
        tnids = self.tn_group.GetIDs()
        tnode_id_map = {nid:k for k,nid in enumerate(tnids)}
        tvert_dic = {tnode_id_map[nid]: msh.GetNodeXYZ(nid) for nid in tnids}
        def coord_shift(x,y): 
            l = self.length
            # v coordinate has to be mirrored due to inverted textures
            return [(x+l)/(2*l),1-(y+l)/(2*l)] 
        tuv_dic = {tnode_id_map[nid]: coord_shift(*msh.GetNodeXYZ(nid)[:2]) for nid in tnids}
        tnormal_dic = {tnode_id_map[nid]: compute_weighted_normal(msh,nid) for nid in tnids}
        
        dic['top_verts'] = [tvert_dic[k] for k in range(len(tnids))]
        dic['top_normals'] = [tnormal_dic[k] for k in range(len(tnids))]
        dic['top_order'] = reduce(lambda a,b: a+b,[msh.GetElemNodes(fid) for fid in self.t_group.GetIDs()])
        dic['top_order'] = [tnode_id_map[nid] for nid in dic['top_order']]
        dic['top_uv'] = [tuv_dic[k] for k in range(len(tnids))]
        
        dic['length'] = self.length
        dic['unit_height'] = self.unit_height
        dic['height'] = self.height
        dic['origin'] = list(self.origin)
        dic['nr_segments'] = self.nr_segments
        
        with open(fname,'w') as f:
            json.dump(dic,f,indent=4)
        return dic
        
min_h = -5
max_h = 10
hrange = max_h - min_h
unit_length = 1.0
unit_height = 0.5
path = os.path.expanduser("~/Games/Godot/UltraMek/UltraMekGodot/assets/hexes")

if __name__ == "__main__":
    for k in range(hrange):
        hexa = Hexagon(unit_length,k+1,unit_height=unit_height)
        hexa.create_hex_in_local_coords()
        hexa.publish()
        hexa.create_base_mesh()
        groups = hexa.extrude_base_mesh(True)
        fname = os.path.join(path,f"hexa_h{k-5}.json")
        hexa.to_json(fname)
