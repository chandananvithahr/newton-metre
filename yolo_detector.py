"""
YOLO-based object detection for engineering drawings
Detects GD&T symbols, dimensions, features, and annotations
"""
from pathlib import Path
from typing import Dict, List, Optional
from PIL import Image
import numpy as np

# YOLO model configuration
YOLO_MODEL_PATH = Path(__file__).parent / "models" / "drawing_detector.pt"
YOLO_MODEL_URL = None  # Can be set to download pre-trained model

# Class names for engineering drawing elements
DRAWING_CLASSES = [
    'dimension_line',
    'dimension_text',
    'gd_t_symbol',
    'thread_symbol',
    'hole',
    'chamfer',
    'groove',
    'surface_finish',
    'tolerance',
    'material_callout',
    'title_block',
    'center_line',
    'hidden_line',
    'section_line'
]


def detect_drawing_elements(image: Image.Image, model_path: Optional[Path] = None) -> Dict:
    """
    Detect engineering drawing elements using YOLO.
    
    Args:
        image: PIL Image object
        model_path: Optional path to YOLO model file
        
    Returns:
        Dictionary with detected elements and their locations
    """
    try:
        from ultralytics import YOLO
        
        # Load model
        model_file = model_path or YOLO_MODEL_PATH
        
        # If custom model doesn't exist, use pre-trained YOLOv8
        if not model_file.exists():
            # Use YOLOv8 general purpose model as fallback
            model = YOLO('yolov8n.pt')  # nano model (fastest)
            # Note: For best results, train custom model on engineering drawings
        else:
            model = YOLO(str(model_file))
        
        # Convert PIL to numpy array
        img_array = np.array(image)
        
        # Run detection
        results = model(img_array, conf=0.25)  # 25% confidence threshold
        
        # Parse results
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].cpu().numpy()  # Bounding box coordinates
                
                # Get class name
                class_name = result.names[cls] if hasattr(result, 'names') else f"class_{cls}"
                
                detections.append({
                    'class': class_name,
                    'confidence': conf,
                    'bbox': {
                        'x1': float(xyxy[0]),
                        'y1': float(xyxy[1]),
                        'x2': float(xyxy[2]),
                        'y2': float(xyxy[3])
                    }
                })
        
        # Group detections by type
        grouped = _group_detections(detections)
        
        # Extract dimensions from detected dimension lines/text
        dimensions = _extract_dimensions_from_detections(detections, image.size)
        
        # Extract features
        features = _extract_features_from_detections(detections)
        
        return {
            'detections': detections,
            'grouped': grouped,
            'dimensions': dimensions,
            'features': features,
            'total_detections': len(detections),
            'confidence': 'medium',  # YOLO is good but may need custom training
            'source': 'yolo_detector'
        }
        
    except ImportError:
        return {"error": "YOLO (ultralytics) not installed. Install with: pip install ultralytics"}
    except Exception as e:
        return {"error": f"YOLO detection error: {str(e)}"}


def _group_detections(detections: List[Dict]) -> Dict:
    """Group detections by class type."""
    grouped = {}
    for det in detections:
        cls = det['class']
        if cls not in grouped:
            grouped[cls] = []
        grouped[cls].append(det)
    return grouped


def _extract_dimensions_from_detections(detections: List[Dict], image_size: tuple) -> Dict:
    """Extract dimension values from detected dimension elements."""
    dimensions = {}
    
    # Find dimension text detections
    dim_texts = [d for d in detections if 'dimension_text' in d['class'].lower()]
    
    # Try to extract numeric values from dimension text
    import re
    for det in dim_texts:
        # This would need OCR or text recognition on the detected region
        # For now, return structure
        pass
    
    # Estimate dimensions from bounding boxes of dimension lines
    dim_lines = [d for d in detections if 'dimension_line' in d['class'].lower()]
    
    if dim_lines:
        # Calculate approximate dimensions based on line lengths
        # This is a simplified approach - real implementation would need
        # scale calibration from drawing scale
        max_length = max([
            abs(d['bbox']['x2'] - d['bbox']['x1']) + abs(d['bbox']['y2'] - d['bbox']['y1'])
            for d in dim_lines
        ])
        
        # Estimate scale (this would need calibration)
        # For now, return detected structure
        dimensions['detected_dimension_lines'] = len(dim_lines)
    
    return dimensions


def _extract_features_from_detections(detections: List[Dict]) -> List[Dict]:
    """Extract features from detected elements."""
    features = []
    
    # Count holes
    holes = [d for d in detections if 'hole' in d['class'].lower()]
    if holes:
        features.append({
            'type': 'hole',
            'quantity': len(holes),
            'confidence': sum([d['confidence'] for d in holes]) / len(holes)
        })
    
    # Count threads
    threads = [d for d in detections if 'thread' in d['class'].lower()]
    if threads:
        features.append({
            'type': 'thread',
            'quantity': len(threads),
            'confidence': sum([d['confidence'] for d in threads]) / len(threads)
        })
    
    # Count chamfers
    chamfers = [d for d in detections if 'chamfer' in d['class'].lower()]
    if chamfers:
        features.append({
            'type': 'chamfer',
            'quantity': len(chamfers)
        })
    
    # Count grooves
    grooves = [d for d in detections if 'groove' in d['class'].lower()]
    if grooves:
        features.append({
            'type': 'groove',
            'quantity': len(grooves)
        })
    
    # GD&T symbols
    gd_t = [d for d in detections if 'gd_t' in d['class'].lower() or 'tolerance' in d['class'].lower()]
    if gd_t:
        features.append({
            'type': 'gd_t_symbol',
            'quantity': len(gd_t),
            'has_tight_tolerances': True
        })
    
    return features


def detect_gdt_symbols(image: Image.Image) -> Dict:
    """
    Specifically detect GD&T (Geometric Dimensioning & Tolerancing) symbols.
    
    Args:
        image: PIL Image object
        
    Returns:
        Dictionary with GD&T symbol detections
    """
    result = detect_drawing_elements(image)
    
    if "error" in result:
        return result
    
    gdt_detections = [
        d for d in result['detections']
        if 'gd_t' in d['class'].lower() or 'tolerance' in d['class'].lower()
    ]
    
    return {
        'gdt_symbols': gdt_detections,
        'count': len(gdt_detections),
        'has_tight_tolerances': len(gdt_detections) > 0,
        'confidence': 'medium'
    }


def create_annotated_image(image: Image.Image, detections: List[Dict]) -> Image.Image:
    """
    Create annotated image with bounding boxes around detected elements.
    
    Args:
        image: Original PIL Image
        detections: List of detection dictionaries
        
    Returns:
        Annotated PIL Image
    """
    from PIL import ImageDraw, ImageFont
    
    annotated = image.copy()
    draw = ImageDraw.Draw(annotated)
    
    # Try to load font
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
    
    for det in detections:
        bbox = det['bbox']
        cls = det['class']
        conf = det['confidence']
        
        # Draw bounding box
        draw.rectangle(
            [(bbox['x1'], bbox['y1']), (bbox['x2'], bbox['y2'])],
            outline='red',
            width=2
        )
        
        # Draw label
        label = f"{cls} {conf:.2f}"
        draw.text(
            (bbox['x1'], bbox['y1'] - 15),
            label,
            fill='red',
            font=font
        )
    
    return annotated
