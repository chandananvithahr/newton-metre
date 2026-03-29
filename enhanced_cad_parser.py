"""
Enhanced CAD file parsing with multiple libraries
Supports: DXF, STEP, IGES, BREP, STL, OBJ, PLY, FCStd
"""
from pathlib import Path
from typing import Dict, Optional, List, Tuple
from PIL import Image
import io
import tempfile

def parse_dxf_ezdxf(dxf_path: Path) -> Dict:
    """Parse DXF using ezdxf library."""
    try:
        import ezdxf
        
        doc = ezdxf.readfile(str(dxf_path))
        msp = doc.modelspace()
        
        # Extract all entities
        entities = {
            'lines': [],
            'circles': [],
            'arcs': [],
            'dimensions': [],
            'text': [],
            'blocks': []
        }
        
        for entity in msp:
            etype = entity.dxftype()
            if etype == 'LINE':
                entities['lines'].append({
                    'start': (entity.dxf.start.x, entity.dxf.start.y),
                    'end': (entity.dxf.end.x, entity.dxf.end.y)
                })
            elif etype == 'CIRCLE':
                entities['circles'].append({
                    'center': (entity.dxf.center.x, entity.dxf.center.y),
                    'radius': entity.dxf.radius,
                    'diameter': entity.dxf.radius * 2
                })
            elif etype == 'ARC':
                entities['arcs'].append({
                    'center': (entity.dxf.center.x, entity.dxf.center.y),
                    'radius': entity.dxf.radius,
                    'start_angle': entity.dxf.start_angle,
                    'end_angle': entity.dxf.end_angle
                })
            elif etype == 'DIMENSION':
                entities['dimensions'].append({
                    'defpoint': (entity.dxf.defpoint.x, entity.dxf.defpoint.y),
                    'text': getattr(entity.dxf, 'text', ''),
                    'dimtype': entity.dxf.dimtype
                })
            elif etype == 'TEXT' or etype == 'MTEXT':
                entities['text'].append({
                    'content': entity.dxf.text if hasattr(entity.dxf, 'text') else str(entity),
                    'position': (entity.dxf.insert.x, entity.dxf.insert.y) if hasattr(entity.dxf, 'insert') else None
                })
        
        # Calculate bounding box and extract dimensions
        all_points = []
        for line in entities['lines']:
            all_points.extend([line['start'], line['end']])
        for circle in entities['circles']:
            center = circle['center']
            radius = circle['radius']
            all_points.extend([
                (center[0] - radius, center[1] - radius),
                (center[0] + radius, center[1] + radius)
            ])
        
        dimensions = {}
        if all_points:
            x_coords = [p[0] for p in all_points]
            y_coords = [p[1] for p in all_points]
            dimensions['width_mm'] = abs(max(x_coords) - min(x_coords))
            dimensions['height_mm'] = abs(max(y_coords) - min(y_coords))
        
        # Find largest circle (likely OD)
        if entities['circles']:
            max_dia = max([c['diameter'] for c in entities['circles']])
            dimensions['max_diameter_mm'] = max_dia
        
        # Extract material from text
        material = None
        for text_entity in entities['text']:
            text_content = text_entity['content'].upper()
            if any(keyword in text_content for keyword in ['STEEL', 'ALUMINUM', 'BRASS', 'MATERIAL']):
                material = text_entity['content']
                break
        
        return {
            'format': 'DXF',
            'parser': 'ezdxf',
            'dimensions': dimensions,
            'entities': {k: len(v) for k, v in entities.items()},
            'material_on_drawing': material,
            'features': _extract_features_from_dxf(entities),
            'confidence': 'high',
            'source': 'ezdxf_parser'
        }
    except Exception as e:
        return {"error": f"ezdxf parsing error: {str(e)}"}


def parse_step_occ(step_path: Path) -> Dict:
    """Parse STEP file using OpenCascade (pythonOCC)."""
    try:
        from OCC.Core.IFSelect import IFSelect_RetDone
        from OCC.Core.STEPControl_Reader import STEPControl_Reader
        from OCC.Core.Bnd import Bnd_Box
        from OCC.Core.BRepBndLib import brepbndlib
        
        reader = STEPControl_Reader()
        status = reader.ReadFile(str(step_path))
        
        if status == IFSelect_RetDone:
            reader.TransferRoots()
            shape = reader.OneShape()
            
            # Get bounding box
            bbox = Bnd_Box()
            brepbndlib.Add(shape, bbox)
            xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
            
            # Calculate dimensions
            length = (xmax - xmin) * 1000  # Convert to mm
            width = (ymax - ymin) * 1000
            height = (zmax - zmin) * 1000
            
            return {
                'format': 'STEP',
                'parser': 'pythonOCC',
                'dimensions': {
                    'length_mm': length,
                    'width_mm': width,
                    'height_mm': height,
                    'max_diameter_mm': max(length, width)  # Estimate
                },
                'confidence': 'high',
                'source': 'occ_parser'
            }
        else:
            return {"error": "Failed to read STEP file"}
    except ImportError:
        return {"error": "pythonOCC not installed. Install with: pip install pythonocc-core"}
    except Exception as e:
        return {"error": f"OCC parsing error: {str(e)}"}


def parse_step_cadquery(step_path: Path) -> Dict:
    """Parse STEP file using cadquery."""
    try:
        import cadquery as cq
        
        # Load STEP file
        result = cq.importers.importStep(str(step_path))
        
        # Get bounding box
        bbox = result.BoundingBox()
        
        dimensions = {
            'length_mm': (bbox.xmax - bbox.xmin) * 1000,
            'width_mm': (bbox.ymax - bbox.ymin) * 1000,
            'height_mm': (bbox.zmax - bbox.zmin) * 1000,
            'max_diameter_mm': max((bbox.xmax - bbox.xmin), (bbox.ymax - bbox.ymin)) * 1000
        }
        
        return {
            'format': 'STEP',
            'parser': 'cadquery',
            'dimensions': dimensions,
            'confidence': 'high',
            'source': 'cadquery_parser'
        }
    except ImportError:
        return {"error": "cadquery not installed. Install with: pip install cadquery"}
    except Exception as e:
        return {"error": f"cadquery parsing error: {str(e)}"}


def parse_stl_trimesh(stl_path: Path) -> Dict:
    """Parse STL/OBJ/PLY using trimesh."""
    try:
        import trimesh
        
        mesh = trimesh.load(str(stl_path))
        
        # Get bounding box
        bounds = mesh.bounds
        dimensions = {
            'length_mm': (bounds[1][0] - bounds[0][0]) * 1000,
            'width_mm': (bounds[1][1] - bounds[0][1]) * 1000,
            'height_mm': (bounds[1][2] - bounds[0][2]) * 1000
        }
        
        # Estimate OD for turning parts
        dimensions['max_diameter_mm'] = max(dimensions['width_mm'], dimensions['height_mm'])
        
        # Calculate volume
        volume_mm3 = mesh.volume * 1e9
        
        return {
            'format': 'STL/OBJ/PLY',
            'parser': 'trimesh',
            'dimensions': dimensions,
            'geometry': {
                'volume_mm3': volume_mm3,
                'surface_area_mm2': mesh.area * 1e6,
                'vertices': len(mesh.vertices),
                'faces': len(mesh.faces)
            },
            'confidence': 'high',
            'source': 'trimesh_parser'
        }
    except Exception as e:
        return {"error": f"trimesh parsing error: {str(e)}"}


def parse_fcstd_freecad(fcstd_path: Path) -> Dict:
    """Parse FreeCAD file using FreeCAD Python API."""
    try:
        import FreeCAD
        import Part
        
        # Load FreeCAD document
        doc = FreeCAD.open(str(fcstd_path))
        
        # Get all objects
        objects = doc.Objects
        dimensions = {}
        
        for obj in objects:
            if hasattr(obj, 'Shape'):
                shape = obj.Shape
                bbox = shape.BoundBox
                
                # Accumulate dimensions
                if not dimensions:
                    dimensions = {
                        'length_mm': (bbox.XMax - bbox.XMin) * 1000,
                        'width_mm': (bbox.YMax - bbox.YMin) * 1000,
                        'height_mm': (bbox.ZMax - bbox.ZMin) * 1000
                    }
                else:
                    dimensions['length_mm'] = max(dimensions['length_mm'], (bbox.XMax - bbox.XMin) * 1000)
                    dimensions['width_mm'] = max(dimensions['width_mm'], (bbox.YMax - bbox.YMin) * 1000)
                    dimensions['height_mm'] = max(dimensions['height_mm'], (bbox.ZMax - bbox.ZMin) * 1000)
        
        dimensions['max_diameter_mm'] = max(dimensions.get('width_mm', 0), dimensions.get('height_mm', 0))
        
        FreeCAD.closeDocument(doc.Name)
        
        return {
            'format': 'FCStd',
            'parser': 'FreeCAD',
            'dimensions': dimensions,
            'confidence': 'high',
            'source': 'freecad_parser'
        }
    except ImportError:
        return {"error": "FreeCAD not available. FreeCAD must be installed separately."}
    except Exception as e:
        return {"error": f"FreeCAD parsing error: {str(e)}"}


def parse_iges_occ(iges_path: Path) -> Dict:
    """Parse IGES file using OpenCascade."""
    try:
        from OCC.Core.IFSelect import IFSelect_RetDone
        from OCC.Core.IGESControl_Reader import IGESControl_Reader
        from OCC.Core.Bnd import Bnd_Box
        from OCC.Core.BRepBndLib import brepbndlib
        
        reader = IGESControl_Reader()
        status = reader.ReadFile(str(iges_path))
        
        if status == IFSelect_RetDone:
            reader.TransferRoots()
            shape = reader.OneShape()
            
            bbox = Bnd_Box()
            brepbndlib.Add(shape, bbox)
            xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
            
            return {
                'format': 'IGES',
                'parser': 'pythonOCC',
                'dimensions': {
                    'length_mm': (xmax - xmin) * 1000,
                    'width_mm': (ymax - ymin) * 1000,
                    'height_mm': (zmax - zmin) * 1000,
                    'max_diameter_mm': max((xmax - xmin), (ymax - ymin)) * 1000
                },
                'confidence': 'high',
                'source': 'occ_parser'
            }
        else:
            return {"error": "Failed to read IGES file"}
    except Exception as e:
        return {"error": f"IGES parsing error: {str(e)}"}


def _extract_features_from_dxf(entities: Dict) -> List[Dict]:
    """Extract features from DXF entities."""
    features = []
    
    # Count holes (circles)
    if entities['circles']:
        features.append({
            'type': 'hole',
            'quantity': len(entities['circles']),
            'source': 'dxf_circles'
        })
    
    # Detect threads (typically shown as parallel lines or specific patterns)
    # This is simplified - real implementation would analyze patterns
    if len(entities['lines']) > 10:
        features.append({
            'type': 'thread_pattern',
            'quantity': 1,
            'source': 'dxf_lines'
        })
    
    return features


def parse_cad_file_enhanced(file_path: Path) -> Dict:
    """
    Enhanced CAD file parser with multiple library support.
    Tries multiple parsers for best results.
    """
    file_ext = file_path.suffix.lower()
    
    # Try appropriate parser based on file extension
    if file_ext == '.dxf':
        result = parse_dxf_ezdxf(file_path)
        if "error" not in result:
            return result
        return {"error": result.get("error", "DXF parsing failed")}
    
    elif file_ext in ['.step', '.stp']:
        # Try multiple STEP parsers
        result = parse_step_cadquery(file_path)
        if "error" not in result:
            return result
        
        result = parse_step_occ(file_path)
        if "error" not in result:
            return result
        
        return {"error": "STEP parsing failed with all available parsers"}
    
    elif file_ext in ['.iges', '.igs']:
        result = parse_iges_occ(file_path)
        if "error" not in result:
            return result
        return {"error": result.get("error", "IGES parsing failed")}
    
    elif file_ext in ['.stl', '.obj', '.ply']:
        result = parse_stl_trimesh(file_path)
        if "error" not in result:
            return result
        return {"error": result.get("error", "STL/OBJ/PLY parsing failed")}
    
    elif file_ext == '.fcstd':
        result = parse_fcstd_freecad(file_path)
        if "error" not in result:
            return result
        return {"error": result.get("error", "FreeCAD parsing failed")}
    
    elif file_ext == '.brep':
        # BREP can be parsed with OCC
        result = parse_step_occ(file_path)  # OCC can handle BREP too
        if "error" not in result:
            result['format'] = 'BREP'
            return result
        return {"error": "BREP parsing failed"}
    
    else:
        return {"error": f"Unsupported CAD format: {file_ext}"}
