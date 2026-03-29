"""
Image preprocessing to improve OCR and AI accuracy
Enhances image quality before analysis
"""
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from typing import Optional

def preprocess_for_ocr(image: Image.Image) -> Image.Image:
    """
    Preprocess image to improve OCR accuracy.
    - Increases contrast
    - Sharpens text
    - Converts to grayscale if needed
    """
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)  # Increase contrast by 50%
    
    # Sharpen image (helps with text recognition)
    image = image.filter(ImageFilter.SHARPEN)
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.3)
    
    return image


def preprocess_for_ai_vision(image: Image.Image) -> Image.Image:
    """
    Preprocess image for AI vision analysis.
    - Normalizes brightness
    - Enhances contrast
    """
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Enhance contrast slightly
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)
    
    # Normalize brightness
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.1)
    
    return image


def enhance_dimension_text(image: Image.Image) -> Image.Image:
    """
    Specifically enhance dimension text areas.
    Useful for drawings with small dimension labels.
    """
    # Convert to grayscale for better text detection
    gray = image.convert('L')
    
    # Increase contrast significantly for text
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(2.0)
    
    # Convert back to RGB
    return enhanced.convert('RGB')
