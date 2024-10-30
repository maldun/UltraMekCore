"""
data.py - Classes and Tools for data handling and processing

Copyright © 2024 Stefan H. Reiterer.
stefan.harald.reiterer@gmail.com 
This work is under GPL v2 as it should remain free but compatible with MegaMek
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import json
import os
import shutil
import pandas as pd
import sqlite3
import shlex
import unittest
from copy import deepcopy
from tempfile import mkdtemp
from zipfile import ZipFile

from .constants import CONFIG_FILE, U8
from .parsers import MulParser, BlkParser, MtfParser

class UnitHandler:
    MEKHQ_KEY = "mekhq_data"
    UNITS_PATH_KEY = "units"
    CUSTOM_PATH = "custom"
    GFX_PATH = "gfx"
    DBS_PATH = "dbs"
    MECH_PATH = "mechfiles"+os.sep
    IMAGE_PATH = "images"
    UNITS_PATH = "units"
    MISC_PATH = "misc"
    TYPE_KEY = "type"
    TYPE2CATEGORY_MAP = {"biped":"mechs",
                    "tracked": "vehicles"}
    
    CHASSIS_KEY = "chassis"
    MODEL_KEY = "model"
    
    BLK_SUFFIX = ".blk"
    MTF_SUFFIX = ".mtf"
    SQL_SUFFIX = ".sqlite"
    JSO_SUFFIX = ".json"
    ZIP_SUFFIX = ".zip"
    
    GFX_DATA_FILE="gfx" + JSO_SUFFIX
    ENTITY_GFX_FILE="{name}_gfx" + JSO_SUFFIX
    MECHSET_FILE = "mechset.txt"
    UNKOWN_UNIT_FILE = "radarBlip.png"
    MECHSET_KEYS = ("exact","chassis")
    
    ID_KEY = "IID"
    NAME_KEY = "NAME"
    DATA_KEY = "DATA"
    DATA_COLUMNS = [ID_KEY,NAME_KEY,DATA_KEY]
    TABLE_NAME = "entities"
    QUERY_CODE = "SELECT {} FROM {}"
    ENTITY_NOT_FOUND_MSG = "Error: Entity not found! Check if it is valid or custom unit file is missing!"
    DB_INTEGRITY_MSG = "Error: Entry exists several time! Check DB integrity"
    
    GFX_2D_IMAGE_KEY = "gfx_2d_image"
    
    NO_CLOSIN_MSG = "No closing quotation"
    """
    Class to manage unit data
    """
    def __init__(self):
        path = os.path.split(__file__)[0]
        config_file = os.path.join(path,CONFIG_FILE)
        self.dir2extract = mkdtemp()
        with open(config_file,'r') as fp:
            config = json.load(fp)
        self.mekhq_path = os.path.expanduser(config[self.MEKHQ_KEY])
        self.units_path = os.path.expanduser(config[self.UNITS_PATH_KEY])
        self.custom_path = os.path.join(self.units_path,self.CUSTOM_PATH)
        self.gfx_path = os.path.join(self.units_path,self.GFX_PATH)
        self.gfx_data_file = os.path.join(self.gfx_path,self.GFX_DATA_FILE)
        self.dbs_path = os.path.join(self.units_path,self.DBS_PATH)
        
        if not os.path.exists(self.gfx_data_file):
            with open(self.gfx_data_file,'w',encoding=U8) as gfp:
                json.dump({},gfp)
        

    def __del__(self):
        shutil.rmtree(self.dir2extract,ignore_errors = True)
        
    def parse_file(self,file_found):
        if file_found.lower().endswith(self.BLK_SUFFIX):
            parser = BlkParser()
        elif file_found.lower().endswith(self.MTF_SUFFIX):
            parser = MtfParser()
            
        result = parser(file_found)
        return result
        
    
    def get_entity_name(self,entity):
        """
        extracts the name from the entity
        """
        chassis = entity[self.CHASSIS_KEY]
        model = entity[self.MODEL_KEY]
        name = chassis + (' ' + model if model != '' else '')
        return name
    
    def get_entity_from_mekhq(self,entity):
        data_path = os.path.join(self.mekhq_path,self.MECH_PATH)
        entity_type = entity[self.TYPE_KEY]
        if entity_type.lower() in self.TYPE2CATEGORY_MAP.keys():
            category = self.TYPE2CATEGORY_MAP[entity_type.lower()]
            file_path = os.path.join(data_path,category+self.ZIP_SUFFIX)
        else:
            return None
        
        tmp_path = os.path.join(self.dir2extract,category)
        if not os.path.exists(tmp_path):
            shutil.unpack_archive(file_path,tmp_path)
        
        name = self.get_entity_name(entity)
        file_found = None
        for root, folder, files in os.walk(tmp_path):
            for filename in files:
                if name == os.path.splitext(filename)[0].strip():
                    file_found = os.path.join(root,filename)
                    break
            if file_found != None:
                break
        else:
            return None
        
        result = self.parse_file(file_found)
        return result
    
    def write_entity_onto_db(self,entity,category,entity_data):
        # category = self.get_category(entity)
        name = self.get_entity_name(entity)
        
        db_fname = os.path.join(self.dbs_path,category+self.SQL_SUFFIX)
        new_row = {}
        if not os.path.exists(db_fname):
            df = pd.DataFrame(columns=self.DATA_COLUMNS)
            nr = 0
        else:
            con = sqlite3.connect(db_fname)
            df = pd.read_sql(self.QUERY_CODE.format(", ".join(self.DATA_COLUMNS),self.TABLE_NAME),con,index_col=self.ID_KEY)
            nr = len(df)
        
        # check if entry exists
        if nr>0 and len(df.index[df[self.NAME_KEY]==name])>0:
            return df
        
        new_row[self.ID_KEY] = nr
        new_row[self.NAME_KEY] = name
        new_row[self.DATA_KEY] = json.dumps(entity_data)
        new_row = pd.DataFrame(new_row,index=[nr])
        new_row.set_index(self.ID_KEY)
        df = pd.concat([df,new_row])
        df.set_index(self.ID_KEY)
        con = sqlite3.connect(db_fname)
        
        df.to_sql(name=self.TABLE_NAME,con=con,if_exists='replace')
        return df
            
    def get_entity_from_db(self,entity,category):
        db_fname = os.path.join(self.dbs_path,category+self.SQL_SUFFIX)
        if not os.path.exists(db_fname):
            return None
        
        con = sqlite3.connect(db_fname)
        df = pd.read_sql(self.QUERY_CODE.format(", ".join(self.DATA_COLUMNS),self.TABLE_NAME),con,index_col=self.ID_KEY)
        name = self.get_entity_name(entity)
        if len(df.index[df[self.NAME_KEY]==name]) == 0:
            return None
        
        if len(df.index[df[self.NAME_KEY]==name]) > 1:
            raise ValueError(self.DB_INTEGRITY_MSG)
        
        if len(df.index[df[self.NAME_KEY]==name]) == 1:
            ind = int(df.index[df[self.NAME_KEY]==name][0])
            data = df.iloc[ind][self.DATA_KEY]
            data_dic = json.loads(data)
            return data_dic
            
    def get_category(self,entity):
        # get enity type:
        entity_type = entity[self.TYPE_KEY]
        if entity_type.lower() in self.TYPE2CATEGORY_MAP.keys():
            category = self.TYPE2CATEGORY_MAP[entity_type.lower()]
            return category
        else:
            return None
        
    def get_custom_entity(self,entity):
        name = self.get_entity_name(entity)
        for filename in os.listdir(self.custom_path):
            fn_parts = os.path.splitext(filename)
            if name == fn_parts[0].strip():
                file_found = filename
                break
        else:
            return None
        
        file_found = os.path.join(self.custom_path,file_found)
        found_entity = self.parse_file(file_found)
        return found_entity
    
    def get_entity(self,entity):
        # first try to find custom entity
        result = self.get_custom_entity(entity)
        if result is not None:
            return result
        
        category = self.get_category(entity)
        #next try to find entity from db
        result = self.get_entity_from_db(entity,category)
        if result is not None:
            return result
        
        # last but not least try getting it from MegaMek data ...
        result = self.get_entity_from_mekhq(entity)
        if result is None:
            raise ValueError(self.ENTITY_NOT_FOUND_MSG)
        # add to db for later use
        self.write_entity_onto_db(entity,category,result)
        
        return result
    
    def get_gfx(self,entity):
        name = self.get_entity_name(entity)
        category = self.get_category(entity)
        with open(self.gfx_data_file,'r',encoding=U8) as gfp:
            gfx_data = json.load(gfp)
        
        if name not in gfx_data.keys():
            gfx_data = self.create_new_gfx(entity,category,gfx_data)
        
        return gfx_data[name]
        
    def create_new_gfx(self,entity,category,gfx_data):
        name = self.get_entity_name(entity)
        entity_path = os.path.join(self.gfx_path,category,name)
        os.makedirs(entity_path,exist_ok=True)
        entity_gfx_file = os.path.join(entity_path,self.ENTITY_GFX_FILE.format(name=name))
        # entry does not exist but file exists
        if not os.path.exists(entity_gfx_file):
            new_gfx_file = {}
            image_path = os.path.join(self.mekhq_path,self.IMAGE_PATH)
            image_unit_path = os.path.join(image_path,self.UNITS_PATH)
            image_category_path = os.path.join(image_unit_path,category)
            chassis = entity[self.CHASSIS_KEY].split(" ")[0]
            model = entity[self.MODEL_KEY]
            mechset = self.parse_mechset(image_unit_path)
            if name in mechset.keys():
                image_file = os.path.join(image_unit_path,mechset[name])
            elif chassis in mechset.keys():
                image_file = os.path.join(image_unit_path,mechset[chassis])
            else:
                image_file = os.path.join(image_path,self.MISC_PATH,self.UNKOWN_UNIT_FILE)
            
            new_image_file = os.path.join(entity_path,os.path.split(image_file)[1])
            shutil.copy2(image_file,new_image_file)
            end_path = os.path.split(new_image_file)[0]
            end_path = os.path.split(end_path)
            end_path = os.path.split(end_path[0]) + (end_path[1],)
            new_image_file_relative = "/".join((self.UNITS_PATH,self.GFX_PATH)+end_path[1:]+(os.path.split(image_file)[1],))
            new_gfx_file[self.GFX_2D_IMAGE_KEY] = new_image_file_relative
            with open(entity_gfx_file,'w',encoding=U8) as fp:
                json.dump(new_gfx_file,fp)
            
        gfx_data[name] = entity_gfx_file
        return gfx_data
        
    def parse_mechset(self,mechset_path):
        # function is very simple no dedicated parser needed ...
        mechset_file = os.path.join(mechset_path,self.MECHSET_FILE)
        with open(mechset_file,'r',encoding=U8) as fp:
            lines = fp.readlines()
        
        lines = [line for line in lines if not line.startswith('#')]
        lines2 = []
        for line in lines:
           try: 
               split_line = shlex.split(line)
               lines2.append(split_line)
           except ValueError as excp:
               if str(excp) == self.NO_CLOSIN_MSG:
                 try:
                    split_line = shlex.split(line.strip() + '"')
                    lines2.append(split_line)
                 except:
                     pass 
           except: # politely ignore tuff that does not work ...
                pass
            
        lines = lines2
        lines = [line for line in lines if len(line)>=3]
        lines = [line[1:3] for line in lines if line[0] in self.MECHSET_KEYS]
        return dict(lines)
        
    
    def __call__(self,entity):
        return self.get_entity(entity)
        
        
    
class UnitHandlerTests(unittest.TestCase):
    
    def setUp(self):
        self.mulp = MulParser()
        self.uh = UnitHandler()
        self.path = os.path.join("test","samples")
        self.mul_files = ["example.mul","example2.mul"]
        self.mul_files = [os.path.join(self.path,f) for f in self.mul_files]
        self.entities = self.mulp(self.mul_files[1])[MulParser.ENTITY_PLURAL]
    def tearDown(self):
        db_fname = os.path.join(self.uh.dbs_path,"test"+UnitHandler.SQL_SUFFIX)
        if os.path.exists(db_fname):
            os.remove(db_fname)
        test_unit_path = "test/units"
        if os.path.exists(test_unit_path):
            shutil.rmtree(test_unit_path)
        del self.uh
        
        
    def test___init__(self):
        self.assertIn('UltraMek/data',self.uh.mekhq_path)
        
    def test_get_category(self):
       entity = self.entities["1"]
       result = self.uh.get_category(entity)
       self.assertEqual(result,'mechs')
       entity = self.entities["2"]
       result = self.uh.get_category(entity)
       self.assertEqual(result,'vehicles')
        
    def test_get_entity_from_mekhq(self):
       entity = self.entities["1"]
       result = self.uh.get_entity_from_mekhq(entity)
       self.assertEqual(result[self.uh.CHASSIS_KEY],'Atlas')
       self.assertEqual(result[self.uh.MODEL_KEY],'AS7-D')
       entity = self.entities["2"]
       result = self.uh.get_entity_from_mekhq(entity)
       self.assertEqual(result["name"],'Rommel Tank')
       
    def test_write_entity_onto_db(self):
        entity = self.entities["1"]
        category = "test" #self.uh.get_category(entity)
        #name = self.get_entity_name(entity)
        mek_data = self.uh.get_entity_from_mekhq(entity)
        df = self.uh.write_entity_onto_db(entity,category,mek_data)
        name=self.uh.get_entity_name(entity)
        self.assertEqual(df.iloc[0][self.uh.NAME_KEY],name)
        entity = self.entities["2"]
        category = "test"
        mek_data = self.uh.get_entity_from_mekhq(entity)
        df = self.uh.write_entity_onto_db(entity,category,mek_data)
        name=self.uh.get_entity_name(entity)
        self.assertEqual(df.iloc[1][self.uh.NAME_KEY],name)
        df2 = self.uh.write_entity_onto_db(entity,category,mek_data)
        self.assertEqual(len(df),len(df2))
    
    def test_get_entity_from_db(self):
        entity = self.entities["1"]
        category = "test" #self.uh.get_category(entity)
        #name = self.get_entity_name(entity)
        mek_data = self.uh.get_entity_from_mekhq(entity)
        df = self.uh.write_entity_onto_db(entity,category,mek_data)
        entity = self.entities["2"]
        mek_data = self.uh.get_entity_from_mekhq(entity)
        df = self.uh.write_entity_onto_db(entity,category,mek_data)
        result = self.uh.get_entity_from_db(entity,"test2")
        self.assertFalse(result)
        result = self.uh.get_entity_from_db(entity,category)
        self.assertEqual(entity["chassis"],result["name"])
    
    def test_get_custom_entity(self):
        entity = self.entities["1"]
        self.uh.custom_path = self.path
        result = self.uh.get_custom_entity(entity)
        self.assertEqual(result[self.uh.CHASSIS_KEY],'Atlas')
        self.assertEqual(result[self.uh.MODEL_KEY],'AS7-D')
        entity = self.entities["2"]
        result = self.uh.get_custom_entity(entity)
        self.assertEqual(result["name"],'Rommel Tank')
        
    def test_get_entity(self):
        entity = self.entities["1"]
        self.uh.custom_path = self.path
        result = self.uh.get_entity(entity)
        self.assertEqual(result[self.uh.CHASSIS_KEY],'Atlas')
        self.assertEqual(result[self.uh.MODEL_KEY],'AS7-D')
        category = "test" #self.uh.get_category(entity)
        #name = self.get_entity_name(entity)
        mek_data = self.uh.get_entity_from_mekhq(entity)
        df = self.uh.write_entity_onto_db(entity,category,mek_data)
        entity = self.entities["2"]
        mek_data = self.uh.get_entity_from_mekhq(entity)
        df = self.uh.write_entity_onto_db(entity,category,mek_data)
        
        entity = deepcopy(self.entities["2"])
        entity["model"] = "2"
        self.uh.TYPE2CATEGORY_MAP["test"] = "test"
        entity[self.uh.TYPE_KEY] = "test"
        df = self.uh.write_entity_onto_db(entity,category,mek_data)
        result = self.uh.get_entity(entity)
        self.assertEqual(result[self.uh.NAME_KEY.lower()],entity[self.uh.CHASSIS_KEY])
        
        entity = self.entities["2"]
        entity[self.uh.CHASSIS_KEY]="bla mek"
        with self.assertRaises(ValueError) as context:
            self.uh.get_entity(entity)
            self.assertEqual(str(context),self.uh.ENTITY_NOT_FOUND_MSG)
    
    def test_parse_mechset(self):
        image_path = os.path.join(self.uh.mekhq_path,self.uh.IMAGE_PATH)
        image_unit_path = os.path.join(image_path,self.uh.UNITS_PATH)
        result = self.uh.parse_mechset(image_unit_path)
        entity = self.entities["1"]
        chassis = entity[self.uh.CHASSIS_KEY]
        self.assertIn(chassis,result.keys())
        
    
    def test_get_gfx(self):
        #self.uh.units_path = "test/units"
        entity = self.entities["1"]
        result = self.uh.get_gfx(entity)
        name = self.uh.get_entity_name(entity)
        self.assertEqual(os.path.split(result)[1],self.uh.ENTITY_GFX_FILE.format(name=name))
        
