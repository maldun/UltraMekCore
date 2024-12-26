import os
import sys

#wpath = os.path.split(__file__)[0]
wpath = "/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/"
sys.path.append(wpath)

import json
import create_mesh
from create_mesh import MekMeshFactory , MeshPart, MekMaterialFactory
from create_skeleton import MekSkeletonFactory, Animation

#blender packages
import bpy
import mathutils



class MekUnit:
    #FIX_KEY = "fixations"
    TYPE_KEY = "type"
    NAME_KEY = "name"
    SCALE_KEY = "scale_factors"
    GENERAL_KEYS = {NAME_KEY,TYPE_KEY,SCALE_KEY}
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
    MATERIALS_KEYW = "materials"
    PARTS_KEYW = "parts"
    BONES_KEYW = "bones"
    COLLECTION_KEYWS = {PARTS_KEYW, BONES_KEYW}
    AUTO_MODE = 'ARMATURE_AUTO'
    ENVELOPE_MODE = 'ARMATURE_ENVELOPE'
    ARMATURE_MODES = {'auto':AUTO_MODE,'envelope':ENVELOPE_MODE}
    ARMATURE_MODE_KEYW = "armature_mode"
    
    def __init__(self,data,materials=wpath+os.sep+"materials.json"):
        if isinstance(data,str):
            with open(data,'r') as fp:
                data = json.load(fp)
        elif isinstance(data,dict):
            pass
        else:
            raise TypeError("Error: Data type not supported!")    
        
        # create mesh
        part_data = data[MekUnit.PARTS_KEYW]
        self._meshes = type(self)._get_key_dict() # get default keys for class
        MekUnit._key_check(self._meshes,part_data) # check if minimal set of keys is avaiailable
        self._meshes.update(MekUnit._get_key_dict()) # get default keys for base class
        
        # set common data
        self._set_data({key:val for key,val in data.items() if key not in MekUnit.COLLECTION_KEYWS})
        # set part data
        self._set_data(part_data)
        # create parts
        self.mesh_parts = self.create_mesh_parts(part_data)
        self.part_data = part_data
        
        with open(materials,'r') as fp:
            material_data = json.load(fp)
        self.materials = MekMaterialFactory.create_material_dict(material_data)
        MekUnit.apply_materials(self.mesh_parts,part_data,self.materials)
        
        # create armature
        bone_data = data[MekUnit.BONES_KEYW]
        self._bones = type(self)._get_key_dict(suffix="_BONE")
        MekUnit._key_check(self._bones,bone_data) # check if minimal set of keys is avaiailable
        self._bones.update(MekUnit._get_key_dict(suffix="_BONE"))
        self._set_data(bone_data)
        self.skeleton = self.create_skeleton(bone_data)
        
        # link everything together
        arm_mode = getattr(self,MekUnit.ARMATURE_MODE_KEYW)
        self.link_all(mode=arm_mode)
        # post scale
        self.post_scale(data[self.SCALE_KEY])
        
    
    @staticmethod
    def _key_check(default_dict,dict2):
        """
        Checkis if dict2 has all keys of default_dict and merges both
        """
        common = set(default_dict.values()) & set(dict2.keys())
        difference = set(default_dict.values()) - set(dict2.keys())
        if len(default_dict.keys())!=len(common):
            missing = ', '.join(list(difference))
            raise ValueError("Error! Keys" + missing + " missing!")
    
    @staticmethod
    def apply_materials(parts,data,materials):
        """
        Applies the materials given in material_data
        to each part defined in data.
        """
        for key, part in parts.items():
            dat = data[key]
            if dat is not None:
                mats = dat[MekUnit.MATERIALS_KEYW]
                for mat in mats:
                    part.apply_material(materials[mat])
                    
        
    @classmethod
    def _get_key_dict(cls,suffix="_KEY"):
        """
        Creates a dictionary of all constants ending with
        a defined suffix (default: '_KEY')
        """
        dic = {}
        for key, val in cls.__dict__.items():
            if key.endswith(suffix):
                nkey = key.split("_")[0]
                dic[nkey] = val
        return dic    
    
    @staticmethod
    def _get_data_key(key,data):
        """
        Convenience function which gets a key
        from a dictionary even if case does not
        match.
        """
        for dkey in data.keys():
            if dkey.lower() == key.lower():
                return dkey
            
        #raise KeyError(f"Error: Key {key} is missing in data!")
        return None
        
    def _set_data(self,data):
        """
        Convenience function which sets a object from
        from a dictionary and sets its a a member to the 
        object. Cases are ignored and the key is lower case.
        """
        for key, val in data.items():
            dkey = self._get_data_key(key,data)
            dat = data[dkey] if dkey is not None else None
            setattr(self,key.lower(),dat)            
            
    def create_mesh_parts(self,part_dict):
        """
        Creates the MeshParts for the meshes
        defined in the metadata set.
        """
        mesh_parts = {}
        for key, val in part_dict.items():
            if key not in MekUnit.GENERAL_KEYS:
                name = "_".join([self.name,key])
                data = getattr(self,key.lower())

                if data is not None:
                    mesh_parts[key] = self._create_mesh_part(data,name)
                else:
                    mesh_parts[key] = None
                
        return mesh_parts
    
    @staticmethod
    def _create_mesh(item):
        """
        Creates a bmesh and its signifikant points from meta data (item).
        """
        mesh_data = item[MekUnit.MESH_POSKEY]
        if mesh_data is None:
            return None, None
        if len(mesh_data) > 1:
            raise ValueError(f"Error: Mesh info not valid! Mesh data has {len(mesh_data)} entries!")
         
        mesh, points = MekMeshFactory.produce(mesh_data)
        return mesh, points
    
    @staticmethod    
    def _create_mesh_part(item,name):
        """
        Creates a MeshPart from meta data (item) with name (name).
        """
        mesh, fpoints = MekUnit._create_mesh(item)
        tpoints = item[MekUnit.AXIS_POSKEY]
        mesh_part = MeshPart(mesh,fpoints,tpoints,name)
        return mesh_part
        
    def create_skeleton(self,bone_data):
        """
        Creates the skeleton for the armature
        """
        root_name, root_data = self._get_skel_root()
        bones = {}
        for key, val in bone_data.items():
            name = '_'.join([self.name,key])
            data = getattr(self,key.lower())
            if isinstance(data,dict) and root_name!=key:
                bones[key.lower()] = data

        name = self.name + "_" + self.ARMATRUE_SUFFIX
        skel = MekSkeletonFactory.produce(name,root_data,bones)
        return skel
    
    def _get_skel_root(self):
        """
        Determines the root bone of the skeleton
        (which is created first).
        """
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
    
    def link_all(self,mode='auto'):
        """
        Links all bones together. Links are defined in the 
        metadata.
        """
        skel = self.skeleton
        arm = skel.get_armature()
        for key, val in self.mesh_parts.items():
            if val is not None:
                obj = val.publish()
                
        
        bpy.context.view_layer.objects.active = arm
        arm.select_set(True)
        
        mode = MekUnit.ARMATURE_MODES[mode] # map mode to correct key
        bpy.ops.object.parent_set(type=mode)
        #bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')
    
    
    def post_scale(self,scale_factors):
        """
        Scales the figure according to the defined scaling from the data
        """
        skel = self.skeleton
        arm = skel.get_armature()
        bpy.context.view_layer.objects.active = arm
        arm.select_set(True)
        
        arm.scale = mathutils.Vector(scale_factors)
        
    def create_animation(self,animation_data,name=None,loop=True):
        """
        Creates an animation from the metadata JSON File
        and pushes the action to NLA actions for easier export.
        """
        anim = Animation(animation_data)
        anim.apply_animation(self.skeleton,name=name,loop=loop)
        self.skeleton.push_action(name=name,loop=loop)
        
    def export_scene(self,fname):
        """
        Export the scene for use with other tools (like Godot)
        into file (fname). Note: The current format is optimized
        for use with Godot, other tools are currently not planned.
        """
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
    

def clear_scene():
    scene = bpy.context.scene
    bpy.data.scenes.new("Scene")
    bpy.data.scenes.remove(scene, do_unlink=True)
    bpy.data.scenes[0].name = "Scene"  
    
if __name__ == "__main__":
    clear_scene()
    
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
    
    sample_mek.create_animation("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/idle_animation.json",name="idle")
    sample_mek.create_animation("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/run_animation.json",name="run")
    sample_mek.create_animation("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/walk_animation.json",name="walk")
    
    
    sample_mek.export_scene("/home/maldun/Games/Godot/playground/anims.glb")