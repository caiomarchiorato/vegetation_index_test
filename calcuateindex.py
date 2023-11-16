import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#modulos otimizados
from dataprocessor.imageprocessor import ImageProcessor

'''
get_ndvi(img) -> np.array:
    Calcula o índice NDVI para a imagem fornecida.

    Parâmetros:
    - img (np.array): A imagem para a qual o índice será calculado.

    Retorna:
    - np.array: A imagem resultante após o cálculo do índice.
    
    .... Demais índices
'''

class IndexCalculator:
        @staticmethod
        def get_ndvi(img) -> np.array:
            nir = ImageProcessor.get_band(img, 'nir')
            nir = np.where(nir == 0, np.nan, nir)
            red = ImageProcessor.get_band(img, 'red')
            red = np.where(red == 0, np.nan, red)
            ndvi = (nir - red) / (nir + red)
            return ndvi
        
        @staticmethod
        def get_ndwi(img) -> np.array:
            green = ImageProcessor.get_band(img, 'green')
            green = np.where(green == 0, np.nan, green)
            nir = ImageProcessor.get_band(img, 'nir')
            nir = np.where(nir == 0, np.nan, nir)
            ndwi = (green - nir) / (green + nir)
            return ndwi
        
        @staticmethod
        def get_ndre(img) -> np.array:
            nir = ImageProcessor.get_band(img, 'nir')
            nir = np.where(nir == 0, np.nan, nir)
            rededge = ImageProcessor.get_band(img, 'rededge')
            rededge = np.where(rededge == 0, np.nan, rededge)
            ndre = (nir - rededge) / (nir + rededge)
            return ndre
        
        @staticmethod
        def get_grvi(img) -> np.array:
            nir = ImageProcessor.get_band(img, 'nir')
            nir = np.where(nir == 0, np.nan, nir)
            green = ImageProcessor.get_band(img, 'green')
            green = np.where(green == 0, np.nan, green)
            grvi = (nir / green)
            return grvi
        
        @staticmethod
        def get_gndvi(img) -> np.array:
            nir = ImageProcessor.get_band(img, 'nir')
            nir = np.where(nir == 0, np.nan, nir)
            green = ImageProcessor.get_band(img, 'green')
            green = np.where(green == 0, np.nan, green)
            gndvi = (nir - green) / (nir + green)
            return gndvi
        
        @staticmethod
        def get_rvi(img) -> np.array:
            red = ImageProcessor.get_band(img, 'red')
            red = np.where(red == 0, np.nan, red)
            nir = ImageProcessor.get_band(img, 'nir')
            nir = np.where(nir == 0, np.nan, nir)
            rvi = (nir / red)
            return rvi