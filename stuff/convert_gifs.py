 
import os 
from PIL import Image 

path = os.path.expanduser("~/Games/Godot/UltraMek/UltraMekGodot/assets/hexes/snow/")
files = os.listdir(path)
format1 = ".gif"
format2 = ".png"

if __name__ == "__main__":
	for fn in files:
		if fn.endswith(format1):
			out_fn = fn[:-len(format1)] + format2
			image = Image.open(os.path.join(path,fn))
			image.save(os.path.join(path,out_fn))
			os.remove(os.path.join(path,fn))
