"""
Dimension validation and correction utilities
Validates extracted dimensions and corrects common errors
"""
from typing import Dict, Optional, Tuple

def validate_dimensions(dimensions: Dict) -> Tuple[Dict, Dict]:
    """
    Validate and correct extracted dimensions.
    
    Returns:
        (validated_dimensions, validation_notes)
    """
    validated = {}
    notes = {}
    
    # Check for common errors
    max_dia = dimensions.get('max_diameter_mm')
    inner_dia = dimensions.get('inner_diameter_mm')
    length = dimensions.get('length_mm')
    width = dimensions.get('width_mm')
    height = dimensions.get('height_mm')
    
    # Rule 1: Inner diameter must be less than outer diameter
    if max_dia and inner_dia:
        if inner_dia >= max_dia:
            notes['inner_diameter'] = f"Warning: Inner diameter ({inner_dia}mm) >= Outer diameter ({max_dia}mm). Setting inner_diameter to null."
            validated['max_diameter_mm'] = max_dia
            validated['inner_diameter_mm'] = None
        else:
            validated['max_diameter_mm'] = max_dia
            validated['inner_diameter_mm'] = inner_dia
    elif max_dia:
        validated['max_diameter_mm'] = max_dia
    
    # Rule 2: Length should be reasonable (not too small or too large)
    if length:
        if length < 0.1:
            notes['length'] = f"Warning: Length ({length}mm) seems too small. May be in wrong units."
        elif length > 10000:
            notes['length'] = f"Warning: Length ({length}mm) seems too large. May be in wrong units."
        else:
            validated['length_mm'] = length
    
    # Rule 3: For milling parts, width and height should be reasonable
    if width:
        if 0.1 <= width <= 10000:
            validated['width_mm'] = width
        else:
            notes['width'] = f"Warning: Width ({width}mm) seems unreasonable."
    
    if height:
        if 0.1 <= height <= 10000:
            validated['height_mm'] = height
        else:
            notes['height'] = f"Warning: Height ({height}mm) seems unreasonable."
    
    # Rule 4: Check for swapped dimensions (common AI error)
    # If length is smaller than width, they might be swapped
    if length and width and length < width:
        # This might be correct for some parts, but flag it
        notes['dimension_order'] = "Note: Length is smaller than width. Verify this is correct."
        validated['length_mm'] = length
        validated['width_mm'] = width
    
    # Rule 5: Check for missing critical dimensions
    if not validated.get('length_mm') and not validated.get('max_diameter_mm'):
        notes['missing_critical'] = "Warning: Missing both length and diameter. Cannot calculate cost."
    
    return validated, notes


def correct_common_errors(dimensions: Dict, part_type: str = None) -> Dict:
    """
    Correct common dimension extraction errors.
    """
    corrected = dimensions.copy()
    
    # Common error: AI reads "50" as "5.0" or vice versa
    # If dimension seems too small, might be decimal error
    for key in ['max_diameter_mm', 'length_mm', 'width_mm', 'height_mm']:
        if key in corrected and corrected[key]:
            value = corrected[key]
            # If value is between 0.1 and 10, might be missing a zero
            # But we can't auto-correct this without context
            pass
    
    # Common error: Units confusion (inches vs mm)
    # If dimensions are in typical inch ranges (0.5-20), might be inches
    # But we'll assume mm for now and let user correct
    
    return corrected


def suggest_corrections(dimensions: Dict, validation_notes: Dict) -> Dict:
    """
    Suggest corrections based on validation notes.
    """
    suggestions = {}
    
    if 'inner_diameter' in validation_notes:
        suggestions['inner_diameter'] = "Inner diameter should be less than outer diameter. Please verify."
    
    if 'missing_critical' in validation_notes:
        suggestions['action'] = "Please enter dimensions manually or upload a CAD file for accurate extraction."
    
    return suggestions
