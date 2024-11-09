import os 
from PIL import Image
import numpy as np

snow_path = os.path.expanduser("~/Games/Godot/UltraMek/UltraMekGodot/assets/hexes/snow/")
road_path = os.path.expanduser("~/Games/Godot/UltraMek/UltraMekGodot/assets/hexes/road/")
forbidden = {"forest","lf","hf","wood","water"}

GIF = ".gif"
PNG = ".png"

def blend_images(fname1,fname2):
    img1 = Image.open(fname1).convert("RGBA")
    img2 = Image.open(fname2).convert("RGBA")
    
    img3 = _blend_images(img1,img2)
    
    return img3

def _blend_images(image1,image2,alpha=0.7):
    
    aim1 = np.array(image1)
    aim2 = np.array(image2)
    inds = aim2[:,:,3] > 0 
    aim1[inds] = aim2[inds]
    
    #image3 = Image.blend(image1,image2, alpha)
    image3 = Image.fromarray(aim1)
    
    return image3

def not_forbidden(fname,forbidden_keys=forbidden):
    check = [forb in fname for forb in forbidden_keys]
    if any(check):
        return False
    return True

def blend_folders(folder1,folder2,file_format=PNG,forbidden_keys=forbidden):
    files1 = os.listdir(folder1)
    files2 = os.listdir(folder2)
    out_folder = os.path.join(folder1,os.path.split(os.path.split(folder2)[0])[-1])
    os.makedirs(out_folder,exist_ok=True)
    
    for fname1 in files1:
        for fname2 in files2:
            if fname1.endswith(file_format) and fname2.endswith(file_format) and not_forbidden(fname1,forbidden_keys):
                end1 = fname1
                end2 = fname2
                new_fname = end2[:-len(file_format)] + '_' + end1
                f1 = os.path.join(folder1,fname1)
                f2 = os.path.join(folder2,fname2)
                try:
                    img = blend_images(f1,f2)
                    img.save(os.path.join(out_folder,new_fname))
                except IndexError:
                    pass
                except:
                    import pdb
                    pdb.set_trace()
                

if __name__ == "__main__":
    #im1 = os.path.join(snow_path,"snow_0.png")
    #im2 = os.path.join(road_path,"road09.png")
    #im3 = blend_images(im1,im2)
    #im3.show()
    blend_folders(snow_path,road_path)
    
