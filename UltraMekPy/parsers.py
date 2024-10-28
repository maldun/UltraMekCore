"""
parsers.py - Classes and Tools for parsing of mul, mtf and other MegaMek files files (compatible with MegaMek)

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

import abc
import os
import re
import unittest
import xml.etree.ElementTree as ET

from . import functions as fn

from .constants import U8

class Parser(abc.ABC):
    @abc.abstractmethod
    def parse_string(self,text):
        raise NotImplementedError("Error: Not Implemented!")
    def parse(self,filename):
        with open(filename,'r',encoding=U8) as fp:
            text = fp.read()
        return self.parse_string(text)
    def __call__(self,filename):
        return self.parse(filename)

class MtfParser(Parser):
    KEYS = {
        'armor',
        'capabilities',
        'center torso',
        'chassis',
        'config',
        'ct armor',
        'deployment',
        'engine',
        'era',
        'hd armor',
        'head',
        'heat sinks',
        'history',
        'jump mp',
        'la armor',
        'left arm',
        'left leg',
        'left torso',
        'll armor',
        'lt armor',
        'manufacturer',
        'mass',
        'model',
        'mul id',
        'myomer',
        'overview',
        'primaryfactory',
        'quirk',
        'ra armor',
        'right arm',
        'right leg',
        'right torso',
        'rl armor',
        'role',
        'rt armor',
        'rtc armor',
        'rtl armor',
        'rtr armor',
        'rules level',
        'source',
        'structure',
        'systemmanufacturer',
        'techbase',
        'walk mp',
        'weapons'
        }

    def lines2dict(self,lines):
        result = {key:[] for key in self.KEYS}
        record = False
        for line in lines:
            if ":" in line:
                breakdown = line.split(":")
                key = breakdown[0]
                if key.lower() in self.KEYS:
                   result[key.lower()] += [":".join([string.strip() for string in breakdown[1:] if string.strip() != ""])]
                   record = True
            elif record is True and line.strip() != "":
                result[key.lower()] += [line.strip()]
            elif line.strip() == "":
                record=False
                
        #"flatten" dict
        for key,val in result.items():
            if len(val) == 0:
                result[key] = ""
            elif len(val) == 1:
                new_val = val[0]
                if isinstance(new_val,str) and new_val.isdigit():
                    new_val = int(new_val)
                result[key] = new_val
            else:
                result[key] = [item for item in val if item != '']
                
        result = {fn.replace_whitespace(key,'_'):val for key,val in result.items()}
        # add unit type since mtf files are for meks only
        result['unit_type'] = 'Mek'
        return result
                
    def parse_string(self,text):
        lines = text.splitlines()
        result = self.lines2dict(lines)
        return result
        
    def parse(self,filename):
        with open(filename,'r',encoding=U8) as fp:
            lines = fp.readlines()
        result = self.lines2dict(lines)
        return result

class BlkParser(Parser):
    DATA_KEYWORD = "ultramekdata"
    EXCLUDE = {
               "block_version",
               "version",
               }
    
    @staticmethod
    def _remove_whitespace(text,regex):
        comp1 = re.compile(regex)
        finds1 = comp1.finditer(text)
        corr = 0
        for find in finds1:
            start,end = find.span()
            old = text[start-corr:end-corr]
            new = [substring.lower() for substring in fn.split_camel_case(old)]
            new = " ".join(new)
            new = re.sub(r"\s+", "_",new , flags=re.UNICODE)
            new = new.replace(":","").replace("+","").replace("*","")
            
            text = text[:start-corr] + new + text[end-corr:]
            
            corr += len(old)-len(new)
            
        return text
    
    def blk2xml(self,text):
        lines = text.splitlines()
        # remove comments
        new_lines = ['<?xml version="1.0"?>',f"<{self.DATA_KEYWORD}>"]
        for line in lines:
            ind = line.find('#')
            ind = None if ind == -1 else ind
            new_lines.append(line[:ind])
        
        new_lines.append(f"</{self.DATA_KEYWORD}>")
        xml_text = "\n".join(new_lines)
        
        reg1 = r'<[\w\s:+*.]+>'
        xml_text = self._remove_whitespace(xml_text,reg1)
        
        reg2 = r'</[\w\s:+*.]+>'
        xml_text = self._remove_whitespace(xml_text,reg2)
        
        return xml_text
                
    def xml2dict(self,root):
        result = {}
        for child in root:
            key = child.tag
            
            if key not in self.EXCLUDE:
                val = child.text.strip()
                    
                if '\n' in val:
                    val = val.splitlines()
                if isinstance(val,str) and val.isdigit():
                    val = int(val)
                elif '.' in val and val.replace('.','').isnumeric():
                    val = fn.string2float(val)
                if isinstance(val,list):
                    for k,it in enumerate(val):
                        new_it = it
                        if new_it.isdigit():
                            new_it = int(new_it)
                        elif '.' in new_it and new_it.replace('.','').isnumeric():
                            new_it = fn.string2.float(new_it)
                        else:
                            continue
                        val[k] = new_it
                        
                result[key] = val
        
        return result
        
    
    def parse_string(self,text):
        xml_text = self.blk2xml(text)
        root = ET.fromstring(xml_text)
        result = self.xml2dict(root)
        return result
    

class MulParser(Parser):
    
    ENTITY_KEY = "entity"
    ENTITY_PLURAL = "entities"
    PILOT_KEY = "pilot"
    LOCATION_KEY = "location"
    SLOT_KEY = "slot"
    INDEX_KEY = "index"
    SHOTS_KEY = "shots"
    GAME_KEY = "game"
    ID_KEY = "id"
    
    def xml2dict(self,root):
        result = root.attrib
        entities = {}
        for child in root:
            if child.tag.lower() == self.ENTITY_KEY:
                game_id, entity = self.collect_entity(child)
                entities[game_id] = entity
        result[self.ENTITY_PLURAL] = entities
        return result

    def collect_entity(self,ent_root):
        result = ent_root.attrib
        locations = {}
        for child in ent_root:
            if child.tag.lower() == self.PILOT_KEY:
                result[self.PILOT_KEY] = child.attrib
            if child.tag.lower() == self.LOCATION_KEY:
                ind = int(child.attrib[self.INDEX_KEY])
                locations[ind] = child.attrib
                locations[ind][self.LOCATION_KEY] = child.text.strip()
                slots = {}
                for grand_child in child:
                    gind = int(grand_child.attrib[self.INDEX_KEY]) 
                    slots[gind]=grand_child.attrib
                    slots[gind][self.SHOTS_KEY] = int(slots[gind][self.SHOTS_KEY])
                locations[ind][self.SLOT_KEY+'s'] = slots
                result[self.LOCATION_KEY+'s'] = locations
            if child.tag.lower() == self.GAME_KEY:
                game_id = child.attrib[self.ID_KEY]
                
        return game_id, result
    
    def parse_string(self,text):
        root = ET.fromstring(text)
        result = self.xml2dict(root)
        return result
                

###################################
# Tests                           #
###################################
    
class MtfTests(unittest.TestCase):
    
    def setUp(self):
        self.mtfp = MtfParser()
        self.path = os.path.join("test","samples")
        self.mtf_files = ["Atlas AS7-D.mtf",]
        self.mtf_files = [os.path.join(self.path,f) for f in self.mtf_files]
        
    def test_parse(self):
        result = self.mtfp(self.mtf_files[0])
        self.assertEqual(result['mass'],100)
    
    def test_lines2dict(self):
        with open(self.mtf_files[0],'r') as fp:
            lines = fp.readlines()
            
        result = self.mtfp.lines2dict(lines)
        unit_type_found = False
        for key,val in result.items():
            if key != 'unit_type':
                self.assertIn(key.replace('_',' '),MtfParser.KEYS)
            else:
                unit_type_found = True
                self.assertEqual(val,"Mek")
            
            if isinstance(val,list):
                self.assertGreater(len(val),1)
            if isinstance(val,str):
                self.assertFalse(val.isdigit())
                self.assertGreater(len(val),0)
        self.assertTrue(unit_type_found)
                
class BlkTests(unittest.TestCase):
    
    def setUp(self):
        self.blkp = BlkParser()
        self.path = os.path.join("test","samples")
        self.blk_files = ["Rommel Tank.blk","Rommel Tank G.blk",]
        self.blk_files = [os.path.join(self.path,f) for f in self.blk_files]

    def test__remove_whitespace(self):
        text = """
        <mul id:>
         2737
        </mul id:>
        
        <primaryFactory>
        Hesperus II,Salem,Alpheratz
        </primaryFactory>
        """
        expected = """
        <mul_id>
         2737
        </mul id:>
        
        <primary_factory>
        Hesperus II,Salem,Alpheratz
        </primaryFactory>
        """
        reg1 = r'<[\w\s:+\-*.]+>'
        result = BlkParser._remove_whitespace(text,reg1)
        self.assertEqual(result,expected)

    def test_blk2xml(self):
        with open(self.blk_files[0],'r') as fp:
            text = fp.read()
            
        xml_text = self.blkp.blk2xml(text)
        root = ET.fromstring(xml_text)

    def test_xml2dict(self):
        with open(self.blk_files[0],'r') as fp:
            text = fp.read()
        xml_text = self.blkp.blk2xml(text)
        root = ET.fromstring(xml_text)
        result = self.blkp.xml2dict(root)
        self.assertEqual(result['armor'],[38, 38, 38, 24, 38])
        self.assertEqual(result['tonnage'],65)
        self.assertEqual(result['body_equipment'][1],'IS Ammo AC/20')
        
        
    def test_parse(self):
        result = self.blkp(self.blk_files[1])
        self.assertEqual(result['tonnage'],65)
        
class MulParserTests(unittest.TestCase):
    
    def setUp(self):
        self.mulp = MulParser()
        self.path = os.path.join("test","samples")
        self.mul_files = ["example.mul","example2.mul"]
        self.mul_files = [os.path.join(self.path,f) for f in self.mul_files]
        
    def test_collect_entity(self):
        with open(self.mul_files[0],'r',encoding=U8) as fp:
            text = fp.read()
        root = ET.fromstring(text)
        for child in root:
            if child.tag == MulParser.ENTITY_KEY:
                gid, result = self.mulp.collect_entity(child)
                
        self.assertEqual(gid,"1")
        self.assertEqual(result['chassis'],"Atlas")
        self.assertEqual(result['commander'],'false')
        self.assertEqual(result['locations'][2]['location'],"Right Torso")
        self.assertEqual(result['locations'][2]['slots'][11]['type'],"IS Ammo AC/20")
        self.assertEqual(result['locations'][2]['slots'][11]['shots'],5)
        
    def test_xml2dict(self):
        with open(self.mul_files[1],'r',encoding=U8) as fp:
            text = fp.read()
        
        root = ET.fromstring(text)
        result = self.mulp.xml2dict(root)
        self.assertEqual(len(result["entities"]),2)
        self.assertEqual(result['entities']["2"]["chassis"],"Rommel Tank")
        
    def test_parse(self):
        result = self.mulp(self.mul_files[1])
        self.assertEqual(len(result["entities"]),2)
        
