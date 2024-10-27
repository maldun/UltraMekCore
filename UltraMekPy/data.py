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
import unittest
from tempfile import mkdtemp
from zipfile import ZipFile

from .constants import CONFIG_FILE
from .parsers import MulParser, BlkParser, MtfParser

class UnitHandler:
    MEKHQ_KEY = "mekhq_data"
    UNITS_PATH_KEY = "units"
    DBS_PATH = "dbs"
    MECH_PATH = "mechfiles"+os.sep
    TYPE_KEY = "type"
    TYPE2ZIP_MAP = {"biped":"mechs.zip",
                    "tracked": "vehicles.zip"}
    
    CHASSIS_KEY = "chassis"
    MODEL_KEY = "model"
    
    BLK_SUFFIX = ".blk"
    MTF_SUFFIX = ".mtf"
    SQL_SUFFIX = ".sqlite"
    
    ID_KEY = "IID"
    NAME_KEY = "NAME"
    DATA_KEY = "DATA"
    DATA_COLUMNS = [ID_KEY,NAME_KEY,DATA_KEY]
    TABLE_NAME = "entities"
    QUERY_CODE = "SELECT {} FROM {}"
    
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
        self.dbs_path = os.path.join(self.units_path,self.DBS_PATH)
        

    def __del__(self):
        shutil.rmtree(self.dir2extract,ignore_errors = True)
    
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
        if entity_type.lower() in self.TYPE2ZIP_MAP.keys():
            zip_file = self.TYPE2ZIP_MAP[entity_type.lower()]
            file_path = os.path.join(data_path,zip_file)
        else:
            return None
        
        tmp_path = os.path.join(self.dir2extract,os.path.splitext(zip_file)[0])
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
        
        if file_found.lower().endswith(self.BLK_SUFFIX):
            parser = BlkParser()
        elif file_found.lower().endswith(self.MTF_SUFFIX):
            parser = MtfParser()
            
        result = parser(file_found)
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
        
        new_row[self.ID_KEY] = nr
        new_row[self.NAME_KEY] = name
        new_row[self.DATA_KEY] = json.dumps(entity_data)
        new_row = pd.DataFrame(new_row,index=[nr])
        new_row.set_index(self.ID_KEY)
        breakpoint()
        df = pd.concat([df,new_row])
        df.set_index(self.ID_KEY)
        con = sqlite3.connect(db_fname)
        
        df.to_sql(name=self.TABLE_NAME,con=con,if_exists='replace')
        return df
            
    def get_entity_from_db(self,entity,category):
        if not os.path.exists(os.join.path(self.dbs_path,category,self.SQL_SUFFIX)):
            return False
    
    def get_category(self,entity):
        # get enity type:
        entity_type = entity[self.TYPE_KEY]
        if entity_type.lower() in self.TYPE2ZIP_MAP.keys():
            category = self.TYPE2ZIP_MAP[entity_type.lower()]
            category = os.path.splitext(category)[0]
            return category
        else:
            return None
        
    def get_entity(self,entity):
        pass
    
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
        entity = self.entities["2"]
        category = "test"
        mek_data = self.uh.get_entity_from_mekhq(entity)
        breakpoint()
        df2 = self.uh.write_entity_onto_db(entity,category,mek_data)
    
    
