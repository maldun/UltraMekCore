import os
import sys

#wpath = os.path.split(__file__)[0]
wpath = "/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/"
sys.path.append(wpath)

import json
import create_mesh
from create_mesh import MekMeshFactory, MeshPart

class MekGeometry:
    #FIX_KEY = "fixations"
    TYPE_KEY = "type"
    NAME_KEY = "name"
    GENERAL_KEYS = {NAME_KEY,TYPE_KEY}
    # Keys related to positining
    CONNECTIONS_POSKEY = "connections"
    JOINTS_POSKEY = "joints"
    AXIS_POSKEY = "axis"
    MESH_POSKEY = "mesh"
    
    
    def __init__(self,data):
        if isinstance(data,str):
            with open(data,'r') as fp:
                data = json.load(fp)
        elif isinstance(data,dict):
            pass
        else:
            raise TypeError("Error: Data type not supported!")    
        
        self._dic = type(self)._get_key_dict()
        self._dic.update(MekGeometry._get_key_dict())
        self._set_data(data)
        self.mesh_parts = self.create_mesh_parts()
        
    @classmethod
    def _get_key_dict(cls,suffix="_KEY"):
        dic = {}
        for key, val in cls.__dict__.items():
            if key.endswith(suffix):
                nkey = key.split("_")[0]
                dic[nkey] = val
        return dic    
    
    @staticmethod
    def _get_data_key(key,data):
        for dkey in data.keys():
            if dkey.lower() == key.lower():
                return dkey
            
        raise KeyError(f"Error: Key {key} is missing in data!")
        
    def _set_data(self,data):
        for key, val in self._dic.items():
            dkey = self._get_data_key(val,data)
            setattr(self,val.lower(),data[dkey])
            
    def create_mesh_parts(self):
        mesh_parts = {}
        for key, val in self._dic.items():
            if val not in MekGeometry.GENERAL_KEYS:
                name = "_".join([self.name,val])
                data = getattr(self,val.lower())

                if data is not None:
                    mesh_parts[val] = self._create_mesh_part(data,name)
                else:
                    mesh_parts[val] = None
                
        return mesh_parts
    
    @staticmethod
    def _create_mesh(item):
        mesh_data = item[MekGeometry.MESH_POSKEY]
        if mesh_data is None:
            return None, None
        if len(mesh_data) > 1:
            raise ValueError(f"Error: Mesh info not valid! Mesh data has {len(mesh_data)} entries!")
         
        mesh, points = MekMeshFactory.produce(mesh_data)
        return mesh, points
    
    @staticmethod    
    def _create_mesh_part(item,name):
        mesh, fpoints = MekGeometry._create_mesh(item)
        tpoints = item[MekGeometry.AXIS_POSKEY]
        with open("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/log.log",'w') as fp:
            fp.write(str(mesh)+str(fpoints)+str(tpoints))
        mesh_part = MeshPart(mesh,fpoints,tpoints,name)
        return mesh_part
        
                
class BipedMekGeometry(MekGeometry):
    H_KEY = "head"
    
    LT_KEY = "left_torso"
    RT_KEY  = "right_torso"
    CT_KEY  = "center_torso"
    
    LUA_KEY  = "left_upper_arm"
    LEB_KEY = "left_elbow"
    LLA_KEY = "left_lower_arm"
    LHA_KEY = "left_hand"
    
    RUA_KEY = "right_upper_arm"
    REB_KEY = "right_elbow"
    RLA_KEY = "right_lower_arm"
    RHA_KEY = "right_hand"
    
    LUL_KEY = "left_upper_leg"
    LKN_KEY = "left_knee"
    LLL_KEY = "left_lower_leg"
    LFO_KEY = "left_foot"
    
    RUL_KEY = "right_upper_leg"
    RKN_KEY = "right_knee"
    RLL_KEY = "right_lower_leg"
    RFO_KEY = "right_foot"
    
if __name__ == "__main__":
    sample_mek = BipedMekGeometry("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/boxi.json")    
    
    #with open("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/log.log",'w') as fp:
    #    fp.write(str(sample_mek.mesh_parts))
        
    for key, val in sample_mek.mesh_parts.items():
        if val is not None:
            val.publish()
            
        