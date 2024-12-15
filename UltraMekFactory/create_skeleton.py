import os
import bpy
import json
#import bmesh
import mathutils
import math
import numpy
import copy

class Skeleton:
    def __init__(self,name="my_armature",root="skull",head=(0,0,0),tail=(0,0,1),armature_center=(0,0,0)):
        self.name = name
        armature, arm_obj, main_bone = MekSkeletonFactory.create_armature(name,root,head=head,tail=tail,center=armature_center)
        self.armature = armature
        self.armature_object = arm_obj
        setattr(self,root,main_bone)
        self._bones = {root}
            
    def add_bone(self,bone_name,head=(0,0,1),tail=(0,0,0),parent="skull"):
        if not hasattr(self,parent):
            return None
        self.armature_object.data.bones[parent].select=True
        bone = MekSkeletonFactory.create_bone(self.armature,self.armature_object,head,tail,bone_name,parent=parent)
        setattr(self,bone_name,bone_data)
        self._bones.update({bone_name})
        return bone
    
    def get_armature(self):
        return self.armature_object
    
    def create_animation_data(self,name="BoneAnimation"):
        self.armature_object.animation_data_create()
        self.armature_object.animation_data.action = bpy.data.actions.new(name=name)
        
    def select_bone(self,bone_name):
        bone = self.armature.bones[bone_name]
        bpy.context.object.data.bones.active = bone
        bone.select = True
        
        pbone = self.armature_object.pose.bones[bone_name]
        #bpy.context.active_pose_bone = pbone
        return pbone
         

class MekSkeletonFactory:
    """
    Class for creating a skeleton from data
    """
    EDIT_MODE = "EDIT"
    OBJECT_MODE = "OBJECT"
    ARMATURE_DEFAULT = "Armature"
    BONE_DEFAULT = "Bone"
    @staticmethod
    def create_armature(name,bone_name,head=(0,0,0),tail=(0,0,1),center=(0,0,0)):
        MekSkeletonFactory.switch_on_object_mode()
        bpy.ops.object.armature_add(location=center)
        for arm in bpy.data.armatures:
            if arm.name == MekSkeletonFactory.ARMATURE_DEFAULT:
                armature = arm
                break
        
        armature.name = name
        armature_obj =  bpy.context.scene.objects[MekSkeletonFactory.ARMATURE_DEFAULT]
        armature_obj.name = name + "_obj" 
        # get first bone
        MekSkeletonFactory.switch_on_edit_mode()
        main_bone = armature.edit_bones[MekSkeletonFactory.BONE_DEFAULT]
        main_bone.head = head
        main_bone.tail = tail
        main_bone.name = bone_name
        MekSkeletonFactory.switch_on_object_mode()
        #main_bone = None
        return armature, armature_obj , main_bone
        
    
    @staticmethod
    def switch_on_object_mode():
        if (bpy.context.mode != MekSkeletonFactory.OBJECT_MODE):
            bpy.ops.object.mode_set(mode=MekSkeletonFactory.OBJECT_MODE)
    
    @staticmethod
    def switch_on_edit_mode():
        if (bpy.context.mode != MekSkeletonFactory.EDIT_MODE):    
            bpy.ops.object.mode_set(mode=MekSkeletonFactory.EDIT_MODE,toggle=True)
    
    @staticmethod
    def setup_bone(bone,head,tail):
        MekSkeletonFactory.switch_on_edit_mode()
        bone.head = head
        bone.tail = tail
        return bone
    
    @staticmethod
    def create_bone(armature,armature_obj,head,tail,name,parent=None):
        armature_obj.select_set(True)
        bpy.context.view_layer.objects.active = armature_obj
        MekSkeletonFactory.switch_on_edit_mode()
        bones = armature.edit_bones
        bone = bones.new(name)
        bone.head = head
        bone.tail = tail
        if parent != None:
            parent_bone = armature.edit_bones[parent]
            bone.parent = parent_bone
            bone.use_connect = True
        MekSkeletonFactory.switch_on_object_mode()
        return bone
    
    @staticmethod
    def produce(name,root_data,bone_data):
        skel = Skeleton(name=name,**root_data)
        
        bone_data = copy.deepcopy(bone_data)
        while len(bone_data) > 0:
            for bone_name, bone_info in bone_data.items():
                bone = skel.add_bone(bone_name,**bone_info)
                if bone is not None:
                    break
            else:
                raise KeyError(f"Error: No bone named {bone_name}")
            
            del bone_data[bone_name]

        return skel
    
class AnimationFactory:
    ANIMATION_SUFFIX="_animation"
    
    @staticmethod
    def init_animation(skeleton,name=None):
        if name is None:
            name = skeleton.name + AnimationFactory.ANIMATION_SUFFIX
        skeleton.create_animation_data(name=name)
        return skeleton
    

            

if __name__ == "__main__":
    head1 = (0,0,4.5)
    tail1 = (0,0,4)
    armature, armature_obj, main_bone = MekSkeletonFactory.create_armature("my_armature","skull",head=head1,tail=tail1)
    #main_bone = MekSkeletonFactory.setup_bone(main_bone,head1,tail1)
    
    #head2 = (0,0,4)
    #tail2 = (0,0,3)
    #spine = MekSkeletonFactory.create_bone(armature,armature_obj,head2,tail2,"spine",parent=main_bone)
    bone_data = {"neck": {"head": [0.0, 0.0, 4], "tail": [0, 0, 3.75], "parent": "skull"}, 
                 "spine": {"head": [0.0, 0.0, 3.75], "tail": [0, 0, 2], "parent": "neck"}, 
                 "left_shoulder": {"head": [0.0, 0.0, 3.75], "tail": [0, -1.15, 3.75], "parent": "neck"},     
                 "left_upper_arm_bone": {"head":[0,-1.15,3.75],"tail":[0.1,-1.15,2.85],"parent":"left_shoulder"},
                 "left_lower_arm_bone": {"head":[0.1,-1.15,2.85],"tail":[1.1,-1.15,2.85],"parent":"left_upper_arm_bone"},
                 "left_hand_bone": {"head":[1.15,-1.15,2.85],"tail":[1.45,-1.15,2.85],"parent":"left_lower_arm_bone"},
                 "right_shoulder": {"head": [0.0, 0.0, 3.75], "tail": [0, 1.15, 3.75], "parent": "neck"},
                 "right_upper_arm_bone": {"head":[0,1.15,3.75],"tail":[0.1,1.15,2.85],"parent":"right_shoulder"},
                 "right_lower_arm_bone": {"head":[0.1,1.15,2.85],"tail":[1.1,1.15,2.85],"parent":"right_upper_arm_bone"},
                 "right_hand_bone": {"head":[1.15,1.15,2.85],"tail":[1.45,1.15,2.85],"parent":"right_lower_arm_bone"},
                 
                 "left_hip":  {"head": [0.0, 0.0, 2], "tail": [0,-0.75,1.9], "parent": "spine"}, 
                 "left_tigh":  {"head": [0,-0.75,1.9], "tail": [0,-0.75,0.95], "parent": "left_hip"}, 
                 "left_lower_leg_bone": {"head": [0,-0.75,0.95], "tail": [-0.25,-0.75,0.05], "parent": "left_tigh"}, 
                 "left_foot_bone": {"head": [-0.25,-0.75,0.05], "tail": [0.75,-0.75,0.05], "parent": "left_lower_leg_bone"},
                 
                 "right_hip":  {"head": [0.0, 0.0, 2], "tail": [0,0.75,1.9], "parent": "spine"},
                 "right_tigh":  {"head": [0,0.75,1.9], "tail": [0,0.75,0.95], "parent": "right_hip"}, 
                 "right_lower_leg_bone": {"head": [0,0.75,0.95], "tail": [-0.25,0.75,0.05], "parent": "right_tigh"}, 
                 "right_foot_bone": {"head": [-0.25,0.75,0.05], "tail": [0.75,0.75,0.05], "parent": "right_lower_leg_bone"},
                 }
    
    root_data = {"root": "skull", "armature_center": [0, 0, 0], "head": [0.0, 0.0, 4.5], "tail": [0, 0, 4]}
    root_name = "skull"
    skel =  MekSkeletonFactory.produce("boxi_skel",root_data,bone_data)
    bpy.ops.object.mode_set(mode="POSE",toggle=True)
    bone_name = "left_hand_bone"
    print(skel._bones)
    #breakpoint()
    #skel.armature_object.bones['left_hand_bone']
    skel = AnimationFactory.init_animation(skel)
    pbone = skel.select_bone("left_hand_bone")
    
    pbone.rotation_quaternion=(1,0,0,0)
    pbone.keyframe_insert(data_path='rotation_quaternion',frame=1)
    
    pbone.rotation_quaternion=(1,-1.5,-1.5,-1.5)
    pbone.keyframe_insert(data_path='rotation_quaternion',frame=20)
    
    pbone.rotation_quaternion=(1,0,0,0)
    pbone.keyframe_insert(data_path='rotation_quaternion',frame=40)
    
    
    
