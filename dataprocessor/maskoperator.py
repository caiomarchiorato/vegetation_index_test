import numpy as np

class MaskOperator:
    
    '''
    select_mask(img, label, mask) -> np.array:
        label (shape): (height, width, 3)
        [:,:,0] = apontando para o background
        [:,:,1] = apontando para as nuvens
        [:,:,2] = apontando para as sombras
        
        Parâmetros:
        - img (np.array): A imagem que será mascarada.
        - label (np.array): A matriz de rótulos associada à imagem.
        - mask (str): O tipo de máscara a ser aplicada (soil, cloud, shadow).

        Retorna:
        - np.array: A imagem resultante após a aplicação da máscara.

    remv_background(img, label) -> np.array:
        Remove o fundo da imagem com base nos rótulos fornecidos.

        Parâmetros:
        - img (np.array): A imagem da qual o fundo será removido.
        - label (np.array): A matriz de rótulos indicando a região do fundo.

        Retorna:
        - np.array: A imagem resultante após a remoção do fundo.
    '''
    
    @staticmethod
    def select_mask(img, label: np.array, mask: str) -> np.array:
        if mask == "soil":
            mask_label = (label[:,:,0] == 1)
        elif mask == "cloud":
            mask_label = (label[:,:,1] == 1)
        elif mask == "shadow":
            mask_label == (label[:,:,2] == 1)
        
        img = img.astype(float)
        img[mask_label] = np.nan
        
        return img
    
    @staticmethod
    def remv_background(img, label: np.array) -> np.array:
        mask_label = (label[:,:,0] == 1)
        img = img.astype(float)
        img[mask_label] = np.nan
        
        return img