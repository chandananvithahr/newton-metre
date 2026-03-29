"""
OCR-based text and dimension extraction using PaddleOCR
Free, local, unlimited processing alternative to AI vision
"""
from pathlib import Path
from typing import Dict, List, Optional
from PIL import Image
import re

def extract_text_with_paddleocr(image: Image.Image) -> Dict:
    """
    Extract text from image using PaddleOCR.
    Preprocesses image first for better accuracy.
    
    Args:
        image: PIL Image object
        
    Returns:
        Dictionary with extracted text and dimensions
    """
    try:
        from paddleocr import PaddleOCR
        from image_preprocessor import preprocess_for_ocr
        
        # Preprocess image for better OCR accuracy
        processed_image = preprocess_for_ocr(image)
        
        # Initialize OCR (use English + numbers by default)
        ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
        
        # Convert PIL image to numpy array
        import numpy as np
        img_array = np.array(processed_image)
        
        # Run OCR
        result = ocr.ocr(img_array, cls=True)
        
        # Extract all text
        all_text = []
        text_boxes = []
        
        if result and result[0]:
            for line in result[0]:
                if line:
                    text_info = line[1]
                    text = text_info[0]
                    confidence = text_info[1]
                    bbox = line[0]
                    
                    all_text.append(text)
                    text_boxes.append({
                        'text': text,
                        'confidence': confidence,
                        'bbox': bbox
                    })
        
        # Extract dimensions from text
        dimensions = _extract_dimensions_from_text(all_text)
        
        # Extract material from text
        material = _extract_material_from_text(all_text)
        
        return {
            'text_extracted': all_text,
            'text_boxes': text_boxes,
            'dimensions': dimensions,
            'material_on_drawing': material,
            'confidence': 'medium',  # OCR is less reliable than CAD parsing
            'source': 'paddleocr'
        }
        
    except ImportError:
        return {"error": "PaddleOCR not installed. Install with: pip install paddlepaddle paddleocr"}
    except Exception as e:
        return {"error": f"OCR extraction error: {str(e)}"}


def _extract_dimensions_from_text(text_list: List[str]) -> Dict:
    """Extract dimension values from OCR text with improved patterns."""
    dimensions = {}
    
    full_text = ' '.join(text_list).upper()
    
    # More comprehensive dimension patterns
    patterns = {
        # Diameter patterns (most common in turning parts)
        'diameter': [
            r'[Ø⌀]\s*(\d+\.?\d*)',  # Ø50
            r'DIA\s*[:=]?\s*(\d+\.?\d*)',  # DIA: 50
            r'OD\s*[:=]?\s*(\d+\.?\d*)',  # OD: 50
            r'OUTER\s*DIA\s*[:=]?\s*(\d+\.?\d*)',  # OUTER DIA: 50
            r'(\d+\.?\d*)\s*MM\s*DIA',  # 50 MM DIA
        ],
        # Inner diameter patterns
        'inner_diameter': [
            r'ID\s*[:=]?\s*(\d+\.?\d*)',  # ID: 30
            r'BORE\s*[:=]?\s*(\d+\.?\d*)',  # BORE: 30
            r'INNER\s*DIA\s*[:=]?\s*(\d+\.?\d*)',  # INNER DIA: 30
        ],
        # Length patterns
        'length': [
            r'L\s*[:=]?\s*(\d+\.?\d*)',  # L: 100
            r'LENGTH\s*[:=]?\s*(\d+\.?\d*)',  # LENGTH: 100
            r'LEN\s*[:=]?\s*(\d+\.?\d*)',  # LEN: 100
        ],
        # Width patterns (for milling)
        'width': [
            r'W\s*[:=]?\s*(\d+\.?\d*)',  # W: 50
            r'WIDTH\s*[:=]?\s*(\d+\.?\d*)',  # WIDTH: 50
        ],
        # Height patterns (for milling)
        'height': [
            r'H\s*[:=]?\s*(\d+\.?\d*)',  # H: 25
            r'HEIGHT\s*[:=]?\s*(\d+\.?\d*)',  # HEIGHT: 25
            r'THICK\s*[:=]?\s*(\d+\.?\d*)',  # THICK: 25
        ],
        # Combined patterns (e.g., "Ø50 x 100")
        'combined': [
            r'[Ø⌀]?\s*(\d+\.?\d*)\s*[xX×]\s*(\d+\.?\d*)',  # Ø50 x 100
            r'(\d+\.?\d*)\s*[xX×]\s*(\d+\.?\d*)\s*[xX×]?\s*(\d+\.?\d*)?',  # 50 x 100 x 25
        ]
    }
    
    # Try combined patterns first (most reliable)
    for pattern in patterns['combined']:
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            groups = match.groups()
            if len(groups) >= 2:
                # First number is usually diameter for turning, length for milling
                dim1 = float(groups[0])
                dim2 = float(groups[1])
                
                # Check if it's a turning part (has diameter symbol)
                if 'Ø' in match.group(0) or 'DIA' in full_text[:match.start()]:
                    dimensions['max_diameter_mm'] = dim1
                    dimensions['length_mm'] = dim2
                else:
                    dimensions['length_mm'] = dim1
                    dimensions['width_mm'] = dim2
                
                if len(groups) >= 3 and groups[2]:
                    dimensions['height_mm'] = float(groups[2])
                break
    
    # Try individual patterns if combined didn't work
    if not dimensions:
        # Diameter
        for pattern in patterns['diameter']:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                dimensions['max_diameter_mm'] = float(match.group(1))
                break
        
        # Inner diameter
        for pattern in patterns['inner_diameter']:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                dimensions['inner_diameter_mm'] = float(match.group(1))
                break
        
        # Length
        for pattern in patterns['length']:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                dimensions['length_mm'] = float(match.group(1))
                break
        
        # Width
        for pattern in patterns['width']:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                dimensions['width_mm'] = float(match.group(1))
                break
        
        # Height
        for pattern in patterns['height']:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                dimensions['height_mm'] = float(match.group(1))
                break
    
    # Also look for standalone numbers with "mm" that might be dimensions
    # This is a fallback if no labels found
    if not dimensions:
        mm_pattern = r'(\d+\.?\d*)\s*MM'
        matches = re.findall(mm_pattern, full_text, re.IGNORECASE)
        if matches:
            numbers = [float(m) for m in matches]
            if len(numbers) >= 2:
                # Assume first is diameter/length, second is length/width
                dimensions['max_diameter_mm'] = numbers[0]
                dimensions['length_mm'] = numbers[1]
            elif len(numbers) == 1:
                dimensions['length_mm'] = numbers[0]
    
    return dimensions


def _extract_material_from_text(text_list: List[str]) -> Optional[str]:
    """Extract material specification from text."""
    material_keywords = [
        'ALUMINUM', 'ALUMINIUM', 'AL', 'STEEL', 'STAINLESS', 'SS', 'BRASS',
        'BRONZE', 'COPPER', 'TITANIUM', 'EN8', 'EN24', 'IS2062', 'IS319',
        '6061', '304', '316'
    ]
    
    full_text = ' '.join(text_list).upper()
    
    for keyword in material_keywords:
        if keyword in full_text:
            # Try to extract full material name
            idx = full_text.find(keyword)
            # Extract surrounding text
            start = max(0, idx - 20)
            end = min(len(full_text), idx + 30)
            material_text = full_text[start:end].strip()
            return material_text
    
    return None
