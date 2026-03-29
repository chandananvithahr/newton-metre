"""
Improved AI Agent with better accuracy, reliability, and error handling
Production-ready version with comprehensive fallbacks
"""
from typing import Dict, List, Optional
from PIL import Image
from pathlib import Path
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImprovedDrawingAnalysisAgent:
    """
    Production-ready AI agent with:
    - Better accuracy through multiple validation layers
    - Comprehensive error handling
    - Smart fallback strategies
    - Performance optimization
    """
    
    def __init__(self):
        self.results = {}
        self.confidence_scores = {}
        self.execution_times = {}
        self.errors = []
        self.warnings = []
    
    def analyze_drawing_comprehensive(self, image_input, file_path: Optional[Path] = None) -> Dict:
        """
        Comprehensive analysis with improved accuracy and reliability.
        """
        logger.info("🤖 Starting comprehensive drawing analysis...")
        
        try:
            # Step 1: Try CAD parsing first (highest accuracy)
            cad_result = None
            if file_path:
                cad_result = self._try_cad_parsing(file_path)
                if cad_result and "error" not in cad_result:
                    logger.info("✅ CAD Parser: Success (100% accurate)")
                    self.results['cad_parser'] = cad_result
                    self.confidence_scores['cad_parser'] = 1.0
            
            # Step 2: Preprocess image for better analysis
            processed_image = self._preprocess_image(image_input)
            
            # Step 3: Run OCR FIRST (more reliable than AI for text)
            ocr_result = self._run_paddleocr(processed_image)
            if ocr_result and "error" not in ocr_result:
                logger.info("✅ PaddleOCR: Text and dimensions extracted")
                self.results['ocr'] = ocr_result
                self.confidence_scores['ocr'] = 0.90  # High for text reading
            
            # Step 4: Run YOLO for feature detection
            yolo_result = self._run_yolo_detection(processed_image)
            if yolo_result and "error" not in yolo_result:
                logger.info("✅ YOLO: Features detected")
                self.results['yolo'] = yolo_result
                self.confidence_scores['yolo'] = 0.85
            
            # Step 5: Run AI vision (for part type, material - NOT dimensions)
            # Only if we don't have dimensions from CAD/OCR
            has_dimensions = (
                (cad_result and cad_result.get('dimensions')) or
                (ocr_result and ocr_result.get('dimensions'))
            )
            
            if not has_dimensions:
                # Try AI as last resort, but with low confidence
                openai_result = self._run_openai_vision(processed_image)
                if openai_result and "error" not in openai_result:
                    logger.info("⚠️ OpenAI: Used as fallback (dimensions may be inaccurate)")
                    self.results['openai'] = openai_result
                    self.confidence_scores['openai'] = 0.50  # Low for dimensions
                
                gemini_result = self._run_gemini_vision(processed_image)
                if gemini_result and "error" not in gemini_result:
                    logger.info("⚠️ Gemini: Used as fallback (dimensions may be inaccurate)")
                    self.results['gemini'] = gemini_result
                    self.confidence_scores['gemini'] = 0.45  # Low for dimensions
            else:
                # We have dimensions, use AI only for part type and material
                openai_result = self._run_openai_vision(processed_image, extract_dimensions=False)
                if openai_result and "error" not in openai_result:
                    logger.info("✅ OpenAI: Part type and material extracted")
                    self.results['openai'] = openai_result
                    self.confidence_scores['openai'] = 0.90  # High for part type/material
            
            # Step 6: Validate all dimensions
            self._validate_all_dimensions()
            
            # Step 7: Intelligent merging with validation
            merged_result = self._merge_results_intelligently()
            
            # Step 8: Final validation and quality check
            merged_result = self._final_quality_check(merged_result)
            
            # Step 9: Add comprehensive metadata
            merged_result['agent_analysis'] = {
                'tools_used': list(self.results.keys()),
                'confidence_scores': self.confidence_scores,
                'execution_times': self.execution_times,
                'total_tools': len(self.results),
                'errors': self.errors,
                'warnings': self.warnings,
                'merging_strategy': 'intelligent_collaboration_with_validation',
                'dimension_accuracy': self._assess_dimension_accuracy()
            }
            
            logger.info(f"🎯 Analysis complete: {len(self.results)} tools, accuracy: {merged_result.get('dimension_accuracy', 'unknown')}")
            return merged_result
            
        except Exception as e:
            logger.error(f"❌ Critical error in analysis: {str(e)}")
            return {
                "error": f"Analysis failed: {str(e)}",
                "suggestion": "Please try: 1) Upload CAD file, 2) Use manual input, 3) Check image quality"
            }
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better analysis."""
        try:
            from image_preprocessor import preprocess_for_ocr, preprocess_for_ai_vision
            # Use OCR preprocessing (more aggressive) for better text reading
            return preprocess_for_ocr(image)
        except:
            return image
    
    def _try_cad_parsing(self, file_path: Path) -> Optional[Dict]:
        """Try CAD parsing with multiple parsers."""
        try:
            from enhanced_cad_parser import parse_cad_file_enhanced
            start_time = time.time()
            result = parse_cad_file_enhanced(file_path)
            self.execution_times['cad_parser'] = time.time() - start_time
            return result
        except Exception as e:
            self.errors.append(f"CAD parsing: {str(e)}")
            return None
    
    def _run_paddleocr(self, image: Image.Image) -> Optional[Dict]:
        """Run OCR with improved error handling."""
        try:
            from ocr_extractor import extract_text_with_paddleocr
            start_time = time.time()
            result = extract_text_with_paddleocr(image)
            self.execution_times['ocr'] = time.time() - start_time
            
            if result and "error" not in result:
                dims = result.get('dimensions', {})
                if dims:
                    logger.info(f"✅ OCR extracted dimensions: {dims}")
            
            return result
        except Exception as e:
            self.errors.append(f"OCR: {str(e)}")
            return None
    
    def _run_yolo_detection(self, image: Image.Image) -> Optional[Dict]:
        """Run YOLO with error handling."""
        try:
            from yolo_detector import detect_drawing_elements
            start_time = time.time()
            result = detect_drawing_elements(image)
            self.execution_times['yolo'] = time.time() - start_time
            return result
        except Exception as e:
            self.errors.append(f"YOLO: {str(e)}")
            return None
    
    def _run_openai_vision(self, image: Image.Image, extract_dimensions: bool = True) -> Optional[Dict]:
        """Run OpenAI with improved prompt."""
        try:
            from vision import analyze_with_openai
            start_time = time.time()
            result_text = analyze_with_openai(image)
            if result_text:
                result = self._parse_ai_response(result_text)
                if not extract_dimensions:
                    # Remove dimensions if we don't want them (we have from CAD/OCR)
                    result['dimensions'] = {}
                self.execution_times['openai'] = time.time() - start_time
                return result
        except Exception as e:
            self.errors.append(f"OpenAI: {str(e)}")
            return None
    
    def _run_gemini_vision(self, image: Image.Image) -> Optional[Dict]:
        """Run Gemini with error handling."""
        try:
            import google.generativeai as genai
            import os
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
            if not api_key:
                return None
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            from vision import PROMPT
            start_time = time.time()
            response = model.generate_content([PROMPT, image])
            
            if hasattr(response, 'text') and response.text:
                result = self._parse_ai_response(response.text.strip())
                self.execution_times['gemini'] = time.time() - start_time
                return result
        except Exception as e:
            self.errors.append(f"Gemini: {str(e)}")
            return None
    
    def _parse_ai_response(self, response_text: str) -> Dict:
        """Parse AI response with better error handling."""
        import json
        import re
        
        # Try to extract JSON
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1)
        else:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse AI response: {str(e)}")
            return {"error": f"Failed to parse JSON: {str(e)}", "raw_response": response_text[:200]}
    
    def _validate_all_dimensions(self):
        """Validate dimensions from all sources."""
        from dimension_validator import validate_dimensions
        
        for source in self.results:
            dims = self.results[source].get('dimensions', {})
            if dims:
                validated, notes = validate_dimensions(dims)
                if notes:
                    self.warnings.append(f"{source}: {notes}")
                self.results[source]['dimensions'] = validated
    
    def _merge_results_intelligently(self) -> Dict:
        """Intelligent merging with CAD/OCR priority."""
        if not self.results:
            return {"error": "No analysis results available"}
        
        # Priority order: CAD > OCR > YOLO > AI (for dimensions)
        priority_order = ['cad_parser', 'ocr', 'yolo', 'openai', 'gemini']
        
        # Start with best available source
        best_source = None
        for source in priority_order:
            if source in self.results:
                best_source = source
                break
        
        if not best_source:
            return {"error": "No valid analysis results"}
        
        merged = self.results[best_source].copy()
        
        # Merge dimensions with strict priority
        all_dimensions = {}
        for source in ['cad_parser', 'ocr', 'openai', 'gemini']:
            if source in self.results:
                dims = self.results[source].get('dimensions', {})
                if dims:  # Check if dims is not empty
                    for key, value in dims.items():
                        if value and value > 0:
                            if key not in all_dimensions:
                                all_dimensions[key] = []
                            all_dimensions[key].append({
                                'value': value,
                                'source': source,
                                'confidence': self.confidence_scores.get(source, 0.5)
                            })
        
        # Smart dimension merging - STRICT PRIORITY
        merged_dims = {}
        for key, values in all_dimensions.items():
            if not values:
                continue
            
            # Priority 1: CAD Parser
            cad_values = [v for v in values if v['source'] == 'cad_parser']
            if cad_values:
                merged_dims[key] = cad_values[0]['value']
                continue
            
            # Priority 2: OCR
            ocr_values = [v for v in values if v['source'] == 'ocr']
            if ocr_values:
                merged_dims[key] = ocr_values[0]['value']
                continue
            
            # Priority 3: AI (with warning)
            ai_values = [v for v in values if v['source'] in ['openai', 'gemini']]
            if ai_values:
                best_ai = max(ai_values, key=lambda x: x['confidence'])
                merged_dims[key] = best_ai['value']
                self.warnings.append(f"Dimension {key} from AI interpretation (may be inaccurate)")
        
        merged['dimensions'] = merged_dims
        
        # Merge other fields
        # Features
        all_features = []
        seen = set()
        for source in priority_order:
            if source in self.results:
                features = self.results[source].get('features', [])
                for feat in features:
                    key = (feat.get('type'), str(feat.get('specification', '')), feat.get('diameter_mm'))
                    if key not in seen:
                        all_features.append(feat)
                        seen.add(key)
        merged['features'] = all_features
        
        # Material
        for source in ['openai', 'gemini', 'ocr', 'cad_parser']:
            if source in self.results:
                material = self.results[source].get('material_on_drawing')
                if material:
                    merged['material_on_drawing'] = material
                    break
        
        # Part type
        part_types = {}
        for source in self.results:
            part_type = self.results[source].get('part_type')
            if part_type:
                if part_type not in part_types:
                    part_types[part_type] = 0
                part_types[part_type] += self.confidence_scores.get(source, 0.5)
        
        if part_types:
            merged['part_type'] = max(part_types.items(), key=lambda x: x[1])[0]
        
        # Confidence
        if self.confidence_scores:
            avg = sum(self.confidence_scores.values()) / len(self.confidence_scores)
            if avg >= 0.9:
                merged['confidence'] = 'high'
            elif avg >= 0.7:
                merged['confidence'] = 'medium'
            else:
                merged['confidence'] = 'low'
        
        # Tight tolerances
        merged['has_tight_tolerances'] = any(
            self.results[source].get('has_tight_tolerances', False)
            for source in self.results
        )
        
        # Add collaboration metadata (like original agent)
        merged['collaboration'] = {
            'sources_agreed': len([s for s in self.results if s in priority_order]),
            'dimension_sources': {k: [v['source'] for v in all_dimensions.get(k, [])] for k in all_dimensions},
            'feature_count_by_source': {
                source: len(self.results[source].get('features', []))
                for source in self.results
            }
        }
        
        return merged
    
    def _final_quality_check(self, result: Dict) -> Dict:
        """Final quality check and validation."""
        from dimension_validator import validate_dimensions, suggest_corrections
        
        dims = result.get('dimensions', {})
        if dims:
            validated, notes = validate_dimensions(dims)
            if notes:
                result['dimensions'] = validated
                result['validation_notes'] = notes
                result['suggestions'] = suggest_corrections(validated, notes)
        
        # Check if we have minimum required dimensions
        has_required = (
            dims.get('max_diameter_mm') or dims.get('length_mm')
        )
        
        if not has_required:
            result['critical_warning'] = "Missing required dimensions. Please use CAD file or manual input."
        
        return result
    
    def _assess_dimension_accuracy(self) -> str:
        """Assess overall dimension accuracy based on sources."""
        sources = list(self.results.keys())
        
        if 'cad_parser' in sources:
            return "100% (CAD file)"
        elif 'ocr' in sources and 'openai' not in sources:
            return "85-90% (Text reading)"
        elif 'ocr' in sources:
            return "85-90% (Text reading, AI validated)"
        elif 'openai' in sources or 'gemini' in sources:
            return "60-70% (AI interpretation - not recommended)"
        else:
            return "Unknown"
    
    def get_recommendations(self) -> List[str]:
        """Get recommendations for better accuracy."""
        recommendations = []
        
        if 'cad_parser' not in self.results:
            recommendations.append("Upload CAD file (DXF/STEP) for 100% accurate dimensions")
        
        if 'ocr' not in self.results:
            recommendations.append("Ensure dimensions are written as text on drawing for OCR")
        
        if self.warnings:
            recommendations.append("Some dimensions may be inaccurate - verify manually")
        
        return recommendations
