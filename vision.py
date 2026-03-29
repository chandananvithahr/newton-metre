"""
Vision API for drawing analysis - supports both OpenAI and Gemini
"""
import json
import os
import base64
from pathlib import Path
from typing import Dict, Union, Optional, List
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Check for API keys
openai_api_key = os.getenv('OPENAI_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')

# Configure APIs
use_openai = bool(openai_api_key)
use_gemini = bool(gemini_api_key)

if use_openai:
    try:
        import openai
        openai.api_key = openai_api_key
    except ImportError:
        use_openai = False
        print("Warning: OpenAI package not installed. Install with: pip install openai")

if use_gemini:
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_api_key)
    except ImportError:
        use_gemini = False
        print("Warning: google-generativeai package not installed. Install with: pip install google-generativeai")

PROMPT = """
You are an expert mechanical engineer analyzing an engineering drawing. Extract information with EXTREME PRECISION.

CRITICAL INSTRUCTIONS:
1. Read dimension text EXACTLY as written - do NOT estimate or guess
2. Look for dimension callouts, leaders, and dimension lines
3. Check title blocks, notes, and annotations for dimensions
4. If dimensions are unclear, set confidence to "low"
5. DO NOT make up dimensions - only extract what you can clearly see

EXTRACTION REQUIREMENTS:

1. PART TYPE: 
   - "turning" if cylindrical/rotational (has diameter)
   - "milling" if rectangular/block (length x width x height)
   - Look for lathe operations, turning symbols, or cylindrical features

2. DIMENSIONS (READ EXACTLY FROM TEXT):
   - Find dimension text labels (e.g., "Ø50", "50mm", "L=100", "DIA 25")
   - For TURNING parts:
     * max_diameter_mm: Largest outer diameter (look for "OD", "DIA", "Ø" symbols)
     * inner_diameter_mm: Inner diameter if hollow (look for "ID", "BORE")
     * length_mm: Total length along axis (look for "L", "LENGTH")
   - For MILLING parts:
     * length_mm: Longest dimension
     * width_mm: Second dimension
     * height_mm: Third dimension/thickness
   - IMPORTANT: Extract numbers EXACTLY as written, don't estimate from visual scale

3. MATERIAL:
   - Look in title block, material callout box, or notes section
   - Common formats: "MATERIAL: Mild Steel", "MAT: SS304", etc.

4. FEATURES:
   - Holes: Look for hole callouts (e.g., "4x Ø5", "HOLE DIA 8")
   - Threads: Look for thread callouts (e.g., "M10x1.5", "1/2-13 UNC")
   - Grooves: Look for groove dimensions
   - Chamfers: Look for chamfer callouts (e.g., "C2", "45°x1mm")

5. SURFACE FINISH:
   - Look for Ra values (e.g., "Ra 1.6", "Ra 3.2")
   - Look for finish symbols

6. TOLERANCES:
   - Look for tolerance callouts (e.g., "±0.05", "H7", "IT6")
   - has_tight_tolerances: true if tolerance < ±0.05mm

ACCURACY RULES:
- If you cannot clearly read a dimension, set it to null
- If dimension text is blurry/unclear, set confidence to "low"
- DO NOT guess dimensions based on visual appearance
- Only extract dimensions from actual text/labels on the drawing

Return ONLY valid JSON (no markdown, no explanations):
{
    "part_type": "turning" or "milling",
    "material_on_drawing": "string or null",
    "dimensions": {
        "max_diameter_mm": number or null,
        "inner_diameter_mm": number or null,
        "length_mm": number or null,
        "width_mm": number or null,
        "height_mm": number or null
    },
    "features": [
        {"type": "thread", "specification": "M10x1.5"},
        {"type": "hole", "diameter_mm": 5, "quantity": 4}
    ],
    "surface_finish_ra": number or null,
    "has_tight_tolerances": boolean,
    "confidence": "high", "medium", or "low"
}
"""


def analyze_drawing(image_input: Union[str, Path, Image.Image]) -> Dict:
    """
    Analyze a single engineering drawing image.
    For multiple pages, use analyze_multiple_drawings().
    """
    return _analyze_single_drawing(image_input)


def analyze_multiple_drawings(images: List[Image.Image], combine_results: bool = True, use_yolo: bool = True) -> Dict:
    """
    Analyze multiple drawing pages/images and combine results.
    
    Args:
        images: List of PIL Image objects (multiple pages/views)
        combine_results: If True, merge results from all pages. If False, return list of results.
        use_yolo: If True, use YOLO for feature detection before AI analysis
        
    Returns:
        Combined dictionary with merged dimensions, features, etc., or list of results
    """
    if not images:
        return {"error": "No images provided"}
    
    results = []
    for i, image in enumerate(images):
        # Try YOLO detection first if enabled
        yolo_features = []
        if use_yolo:
            try:
                from yolo_detector import detect_drawing_elements
                yolo_result = detect_drawing_elements(image)
                if "error" not in yolo_result:
                    yolo_features = yolo_result.get('features', [])
            except:
                pass  # YOLO not available, continue with AI
        
        # Run AI analysis
        result = _analyze_single_drawing(image)
        if "error" not in result:
            result['page_number'] = i + 1
            
            # Merge YOLO features with AI features
            if yolo_features:
                existing_features = result.get('features', [])
                # Combine unique features
                combined_features = existing_features.copy()
                for yolo_feat in yolo_features:
                    # Check if similar feature already exists
                    if not any(
                        f.get('type') == yolo_feat.get('type') 
                        for f in combined_features
                    ):
                        combined_features.append(yolo_feat)
                result['features'] = combined_features
                result['yolo_detections'] = len(yolo_features)
            
            results.append(result)
    
    if not results:
        return {"error": "Failed to analyze any pages"}
    
    if combine_results:
        return _combine_analysis_results(results)
    else:
        return {"pages": results, "total_pages": len(results)}


def _combine_analysis_results(results: List[Dict]) -> Dict:
    """
    Combine analysis results from multiple pages.
    Merges dimensions (takes max), combines features, etc.
    """
    if not results:
        return {"error": "No results to combine"}
    
    if len(results) == 1:
        return results[0]
    
    # Start with first result
    combined = results[0].copy()
    
    # Merge dimensions - take maximum values
    combined_dims = combined.get('dimensions', {}).copy()
    for result in results[1:]:
        dims = result.get('dimensions', {})
        for key in ['max_diameter_mm', 'inner_diameter_mm', 'length_mm', 'width_mm', 'height_mm']:
            if dims.get(key):
                current = combined_dims.get(key, 0) or 0
                new_val = dims.get(key, 0) or 0
                combined_dims[key] = max(current, new_val)
    
    combined['dimensions'] = combined_dims
    
    # Combine features - merge unique features
    all_features = []
    seen_features = set()
    for result in results:
        features = result.get('features', [])
        for feat in features:
            # Create a unique key for the feature
            feat_key = (feat.get('type', ''), feat.get('specification', ''), feat.get('diameter_mm'))
            if feat_key not in seen_features:
                all_features.append(feat)
                seen_features.add(feat_key)
    
    combined['features'] = all_features
    
    # Material - use first non-null value
    for result in results:
        material = result.get('material_on_drawing')
        if material:
            combined['material_on_drawing'] = material
            break
    
    # Surface finish - use first non-null value
    for result in results:
        surface_finish = result.get('surface_finish_ra')
        if surface_finish:
            combined['surface_finish_ra'] = surface_finish
            break
    
    # Tight tolerances - true if any page has it
    combined['has_tight_tolerances'] = any(r.get('has_tight_tolerances', False) for r in results)
    
    # Confidence - use lowest (most conservative)
    confidences = [r.get('confidence', 'low') for r in results]
    confidence_order = {'high': 3, 'medium': 2, 'low': 1}
    combined['confidence'] = min(confidences, key=lambda x: confidence_order.get(x, 0))
    
    # Part type - use most common
    part_types = [r.get('part_type', 'unknown') for r in results]
    combined['part_type'] = max(set(part_types), key=part_types.count)
    
    combined['pages_analyzed'] = len(results)
    combined['analysis_combined'] = True
    
    return combined


def _analyze_single_drawing(image_input: Union[str, Path, Image.Image], use_ocr_fallback: bool = True) -> Dict:
    """
    Analyze an engineering drawing using OpenAI GPT-4 Vision or Gemini 2.0 Flash.
    Tries OpenAI first if available, falls back to Gemini.
    
    Args:
        image_input: Path to image file (PNG, JPG) or PIL Image object
        
    Returns:
        Dictionary containing extracted drawing information, or error dict with 'error' key
        
    Example:
        result = analyze_drawing("drawing.png")
        result = analyze_drawing(Image.open("drawing.jpg"))
    """
    try:
        # Check if any API key is configured
        if not use_openai and not use_gemini:
            return {
                "error": "No API key found. Please set OPENAI_API_KEY or GOOGLE_API_KEY in .env file"
            }
        
        # Load image
        if isinstance(image_input, (str, Path)):
            image_path = Path(image_input)
            if not image_path.exists():
                return {"error": f"Image file not found: {image_path}"}
            
            # Validate file extension
            if image_path.suffix.lower() not in ['.png', '.jpg', '.jpeg']:
                return {"error": f"Unsupported image format: {image_path.suffix}. Use PNG or JPG."}
            
            image = Image.open(image_path)
        elif isinstance(image_input, Image.Image):
            image = image_input
        else:
            return {"error": "Invalid image input. Provide a file path (str/Path) or PIL Image object."}
        
        # Try OpenAI first if available, then fallback to Gemini
        response_text = None
        
        if use_openai:
            try:
                response_text = analyze_with_openai(image)
            except Exception as e:
                print(f"OpenAI API error: {e}")
                if not use_gemini:
                    return {"error": f"OpenAI API error: {str(e)}"}
        
        # Fallback to Gemini if OpenAI failed or not available
        if not response_text and use_gemini:
            try:
                # Initialize Gemini model
                model = genai.GenerativeModel('gemini-2.0-flash')
                
                # Send image and prompt to Gemini
                response = model.generate_content([PROMPT, image])
                
                # Extract text response
                if hasattr(response, 'text') and response.text:
                    response_text = response.text.strip()
                else:
                    return {"error": "No response text from Gemini API. The model may have failed to generate content."}
            except Exception as e:
                return {"error": f"Gemini API error: {str(e)}"}
        
        if not response_text:
            # Fallback to OCR if AI fails and OCR is enabled
            if use_ocr_fallback and isinstance(image_input, Image.Image):
                try:
                    from ocr_extractor import extract_text_with_paddleocr
                    ocr_result = extract_text_with_paddleocr(image_input)
                    if "error" not in ocr_result:
                        # Convert OCR result to analysis format
                        return {
                            'part_type': 'turning',  # Default assumption
                            'dimensions': ocr_result.get('dimensions', {}),
                            'material_on_drawing': ocr_result.get('material_on_drawing'),
                            'features': [],
                            'surface_finish_ra': None,
                            'has_tight_tolerances': False,
                            'confidence': 'medium',
                            'source': 'ocr_fallback'
                        }
                except ImportError:
                    pass
                except Exception:
                    pass
            
            return {"error": "No API keys configured. Please set OPENAI_API_KEY or GOOGLE_API_KEY in .env file"}
        
        # Try to extract JSON from response (handle markdown code blocks if present)
        if "```json" in response_text:
            # Extract JSON from markdown code block
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            # Extract JSON from generic code block
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        
        # Parse JSON response
        try:
            result = json.loads(response_text)
            
            # Validate required fields
            if "part_type" not in result:
                return {"error": "Invalid response: missing 'part_type' field"}
            
            return result
            
        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse JSON response: {str(e)}",
                "raw_response": response_text[:500]  # Include first 500 chars for debugging
            }
    
    except Exception as e:
        return {
            "error": f"Error analyzing drawing: {str(e)}"
        }


def analyze_with_openai(image: Image.Image) -> Optional[str]:
    """
    Analyze image using OpenAI GPT-4 Vision API.
    
    Args:
        image: PIL Image object
        
    Returns:
        Response text from OpenAI
    """
    import openai
    
    # Convert PIL image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    # Call OpenAI Vision API
    client = openai.OpenAI(api_key=openai_api_key)
    
    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4-vision-preview" for older models
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": PROMPT
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000
    )
    
    return response.choices[0].message.content.strip()
