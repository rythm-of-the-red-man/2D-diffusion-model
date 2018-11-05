import imageio
from diffusion_model import grid
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
gr=grid(200,200)
gr.initiate_atoms_in_line(quantitiy=5000)


images=[]
for i in range(800):
    gr.simulate_move()
    images.append(np.uint8(cm.jet(gr.grid)*255))
imageio.mimsave('diffusion.gif', images,duration=0.1)