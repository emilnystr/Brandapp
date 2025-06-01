import numpy as np
from B_Input import*
import json



with open('config.json', 'r') as config_file:
    config = json.load(config_file)

elementtjocklek_mm = config["mm_per_layer"]

def skapa_element(materialdata):
    dx_target = elementtjocklek_mm / 1000
    element_sizes = []
    element_material_indices = []

    for längd, material in materialdata:
        tjocklek_mm = längd * 1000
        if tjocklek_mm % elementtjocklek_mm == 0:
            antal_element = int(tjocklek_mm // elementtjocklek_mm)
            element_sizes.extend([dx_target] * antal_element)
        else:
            antal_element = int(tjocklek_mm // elementtjocklek_mm) + 1
            justerad_dx = längd / antal_element
            element_sizes.extend([justerad_dx] * antal_element)
        element_material_indices.extend([material] * antal_element)

    element_sizes = np.array(element_sizes, dtype=np.float32)
    element_material_indices = np.array(element_material_indices, dtype=np.int32)
    antal_element = len(element_sizes)
    antal_noder = antal_element + 1

    return element_sizes, element_material_indices, antal_noder

if __name__ == '__main__':
    materialdata = skapa_indata()
    test2 = skapa_element(materialdata)
    print(test2)
