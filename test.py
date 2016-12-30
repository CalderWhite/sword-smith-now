import pygame, base64, codecs
from PIL import Image, ImageFilter

pygame.init()
def blur_surf(surf):
    # create the original pygame surface
    #surf = pygame.image.fromstring(, size, mode)
    size = surf.get_size()
    raw = pygame.image.tostring(surf,"RGBA",False)
    # create a PIL image and blur it
    pil_blured = Image.frombytes("RGBA", size, raw).filter(ImageFilter.GaussianBlur(radius=6))

    # convert it back to a pygame surface
    filtered = pygame.image.fromstring(pil_blured.tobytes("raw", image_mode), size, image_mode)
    return filtered