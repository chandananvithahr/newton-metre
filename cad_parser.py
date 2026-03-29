"""
CAD file parsing utilities for native CAD formats
Supports DXF, STEP, STL, and other CAD formats
"""
from pathlib import Path
from typing import Dict, Optional, List
from PIL import Image
import io

def parse_dxf_file(dxf_path: Path) -> Dict:
    """
    Parse DXF file and extract dimensions and features.
    
    Args:
        dxf_path: Path to DXF file
        
    Returns:
        Dictionary with extracted CAD data
    """
    try:
        import ezdxf
        
        doc = ezdxf.readfile(str(dxf_path))
        msp = doc.modelspace()
        
        # Extract entities
        lines = []
        circles = []
        arcs = []
        dimensions = []
        
        for entity in msp:
            if entity.dxftype() == 'LINE':
                lines.append({
                    'start': entity.dxf.start,
                    'end': entity.dxf.end,
                    'length': entity.dxf.start.distance(entity.dxf.end)
                })
            elif entity.dxftype() == 'CIRCLE':
                circles.append({
                    'center': entity.dxf.center,
                    'radius': entity.dxf.radius,
                    'diameter': entity.dxf.radius * 2
                })
            elif entity.dxftype() == 'ARC':
                arcs.append({
                    'center': entity.dxf.center,
                    'radius': entity.dxf.radius,
                    'start_angle': entity.dxf.start_angle,
                    'end_angle': entity.dxf.end_angle
                })
            elif entity.dxftype() == 'DIMENSION':
                dimensions.append({
                    'defpoint': entity.dxf.defpoint,
                    'text': entity.dxf.text if hasattr(entity.dxf, 'text') else '',
                    'dimtype': entity.dxf.dimtype
                })
        
        # Calculate bounding box
        all_points = []
        for line in lines:
            all_points.extend([line['start'], line['end']])
        for circle in circles:
            center = circle['center']
            radius = circle['radius']
            all_points.extend([
                (center.x - radius, center.y - radius),
                (center.x + radius, center.y + radius)
            ])
        
        if all_points:
            x_coords = [p[0] if hasattr(p, '__iter__') else p.x for p in all_points]
            y_coords = [p[1] if hasattr(p, '__iter__') else p.y for p in all_points]
            
            width = max(x_coords) - min(x_coords)
            height = max(y_coords) - min(y_coords)
        else:
            width = height = 0
        
        # Find largest circle (likely OD for turning parts)
        max_diameter = max([c['diameter'] for c in circles], default=0)
        
        # Extract dimensions from dimension entities
        extracted_dims = {}
        for dim in dimensions:
            if dim['text']:
                try:
                    # Try to parse dimension text
                    value = float(dim['text'].replace('mm', '').strip())
                    if 'DIAMETER' in str(dim['dimtype']):
                        extracted_dims['max_diameter_mm'] = value
                    elif 'LINEAR' in str(dim['dimtype']):
                        if 'length_mm' not in extracted_dims:
                            extracted_dims['length_mm'] = value
                except:
                    pass
        
        return {
            'format': 'DXF',
            'entities': {
                'lines': len(lines),
                'circles': len(circles),
                'arcs': len(arcs),
                'dimensions': len(dimensions)
            },
            'dimensions': {
                'max_diameter_mm': max_diameter if max_diameter > 0 else extracted_dims.get('max_diameter_mm'),
                'width_mm': width,
                'height_mm': height,
                **extracted_dims
            },
            'features': _extract_dxf_features(lines, circles, arcs),
            'confidence': 'high',  # Direct CAD data = high confidence
            'source': 'dxf_parser'
        }
        
    except ImportError:
        return {"error": "ezdxf not installed. Install with: pip install ezdxf"}
    except Exception as e:
        return {"error": f"Error parsing DXF: {str(e)}"}


def _extract_dxf_features(lines, circles, arcs) -> List[Dict]:
    """Extract features from DXF entities."""
    features = []
    
    # Threads (typically shown as parallel lines or specific patterns)
    # This is simplified - real implementation would analyze patterns
    if len(circles) > 1:
        features.append({
            'type': 'hole',
            'quantity': len(circles),
            'source': 'dxf_circles'
        })
    
    return features


def parse_stl_file(stl_path: Path) -> Dict:
    """
    Parse STL file and extract 3D geometry information.
    
    Args:
        stl_path: Path to STL file
        
    Returns:
        Dictionary with extracted geometry data
    """
    try:
        import trimesh
        
        mesh = trimesh.load(str(stl_path))
        
        # Calculate bounding box
        bounds = mesh.bounds
        dimensions_3d = {
            'length_mm': (bounds[1][0] - bounds[0][0]) * 1000,  # Convert to mm
            'width_mm': (bounds[1][1] - bounds[0][1]) * 1000,
            'height_mm': (bounds[1][2] - bounds[0][2]) * 1000
        }
        
        # Calculate volume
        volume_m3 = mesh.volume
        volume_mm3 = volume_m3 * 1e9  # Convert to mm³
        
        # For turning parts, estimate OD from bounding box
        max_diameter = max(dimensions_3d['width_mm'], dimensions_3d['height_mm'])
        
        return {
            'format': 'STL',
            'dimensions': {
                'max_diameter_mm': max_diameter,
                **dimensions_3d
            },
            'geometry': {
                'volume_mm3': volume_mm3,
                'surface_area_mm2': mesh.area * 1e6,
                'vertices': len(mesh.vertices),
                'faces': len(mesh.faces)
            },
            'confidence': 'high',
            'source': 'stl_parser'
        }
        
    except ImportError:
        return {"error": "trimesh not installed. Install with: pip install trimesh"}
    except Exception as e:
        return {"error": f"Error parsing STL: {str(e)}"}


def parse_step_file(step_path: Path) -> Dict:
    """
    Parse STEP file using pythonOCC (if available).
    
    Args:
        step_path: Path to STEP file
        
    Returns:
        Dictionary with extracted CAD data
    """
    try:
        from OCC.Core.IFSelect import IFSelect_RetDone
        from OCC.Core.Interface import Interface_Static_SetCVal
        from OCC.Core.STEPControl_Reader import STEPControl_Reader
        
        step_reader = STEPControl_Reader()
        status = step_reader.ReadFile(str(step_path))
        
        if status == IFSelect_RetDone:
            step_reader.TransferRoots()
            shape = step_reader.OneShape()
            
            # Extract bounding box
            from OCC.Core.Bnd import Bnd_Box
            from OCC.Core.BRepBndLib import brepbndlib
            
            bbox = Bnd_Box()
            brepbndlib.Add(shape, bbox)
            xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
            
            return {
                'format': 'STEP',
                'dimensions': {
                    'length_mm': (xmax - xmin) * 1000,
                    'width_mm': (ymax - ymin) * 1000,
                    'height_mm': (zmax - zmin) * 1000,
                    'max_diameter_mm': max((xmax - xmin), (ymax - ymin)) * 1000
                },
                'confidence': 'high',
                'source': 'step_parser'
            }
        else:
            return {"error": "Failed to read STEP file"}
            
    except ImportError:
        return {"error": "pythonOCC not installed. Install with: pip install pythonocc-core"}
    except Exception as e:
        return {"error": f"Error parsing STEP: {str(e)}"}


def detect_cad_format(file_path: Path) -> str:
    """Detect CAD file format from extension."""
    ext = file_path.suffix.lower()
    format_map = {
        '.dxf': 'DXF',
        '.dwg': 'DWG',  # Would need additional library
        '.step': 'STEP',
        '.stp': 'STEP',
        '.iges': 'IGES',
        '.igs': 'IGES',
        '.stl': 'STL',
        '.obj': 'OBJ',
        '.ply': 'PLY',
        '.brep': 'BREP'
    }
    return format_map.get(ext, 'UNKNOWN')


def parse_cad_file(file_path: Path) -> Dict:
    """
    Auto-detect and parse CAD file based on format.
    
    Args:
        file_path: Path to CAD file
        
    Returns:
        Dictionary with extracted data
    """
    file_format = detect_cad_format(file_path)
    
    if file_format == 'DXF':
        return parse_dxf_file(file_path)
    elif file_format == 'STL':
        return parse_stl_file(file_path)
    elif file_format == 'STEP':
        return parse_step_file(file_path)
    elif file_format == 'OBJ' or file_format == 'PLY':
        return parse_stl_file(file_path)  # trimesh supports these too
    else:
        return {"error": f"Unsupported CAD format: {file_format}"}
