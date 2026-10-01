"""Create bundled, offline examples from scikit-image's included data."""
from pathlib import Path
import numpy as np
from PIL import Image
from skimage import data

destination=Path(__file__).resolve().parents[1]/"sample_images"
destination.mkdir(exist_ok=True)
y,x=np.indices((384,384))
patterns=.45+.15*np.sin(2*np.pi*x/32)+.12*np.sin(2*np.pi*y/12)
patterns[70:170,70:170]=.9
patterns[(x-260)**2+(y-255)**2<48**2]=.12
samples={"cameraman":data.camera(),"coffee":data.coffee(),"astronaut":data.astronaut(),"chelsea":data.chelsea(),"patterns":np.uint8(np.clip(patterns,0,1)*255)}
for name,array in samples.items():
    image=Image.fromarray(array)
    image.thumbnail((512,512),Image.Resampling.LANCZOS)
    image.save(destination/(name+".png"))
    print(name,image.size)
