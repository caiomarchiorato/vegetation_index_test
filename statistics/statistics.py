from dataprocessor.imageprocessor import ImageProcessor
from dataprocessor.maskoperator import MaskOperator
from dataprocessor.calcuateindex import IndexCalculator
import rasterio
import os
import numpy as np

"""
    Extrai máscaras de solo, nuvem e sombra do arquivo de label e as retorna como arrays.

    Args:
    - index: Índice para seleção da máscara desejada.

    Returns:
    - Array contendo a máscara de solo.
    - Array contendo a máscara de nuvem.
    - Array contendo a máscara de sombra.
        """

class LoadData:
    def __init__(self, raster_path: str, label_path: str) -> None:
        self.raster_path = raster_path
        self.label_path = label_path
    
    def get_soil_cloud_shadow_arrays(self, index):
        label = np.load(self.label_path)
        
        cloud = MaskOperator.select_mask(index, label, "cloud")
        shadow = MaskOperator.select_mask(index, label, "shadow")
        soil = MaskOperator.select_mask(index, label, "soil")
        
        mask_cloud = (cloud != 0) & (~np.isnan(cloud))
        mask_shadow = (shadow != 0) & (~np.isnan(shadow))
        mask_soil = (soil != 0) & (~np.isnan(soil))
        
        return soil[mask_soil], cloud[mask_cloud], shadow[mask_shadow]

"""
    Extrai máscaras de solo, nuvem e sombra do arquivo de label e as retorna como arrays.

    Args:
    - index: Índice para seleção da máscara desejada.

    Returns:
    - Array contendo a máscara de solo.
    - Array contendo a máscara de nuvem.
    - Array contendo a máscara de sombra.
"""

class DictionaryCreator:
    def __init__(self, raster_path) -> None:
        self.raster_path = raster_path 
        
    def get_file_paths(self, imgs_dir, filename):
        input_path = os.path.join(imgs_dir, filename)
        label_path = input_path.replace("inputs", "labels")
        tiff_path = input_path.replace(".npy", ".tif").replace("inputs", "tiffs")
        return input_path, label_path, tiff_path
    
    def calculate_mean(self, mask: str) -> np.array:
        img = np.load(self.raster_path)
        label = np.load(self.label_path)
        img = MaskOperator.select_mask(img, label, mask)
        mean = np.nanmean(img)
        return mean
    
    def get_index_dict(self, img_dir, mean = False, concatenate = False):
        filenames = os.listdir(img_dir)
        soil_values = {
            'ndwi': [], 'ndre': [], 'grvi': [], 'rvi': [], 'ndvi': [], 'gndvi': [],
        }
        cloud_values = {
            'ndwi': [], 'ndre': [], 'grvi': [], 'rvi': [], 'ndvi': [], 'gndvi': [],
        }
        shadow_values = {
            'ndwi': [], 'ndre': [], 'grvi': [], 'rvi': [], 'ndvi': [], 'gndvi': [],
        }

        for filename in filenames:
            if filename != ".DS_Store":
                input_path, label_path, tiff_path = self.get_file_paths(img_dir, filename= filename)
                load_data = LoadData(input_path, label_path)
                array_img = rasterio.open(tiff_path)
                
                indices = [
                    IndexCalculator.get_ndwi(array_img),
                    IndexCalculator.get_ndre(array_img),
                    IndexCalculator.get_grvi(array_img),
                    IndexCalculator.get_rvi(array_img),
                    IndexCalculator.get_ndvi(array_img),
                    IndexCalculator.get_gndvi(array_img),
                ]

            for index, key in zip(indices, soil_values.keys()):
                if mean:
                    soil_data, cloud_data, shadow_data = load_data.get_soil_cloud_shadow_arrays(index)                 
                    soil_values[key].append(np.nanmean(soil_data))
                    cloud_values[key].append(np.nanmean(cloud_data))
                    shadow_values[key].append(np.nanmean(shadow_data))
                    
                else:
                    soil_data, cloud_data, shadow_data = load_data.get_soil_cloud_shadow_arrays(index)                 
                    soil_values[key].append(soil_data)
                    cloud_values[key].append(cloud_data)
                    shadow_values[key].append(shadow_data)
                    
            if concatenate:
                soil_combined = {}
                cloud_combined = {}
                shadow_combined = {}
                
                for key, value_list in soil_values.items():
                    combined_array = np.concatenate(value_list, axis=None)
                    soil_combined[key] = combined_array
                    
                for key, value_list in cloud_values.items():
                    combined_array = np.concatenate(value_list, axis=None)
                    cloud_combined[key] = combined_array
                    
                for key, value_list in shadow_values.items():
                    combined_array = np.concatenate(value_list, axis=None)
                    shadow_combined[key] = combined_array
                
                return soil_combined, cloud_combined, shadow_combined
            
            else:
                return soil_values, cloud_values, shadow_values
            

class Statistics:
    def calc_test_z(soil: np.array, cloud: np.array) -> float: 
        m_soil = np.mean(soil)
        m_clouds = np.mean(cloud)
        
        n_soil = len(soil)
        n_clouds = len(cloud)
        
        std_soil = np.std(soil)
        std_clouds = np.std(cloud)
        
        z = abs( (m_soil - m_clouds) / np.sqrt( (std_soil**2 / n_soil) + (std_clouds**2 / n_clouds) ) )
        return z

    def calc_index_z(img_path: str):
        dictionary_creator = DictionaryCreator(img_path)
        soil_combined, cloud_combined, shadow_combined = dictionary_creator.get_index_dict(img_dir = img_path, concatenate = True)
        
        z_soil_x_clouds = {}
        z_soil_x_shadows = {}
        z_shadow_x_clouds = {}

        for key in soil_combined.keys():
            soil = soil_combined[key]
            cloud = cloud_combined[key]
            
            z = Statistics.calc_test_z(soil, cloud)
            z_soil_x_clouds[key] = z
            
        for key in soil_combined.keys():
            soil = soil_combined[key]
            shadow = shadow_combined[key]
            
            z = Statistics.calc_test_z(soil, shadow)
            z_soil_x_shadows[key] = z
            
        for key in soil_combined.keys():
            shadow = shadow_combined[key]
            cloud = cloud_combined[key]
            
            z = Statistics.calc_test_z(shadow, cloud)
            z_shadow_x_clouds[key] = z
        
        return z_soil_x_clouds, z_soil_x_shadows, z_shadow_x_clouds