import rasterio
import numpy as np

class ImageProcessor:
    '''
    get_band(img, band: str) -> np.array:
        Parâmetros:
        - img (obj): A imagem da qual a banda será extraída.
        - band (str): O nome da banda a ser extraída.

        Retorna:
        - np.array: A banda extraída.

    normalize(arr) -> np.array:
        Parâmetros:
        - arr (np.array): A matriz a ser normalizada.

        Retorna:
        - np.array: A matriz normalizada.

    get_cloud(img) -> np.array:
        Parâmetros:
        - img (obj): A imagem da qual a banda de nuvens será extraída.

        Retorna:
        - np.array: A banda de nuvens.

    prepare_image(img) -> np.array:
        Parâmetros:
        - img (obj): A imagem da qual as bandas serão extraídas
        
        Retorna:
        - np.array: A imagem preparada no formato RGB.

    prepare_image_to_rgb(img) -> np.array:
        Parâmetros:
        - img (obj): A imagem da qual as bandas serão extraídas.

        Retorna:
        - np.array: A imagem preparada no formato RGB com valores normalizados para o intervalo [0, 255].
    '''
    
    
    @staticmethod
    def get_band(img, band: str) -> np.array:
        bands = {band: num for num, band in enumerate(img.descriptions, start = 1)}
        if band in bands.keys():
            band = img.read(bands.get(band))
            return band
    
    @staticmethod
    def normalize(arr):
        array_min, array_max = arr.min(), arr.max()
        normalized_array = (arr - array_min) / (array_max - array_min)
        return normalized_array
    
    @staticmethod
    def get_cloud(img):
        bands = {band:num for num, band in enumerate(img.descriptions, start=1)}
        clouds = img.read(bands.get('clouds'))
        return clouds
    
    @staticmethod
    def prepare_image(img):
        bands = {band:num for num, band in enumerate(img.descriptions, start=1)}
        
        red = img.read(bands.get('red'))
        green = img.read(bands.get('green'))
        blue = img.read(bands.get('blue'))
        
        redn = ImageProcessor.normalize(red)
        greenn = ImageProcessor.normalize(green)
        bluen = ImageProcessor.normalize(blue)
        
        rgb = np.dstack((redn, greenn, bluen))
        return rgb
    
    @staticmethod
    def prepare_image_to_rgb(img):
        bands = {band:num for num, band in enumerate(img.descriptions, start=1)}
        
        red = img.read(bands.get('red'))
        green = img.read(bands.get('green'))
        blue = img.read(bands.get('blue'))
        
        redn = ImageProcessor.normalize(red)
        greenn = ImageProcessor.normalize(green)
        bluen = ImageProcessor.normalize(blue)
        
        redn = (redn * 255)
        greenn = (greenn * 255)
        bluen = (bluen * 255)
        
        rgb = np.dstack((redn, greenn, bluen))
        return rgb