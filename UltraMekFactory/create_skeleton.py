import os
import bpy
import json
#import bmesh
import mathutils
import math
import numpy
import copy
import time

class Skeleton:
    EULER_MODE = "XYZ"
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
        self._bones.update({bone_name})
        return bone
    
    def get_armature(self):
        return self.armature_object
    
    def create_animation_data(self,name="BoneAnimation"):
        self.armature_object.animation_data_create()
        self.armature_object.animation_data.action = bpy.data.actions.new(name=name)
        
    def select_bone(self,bone_name,rotation_mode=EULER_MODE):
        bone = self.armature.bones[bone_name]
        bpy.context.object.data.bones.active = bone
        bone.select = True
        
        pbone = self.armature_object.pose.bones[bone_name]
        pbone.rotation_mode = rotation_mode
        #bpy.context.active_pose_bone = pbone
        return pbone
    
    def push_action(self,name,start=None,loop=True,):
        """
        Pushes an action to an NLA strip
        """
        obj = self.armature_object
        action = obj.animation_data.action
        if action is not None:
            if start is None:
                start = int(action.frame_range[0])
            if loop is True:
                name += Animation.LOOP_SUFFIX

            action = obj.animation_data.action
            track = obj.animation_data.nla_tracks.new()
            track.name = name
            track.strips.new(action.name, start , action)
            obj.animation_data.action = None
         

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
            #bone.use_connect = True
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
            setattr(skel,bone_name,bone_data)
            del bone_data[bone_name]

        return skel

class Animation:
    ANIMATION_SUFFIX="_animation"
    ROTATION_EULER_OP = "rotation_euler"
    LOCATION_OP = "location"
    OPS = {ROTATION_EULER_OP,LOCATION_OP}
    START_CUT="start"
    END_CUT="end"
    INIT_FRAME=1
    LOOP_SUFFIX = "-loop"
    def __init__(self,animation_data):
        if isinstance(animation_data,str):
            with open(animation_data,'r') as fp:
                animation_data = json.load(fp)
                
        self.animation_data = animation_data
        
    @staticmethod
    def init_animation(skeleton,name=None,loop=True):
        if name is None:
            name = skeleton.name + Animation.ANIMATION_SUFFIX
        if loop is True:
            name+=Animation.LOOP_SUFFIX
        skeleton.create_animation_data(name=name)
        return skeleton
    
    @staticmethod
    def convert_op(op,data):
        if op == Animation.ROTATION_EULER_OP:
            data = tuple(math.radians(x) for x in data)
        return op, data
    
    def apply_animation(self,skeleton,name=None,loop=True):
        self.init_animation(skeleton,name=name,loop=loop)
        if str(Animation.INIT_FRAME) not in self.animation_data.keys():
            self._init_anim(skeleton)

        obj = skeleton.get_armature()            
        action = obj.animation_data.action
        action.use_frame_range=True
        for frame, frame_data in self.animation_data.items():
            if frame==Animation.START_CUT:
                #bpy.context.scene.frame_start = int(frame_data)
                action.frame_start=int(frame_data)
            elif frame==Animation.END_CUT:
                #bpy.context.scene.frame_end = int(frame_data)
                action.frame_end = int(frame_data)
            else:
                self.create_keyframe(skeleton,frame,frame_data)
    
    @staticmethod
    def _init_anim(skeleton):
        for bone in skeleton._bones:
            pbone = skeleton.select_bone(bone)
            for op in Animation.OPS:
                setattr(pbone,op,(0,0,0))
                pbone.keyframe_insert(data_path=op,frame=Animation.INIT_FRAME)
    
    @staticmethod
    def create_keyframe(skeleton,frame,keyframe_data):
        try:
            frame = int(frame)
        except:
            raise KeyError(f"Error {frame} not a valid integer!")    
        for bone, anim_data in keyframe_data.items():
            pbone = skeleton.select_bone(bone)
            for op, data in anim_data.items():
                if op not in Animation.OPS:
                    raise ValueError(f"Error Operation {op} not allowed! Check Metadata!")
                op, data = Animation.convert_op(op,data)
                setattr(pbone,op,data)
                pbone.keyframe_insert(data_path=op,frame=frame)
            
            
            

if __name__ == "__main__":
    
    scene = bpy.context.scene
    bpy.data.scenes.new("Scene")
    bpy.data.scenes.remove(scene, do_unlink=True)
    bpy.data.scenes[0].name = "Scene"
    
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
    #skel = Animation.init_animation(skel)
    pbone = skel.select_bone("left_hand_bone")
    
    #pbone.location=(0,0,0)
    #pbone.keyframe_insert(data_path='location',frame=1)
    #pbone.rotation_euler=(0,0,0)
    #pbone.keyframe_insert(data_path='rotation_euler',frame=1)
    
    rotq = (1,-1.5/2,-1.5/2,-1.5/2)
    #rot = mathutils.Euler(rotq[1:])
    #pbone.rotation_quaternion=(1,-1.5,-1.5,-1.5)
    
    #mloc, mrot, msca = pbone.matrix.decompose()
    #mat = mathutils.Matrix.LocRotScale(mloc, rot, (1,1,1)) # @ pbone.matrix
    #pbone.matrix=mat
    #pbone.location=(0,0,0)
    #pbone.keyframe_insert(data_path='location',frame=20)
    #pbone.rotation_quaternion = rotq
    #pbone.keyframe_insert(data_path='rotation_quaternion',frame=20)
    #pbone.rotation_mode = 'XYZ'
    #pbone.rotation_euler = rot
    #pbone.keyframe_insert(data_path='rotation_euler',frame=20)
    
    #pbone.rotation_quaternion=(1,0,0,0)
    #pbone.keyframe_insert(data_path='rotation_quaternion',frame=40)
    #pbone.rotation_euler=(0,0,0)
    #pbone.keyframe_insert(data_path='rotation_euler',frame=40)

    walk_anim = Animation("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/walk_animation.json")
    walk_anim.apply_animation(skel,name='walk',loop=True)
    skel.push_action(name='walk',start=1)
    
    run_anim = Animation("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/run_animation.json")
    run_anim.apply_animation(skel,name='run',loop=True)
    skel.push_action(name='run',start=1)
    
    
