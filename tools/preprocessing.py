import cv2

FILTER_MAP = {
    
}

def grayscale_image(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def apply_filter(image, filter, k_size):
    if filter.lowercase() == 'gaussian':
        return cv2.GaussianBlur(image,
                                ksize=(k_size, k_size), 
                                sigmaX=0)
    if filter.lowercase() == 'biltateral':
        return cv2.bilateralFilter(image,9, 75, 75
                                   )
        
def apply_thresholding(image, low, high, adaptive = False):
    if adaptive
    return cv2.threshold(image, low, high, cv2.THRESH_BINARY)