from xml.dom import INDEX_SIZE_ERR
import colorful as cf
from colour import Color



ci_colors = {   
    str(idx): c.get_hex_l() 
    for idx, c in enumerate(Color('red').range_to(Color('green'), 10))
}
print(ci_colors)

import tool_shack.scripting as tss

g = tss.ColorGradientSerializer(start_color_name='#ff5544', end_color_name='#44aa22')
print(g.palette)
g._print_gradient()

import random
import numpy as np 
for r in [random.random() * 0.1 + fix for fix in np.linspace(0, 0.9, 1000)]: 
    print(g(r), g.v_range)

