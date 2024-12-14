import os
import sys

#wpath = os.path.split(__file__)[0]
wpath = "/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/"
sys.path.append(wpath)

import json
import create_mesh
from create_mesh import MekMeshFactory, MeshPart
from create_skeleton import MekSkeletonFactory

class MekUnit:
    #FIX_KEY = "fixations"
    TYPE_KEY = "type"
    NAME_KEY = "name"
    GENERAL_KEYS = {NAME_KEY,TYPE_KEY}
    # Keys related to positining
    CONNECTIONS_POSKEY = "connections"
    JOINTS_POSKEY = "joints"
    AXIS_POSKEY = "axis"
    MESH_POSKEY = "mesh"
    SKEL_POSKEY = "armature"
    # Center for armature
    CENTER_BONE = "armature_center"
    PARENT_BKEY = "parent"
    ROOT_BKEY = "root"
    ARMATRUE_SUFFIX = "armature"
    
    def __init__(self,data):
        if isinstance(data,str):
            with open(data,'r') as fp:
                data = json.load(fp)
        elif isinstance(data,dict):
            pass
        else:
            raise TypeError("Error: Data type not supported!")    
        
        # create mesh 
        self._meshes = type(self)._get_key_dict()
        self._meshes.update(MekUnit._get_key_dict())
        self._set_data(data,self._meshes)
        self.mesh_parts = self.create_mesh_parts()
        
        # create armature
        self._bones = type(self)._get_key_dict(suffix="_BONE")
        self._bones.update(MekUnit._get_key_dict(suffix="_BONE"))
        self._set_data(data,self._bones)
        self.skeleton = self.create_skeleton()
        
        
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
            
        #raise KeyError(f"Error: Key {key} is missing in data!")
        return None
        
    def _set_data(self,data,dic):
        for key, val in dic.items():
            dkey = self._get_data_key(val,data)
            dat = data[dkey] if dkey is not None else None
            setattr(self,val.lower(),dat)            
            
    def create_mesh_parts(self):
        mesh_parts = {}
        for key, val in self._meshes.items():
            if val not in MekUnit.GENERAL_KEYS:
                name = "_".join([self.name,val])
                data = getattr(self,val.lower())

                if data is not None:
                    mesh_parts[val] = self._create_mesh_part(data,name)
                else:
                    mesh_parts[val] = None
                
        return mesh_parts
    
    @staticmethod
    def _create_mesh(item):
        mesh_data = item[MekUnit.MESH_POSKEY]
        if mesh_data is None:
            return None, None
        if len(mesh_data) > 1:
            raise ValueError(f"Error: Mesh info not valid! Mesh data has {len(mesh_data)} entries!")
         
        mesh, points = MekMeshFactory.produce(mesh_data)
        return mesh, points
    
    @staticmethod    
    def _create_mesh_part(item,name):
        mesh, fpoints = MekUnit._create_mesh(item)
        tpoints = item[MekUnit.AXIS_POSKEY]
        mesh_part = MeshPart(mesh,fpoints,tpoints,name)
        return mesh_part
        
    def create_skeleton(self):
        """
        Creates the skeleton for the armature
        """
        root_name, root_data = self._get_skel_root()
        bones = {}
        for key, val in self._bones.items():
            name = '_'.join([self.name,val])
            data = getattr(self,val.lower())
            if isinstance(data,dict) and root_name!=val:
                bones[val.lower()] = data
        with open("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/log.log",'w') as fp:
                json.dump(root_data,fp)
        name = self.name + "_" + self.ARMATRUE_SUFFIX
        skel = MekSkeletonFactory.produce(name,root_data,bones)
        return skel
    
    def _get_skel_root(self):
        
        for key, val in self._bones.items():
            dat = getattr(self,val)
            if dat[self.PARENT_BKEY] is None:
                root = val
                break
        else:
            raise KeyError("Error: No Root Bone defined!")
        
        root_bone = dat
        center = getattr(self,self.CENTER_BONE)
        root_data = {self.ROOT_BKEY:root,self.CENTER_BONE:center}
        root_data.update(root_bone)
        del root_data[self.PARENT_BKEY]
        return root, root_data
    
class BipedMekUnit(MekUnit):
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
    
    SKU_BONE = "skull"
    NEC_BONE = "neck"
    SPI_BONE = "spine"
    
    LSH_BONE = "left_shoulder"
    LUA_BONE = "left_upper_arm_bone"
    LLA_BONE = "left_lower_arm_bone"
    LHA_BONE = "left_hand_bone"
    
    RSH_BONE = "right_shoulder"
    RUA_BONE = "right_upper_arm_bone"
    RLA_BONE = "right_lower_arm_bone"
    RHA_BONE = "right_hand_bone"
    
    LHI_BONE = "left_hip"
    LTH_BONE = "left_tigh"
    LLL_BONE = "left_lower_leg_bone"
    LFO_BONE = "left_foot_bone"
    
    RHI_BONE = "right_hip"
    RTH_BONE = "right_tigh"
    RLL_BONE = "right_lower_leg_bone"
    RFO_BONE = "right_foot_bone"
    
    
    
if __name__ == "__main__":
    sample_mek = BipedMekUnit("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/boxi.json")    
    
    #with open("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/log.log",'w') as fp:
    #    fp.write(str(sample_mek.mesh_parts))
        
    for key, val in sample_mek.mesh_parts.items():
        if val is not None:
            val.publish()
            
        
