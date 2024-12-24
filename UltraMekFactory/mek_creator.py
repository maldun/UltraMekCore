import os
import sys

#wpath = os.path.split(__file__)[0]
wpath = "/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/"
sys.path.append(wpath)

import json
import create_mesh
from create_mesh import MekMeshFactory, MeshPart, MekMaterialFactory
from create_skeleton import MekSkeletonFactory, Animation

#blender packages
import bpy
import mathutils

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
    
    def __init__(self,data,materials=wpath+os.sep+"materials.json"):
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
        
        with open(materials,'r') as fp:
            material_data = json.load(fp)
        
        
        # create armature
        self._bones = type(self)._get_key_dict(suffix="_BONE")
        self._bones.update(MekUnit._get_key_dict(suffix="_BONE"))
        self._set_data(data,self._bones)
        self.skeleton = self.create_skeleton()
        
        # link everything together
        self.link_all()
        
        
    @classmethod
    def apply_materials(material_data):
        pass
        
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
    
    def link_all(self):
        skel = self.skeleton
        arm = skel.get_armature()
        for key, val in self.mesh_parts.items():
            if val is not None:
                obj = val.publish()
                
        
        bpy.context.view_layer.objects.active = arm
        arm.select_set(True)
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        
    def create_animation(self,animation_data,name=None,loop=True):
        anim = Animation(animation_data)
        anim.apply_animation(self.skeleton,name=name,loop=loop)
        self.skeleton.push_action(name=name,loop=loop)
        
    def export_scene(self,fname):
        bpy.ops.export_scene.gltf(filepath=fname,
                                  check_existing=False,
                                  export_animations=True,
                                  export_frame_range=True,
                                  export_frame_step=1,
                                  export_anim_slide_to_zero=True)
                                  
    
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
    RSH_KEY = "right_shoulder"
    
    LUL_KEY = "left_upper_leg"
    LKN_KEY = "left_knee"
    LLL_KEY = "left_lower_leg"
    LFO_KEY = "left_foot"
    LSH_KEY = "left_shoulder"
    
    RUL_KEY = "right_upper_leg"
    RKN_KEY = "right_knee"
    RLL_KEY = "right_lower_leg"
    RFO_KEY = "right_foot"
    
    SKU_BONE = "skull"
    NEC_BONE = "neck"
    SPI_BONE = "spine"
    
    LSH_BONE = "left_shoulder_bone"
    LUA_BONE = "left_upper_arm_bone"
    LLA_BONE = "left_lower_arm_bone"
    LHA_BONE = "left_hand_bone"
    
    RSH_BONE = "right_shoulder_bone"
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
    scene = bpy.context.scene
    bpy.data.scenes.new("Scene")
    bpy.data.scenes.remove(scene, do_unlink=True)
    bpy.data.scenes[0].name = "Scene"
    
    sample_mek = BipedMekUnit("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/boxi.json")    
    #breakpoint()
    
    arm = sample_mek.skeleton.armature_object
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="POSE",toggle=True)
    
    #fcurves = sample_mek.skeleton.armature.animation_data.action.fcurves
    #sample_mek.skeleton.armature_object.pose.bones['left_hand_bone'].rotation_euler = mathutils.Vector((1,0,0))
    #action=bpy.data.actions['ArmatureAction']
    #thebone=bpy.context.object.pose.bones['left_hand_bone']
    #thebone.rotation_euler=(-1.5,0.0,0.0)       
    #thebone.keyframe_insert(data_path='rotation_euler',frame=10)
    
    sample_mek.create_animation("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/run_animation.json",name="run")
    sample_mek.create_animation("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/walk_animation.json",name="walk")
    
    sample_mek.export_scene("/home/maldun/Games/Godot/playground/anims.glb")