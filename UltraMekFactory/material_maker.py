"""
Class and tools for creating material
"""
import bpy
import sys


class MekMaterialFactory:
    """
    Creates material from a dictionary of data, which in return
    can be retrieved from JSONS
    """
    NAME_MAT = "name"
    PBSDF_KEYW = "Principled BSDF"
    PBSDF_PROPERTY_MAP = {
    "Base Color":0,
    "Metallic":1,
    "Roughness":2,
    "IOR":3,
    "Alpha":4,
    "Normal":5,
    "Weight":6,
    "Diffuse Roughness":7,
    "Subsurface Weight":8,
    "Subsurface Radius":9,
    "Subsurface Scale":10,
    "Subsurface IOR":11,
    "Subsurface Anisotropy":12,
    "Specular IOR Level":13,
    "Specular Tint":14,
    "Anisotropic":15,
    "Anisotropic Rotation":16,
    "Tangent":17,
    "Transmission Weight":18,
    "Coat Weight":19,
    "Coat Roughness":20,
    "Coat IOR":21,
    "Coat Tint":22,
    "Coat Normal":23,
    "Sheen Weight":24,
    "Sheen Roughness":25,
    "Sheen Tint":26,
    "Emission Color":27,
    "Emission Strength":28,
    "Thin Film Thickness":29,
    "Thin Film IOR":30
    }
    
    
    @staticmethod
    def create_material(material_data):
        """
        Creates material from data.
        """
        name = material_data[MekMaterialFactory.NAME_MAT]
        
        mat = bpy.data.materials.new(name)
        bsdf = MekMaterialFactory.create_principled_bsdf_obj(mat)
        bsdf = MekMaterialFactory.apply_data(bsdf,material_data)

        #bpy.context.object.data.materials.append(mat)
        return mat
        


    @staticmethod        
    def create_principled_bsdf_obj(mat):
        """
        Creates a principled bsdf object.
        pbdsf is the only format Godot can 100% 
        support
        """
        mat.use_nodes = True
        mat_nodes = mat.node_tree.nodes
        bsdf = mat_nodes[MekMaterialFactory.PBSDF_KEYW]
        return bsdf

        
    @staticmethod
    def apply_data(bsdf,material_data):
        """
        Apply data to principled bsdf
        """
        m = MekMaterialFactory.PBSDF_PROPERTY_MAP # make short hand for map
        for key, i in m.items():
            # we allow some variants in the definition
            key_snake = key.replace(" ","_")
            key_usnake = key_snake.upper()
            key_lsnake = key_snake.lower()
            value = None
            if key in material_data.keys():
                value = material_data[key]
            elif key_snake in material_data.keys():
                value = material_data[key_snake]
            elif key_usnake in material_data.keys():
                value = material_data[key_usnake]
            elif key_lsnake in material_data.keys():
                value = material_data[key_lsnake]

            if value is not None:
                bsdf.inputs[i].default_value = value
                
            return bsdf
            
            
        
                
        
if __name__ == "__main__":
    scene = bpy.context.scene
    bpy.data.scenes.new("Scene")
    bpy.data.scenes.remove(scene, do_unlink=True)
    bpy.data.scenes[0].name = "Scene"
    
    wpath = "/home/maldun/Games/Godot/UltraMek/UltraMekCore/UltraMekFactory/"
    sys.path.append(wpath)
    from create_mesh import MekMeshFactory
    bm_box = MekMeshFactory.create_box(center=(0,0,0),dims=(1,2,3))
    box_msh = MekMeshFactory.bmesh2mesh(bm_box)
    box_obj = MekMeshFactory.mesh2blender(bm_box,"Box",mesh=box_msh)  
    mat_data = {MekMaterialFactory.NAME_MAT: "mat1",
                "base_color": (1,0,0,1)}    
    
    mat = MekMaterialFactory.create_material(mat_data)
    box_msh.materials.append(mat)
    
      
    bm_box.free() 