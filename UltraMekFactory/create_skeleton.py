import os
import bpy
import json
#import bmesh
import mathutils
import math
import numpy

class MekSkeletonFactory:
    """
    Class for creating a skeleton from data
    """
    EDIT_MODE = "EDIT"
    OBJECT_MODE = "OBJECT"
    ARMATURE_DEFAULT = "Armature"
    BONE_DEFAULT = "Bone"
    @staticmethod
    def create_armature(name,bone_name,head=(0,0,0),tail=(0,0,1)):
        MekSkeletonFactory.switch_on_object_mode()
        bpy.ops.object.armature_add(location=head)
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
            bone.parent = parent
        bone.use_connect = True
        MekSkeletonFactory.switch_on_object_mode()
        return bone

if __name__ == "__main__":
    head1 = (0,0,4.5)
    tail1 = (0,0,4)
    armature, armature_obj, main_bone = MekSkeletonFactory.create_armature("my_armature","head",head=head1,tail=tail1)
    #main_bone = MekSkeletonFactory.setup_bone(main_bone,head1,tail1)
    
    head2 = (0,0,4)
    tail2 = (0,0,3)
    bone1 = MekSkeletonFactory.create_bone(armature,armature_obj,head2,tail2,"center_torso",parent=main_bone)
    
    