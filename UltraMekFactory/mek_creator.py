import os
import sys

wpath = os.path.split(__file__)[0]
sys.path.append(wpath)

import json
import create_mesh

class MekGeometry:
    FIX_KEY = "fixations"
    TYPE_KEY = "type"
    
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
    
    @classmethod
    def _get_key_dict(cls):
        dic = {}
        for key, val in cls.__dict__.items():
            if key.endswith("_KEY"):
                nkey = key.split("_")[0]
                dic[nkey] = val
        return dic    
    
    @staticmethod
    def _get_data_key(key,data):
        for dkey in data.keys():
            if dkey.lower() == key.lower():
                return dkey
            
        raise KeyError("Error: Key is missing in data!")
        
    def _set_data(self,data):
        for key, val in self._dic.items():
            dkey = self._get_data_key(val,data)
            setattr(self,key.lower(),data[dkey])
                
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
    RHA_KEY = "left_hand"
    
    LUL_KEY = "left_upper_leg"
    LKN_KEY = "left_knee"
    LLL_KEY = "left_lower_leg"
    LFO_KEY = "left_foot"
    
    RUL_KEY = "right_upper_leg"
    RKN_KEY = "right_knee"
    RLL_KEY = "right_lower_leg"
    RFO_KEY = "right_foot"
    
if __name__ == "__main__":
    sample_mek = BipedMekGeometry("/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekCreator/boxi.json")    
    

            
        