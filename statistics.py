from dataprocessor.imageprocessor import ImageProcessor
from dataprocessor.maskoperator import MaskOperator
from indexes_test.calcuateindex import IndexCalculator
import rasterio
import os
import numpy as np

class Statistics:
    def __init__(self, raster_path: str, label_path: str) -> None:
        self.raster_path = raster_path
        self.label_path = label_path
    
    def __get_file_paths(self, path, filename):
        input_path = os.path.join(path, filename)
        label_path = input_path.replace("inputs", "labels")
        tiff_path = input_path.replace(".npy", ".tif").replace("inputs", "tiffs")
        return input_path, label_path, tiff_path
    
    def __get_soil_cloud_shadow_arrays(self):
        img = rasterio.open(self.raster_path)
        cloud = MaskOperator.select_mask(img, self.label_path, "cloud")
        shadow = MaskOperator.select_mask(img, self.label_path, "shadow")
        soil = MaskOperator.select_mask(img, self.label_path, "soil")
        
        mask_cloud = (cloud != 0) & (~np.isnan(cloud))
        mask_shadow = (shadow != 0) & (~np.isnan(shadow))
        mask_soil = (soil != 0) & (~np.isnan(soil))
        
        return [mask_soil], [mask_cloud], mask_shadow
    
    def calculate_mean(self, mask: str) -> np.array:
        img = rasterio.open(self.raster_path)
        label = np.open(self.label_path)
        img = MaskOperator.select_mask(img, label, mask)
        mean = np.nanmean(img)
        return mean
    
    def process_images(self, imgs_dir, mean = False):
        filenames = os.listdir(imgs_dir)
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
                array_array, label_array, array_img = Statistics.__get_file_paths(imgs_dir, filename)
                cloudsoilhist = CloudSoilHistogram(path_raster=array_img, path_array=array_array, path_label=label_array)
                indices = [
                    IndexCalculator.get_ndwi(),
                    IndexCalculator.get_ndre(),
                    IndexCalculator.get_grvi(),
                    IndexCalculator.get_rvi(),
                    IndexCalculator.get_ndvi(),
                    IndexCalculator.get_gndvi(),
                ]



            for index, key in zip(indices, soil_values.keys()):
                soil_data = MaskOperator.select_mask(array_img, label_array, "soil")
                cloud_data = MaskOperator.select_mask(array_img, label_array, "cloud")
                shadow_data = MaskOperator.select_mask(array_img, label_array, "shadow")
            
            
            if mean:
                for index, key in zip(indices, soil_values.keys()):
                    soil_data, cloud_data, shadow_data = soil_clouds_arrays(cloudsoilhist, index)
                    soil_values[key].append(np.nanmean(soil_data))
                    cloud_values[key].append(np.nanmean(cloud_data))
                    shadow_values[key].append(np.nanmean(shadow_data))

            else:
                for index, key in zip(indices, soil_values.keys()):
                    soil_data, cloud_data, shadow_data = soil_clouds_arrays(cloudsoilhist, index)
                    soil_values[key].append(soil_data)
                    cloud_values[key].append(cloud_data)
                    shadow_values[key].append(shadow_data)
                    
        return soil_values, cloud_values, shadow_values