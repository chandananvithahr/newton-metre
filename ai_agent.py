"""
AI Agent Orchestrator - Automatically runs all AI tools, compares and collaborates results
"""
from typing import Dict, List, Optional
from PIL import Image
from pathlib import Path
import time

class DrawingAnalysisAgent:
    """
    Intelligent agent that orchestrates all AI tools:
    - YOLO (object detection)
    - OpenAI GPT-4o Vision
    - Gemini 2.0 Flash
    - PaddleOCR
    - CAD Parsers
    Compares and merges results for best accuracy
    """
    
    def __init__(self):
        self.results = {}
        self.confidence_scores = {}
        self.execution_times = {}
    
    def analyze_drawing_comprehensive(self, image_input, file_path: Optional[Path] = None) -> Dict:
        """
        Comprehensive analysis using all available AI tools.
        Automatically runs, compares, and merges results.
        """
        print("🤖 AI Agent: Starting comprehensive analysis...")
        
        # Step 1: Try CAD parsing first (if file path provided)
        cad_result = None
        if file_path:
            cad_result = self._try_cad_parsing(file_path)
            if cad_result and "error" not in cad_result:
                print("✅ CAD Parser: Success (100% accurate)")
                self.results['cad_parser'] = cad_result
                self.confidence_scores['cad_parser'] = 1.0  # 100% confidence
        
        # Step 2: Run YOLO detection (always, if available)
        yolo_result = self._run_yolo_detection(image_input)
        if yolo_result and "error" not in yolo_result:
            print("✅ YOLO: Detected features and symbols")
            self.results['yolo'] = yolo_result
            self.confidence_scores['yolo'] = 0.85  # High confidence for object detection
        
        # Step 3: Run OpenAI GPT-4o Vision (primary AI)
        openai_result = self._run_openai_vision(image_input)
        if openai_result and "error" not in openai_result:
            print("✅ OpenAI GPT-4o: Analysis complete")
            self.results['openai'] = openai_result
            self.confidence_scores['openai'] = 0.95  # Highest confidence
        
        # Step 4: Run Gemini 2.0 Flash (for validation - NOT dimensions)
        # NOTE: Gemini also NOT accurate for dimensions - use CAD parser or OCR
        gemini_result = self._run_gemini_vision(image_input)
        if gemini_result and "error" not in gemini_result:
            print("✅ Gemini 2.0 Flash: Analysis complete (part type, material, features)")
            self.results['gemini'] = gemini_result
            # Lower confidence for dimensions
            self.confidence_scores['gemini'] = 0.65  # Lower for dimensions
        
        # Step 5: Run PaddleOCR (text extraction) - CRITICAL for accurate dimensions!
        # OCR reads actual text on drawings, more reliable than AI interpretation
        ocr_result = self._run_paddleocr(image_input)
        if ocr_result and "error" not in ocr_result:
            print("✅ PaddleOCR: Text and dimensions extracted from drawing labels")
            self.results['ocr'] = ocr_result
            # OCR is MORE reliable than AI for dimensions (reads actual text, not guesses)
            self.confidence_scores['ocr'] = 0.85  # Better than AI for dimensions
        
        # Step 6: Validate dimensions before merging
        for source in self.results:
            dims = self.results[source].get('dimensions', {})
            if dims:
                from dimension_validator import validate_dimensions
                validated_dims, notes = validate_dimensions(dims)
                if notes:
                    print(f"⚠️ Validation notes for {source}: {notes}")
                self.results[source]['dimensions'] = validated_dims
        
        # Step 7: Intelligent result merging
        merged_result = self._merge_results_intelligently()
        
        # Step 8: Final validation of merged result
        merged_dims = merged_result.get('dimensions', {})
        if merged_dims:
            from dimension_validator import validate_dimensions, suggest_corrections
            final_validated, final_notes = validate_dimensions(merged_dims)
            if final_notes:
                print(f"⚠️ Final validation notes: {final_notes}")
                merged_result['dimensions'] = final_validated
                merged_result['validation_notes'] = final_notes
                merged_result['suggestions'] = suggest_corrections(final_validated, final_notes)
        
        # Step 7: Add metadata
        merged_result['agent_analysis'] = {
            'tools_used': list(self.results.keys()),
            'confidence_scores': self.confidence_scores,
            'execution_times': self.execution_times,
            'total_tools': len(self.results),
            'merging_strategy': 'intelligent_collaboration'
        }
        
        print(f"🎯 AI Agent: Merged results from {len(self.results)} tools")
        return merged_result
    
    def _try_cad_parsing(self, file_path: Path) -> Optional[Dict]:
        """Try CAD parsing if file is CAD format."""
        try:
            from enhanced_cad_parser import parse_cad_file_enhanced
            start_time = time.time()
            result = parse_cad_file_enhanced(file_path)
            self.execution_times['cad_parser'] = time.time() - start_time
            return result
        except Exception as e:
            print(f"⚠️ CAD Parser: {str(e)}")
            return None
    
    def _run_yolo_detection(self, image: Image.Image) -> Optional[Dict]:
        """Run YOLO object detection."""
        try:
            from yolo_detector import detect_drawing_elements
            start_time = time.time()
            result = detect_drawing_elements(image)
            self.execution_times['yolo'] = time.time() - start_time
            return result
        except Exception as e:
            print(f"⚠️ YOLO: {str(e)}")
            return None
    
    def _run_openai_vision(self, image: Image.Image) -> Optional[Dict]:
        """Run OpenAI GPT-4o Vision - NOTE: Not accurate for dimensions, use for part type/material."""
        try:
            from vision import analyze_with_openai
            from image_preprocessor import preprocess_for_ai_vision
            
            # Preprocess image for better analysis
            processed_image = preprocess_for_ai_vision(image)
            
            start_time = time.time()
            result_text = analyze_with_openai(processed_image)
            if result_text:
                import json
                # Parse JSON response
                result = self._parse_ai_response(result_text)
                
                # Lower confidence for dimensions (AI is not accurate)
                if 'dimensions' in result:
                    # Flag that these are AI-interpreted (may be inaccurate)
                    result['dimensions_ai_interpreted'] = True
                    result['dimension_warning'] = "AI-extracted dimensions may be inaccurate. Use CAD parser or OCR for accurate dimensions."
                
                self.execution_times['openai'] = time.time() - start_time
                return result
        except Exception as e:
            print(f"⚠️ OpenAI: {str(e)}")
            return None
    
    def _run_gemini_vision(self, image: Image.Image) -> Optional[Dict]:
        """Run Gemini 2.0 Flash Vision."""
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
            print(f"⚠️ Gemini: {str(e)}")
            return None
    
    def _run_paddleocr(self, image: Image.Image) -> Optional[Dict]:
        """Run PaddleOCR for text extraction."""
        try:
            from ocr_extractor import extract_text_with_paddleocr
            start_time = time.time()
            result = extract_text_with_paddleocr(image)
            self.execution_times['ocr'] = time.time() - start_time
            return result
        except Exception as e:
            print(f"⚠️ PaddleOCR: {str(e)}")
            return None
    
    def _parse_ai_response(self, response_text: str) -> Dict:
        """Parse AI response text to structured dict."""
        import json
        import re
        
        # Try to extract JSON from response
        # Handle markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1)
        else:
            # Try to find JSON object directly
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)
        
        try:
            return json.loads(response_text)
        except:
            # Fallback: return raw response
            return {"raw_response": response_text, "error": "Failed to parse JSON"}
    
    def _merge_results_intelligently(self) -> Dict:
        """
        Intelligently merge results from all AI tools.
        Uses confidence scores and cross-validation.
        """
        if not self.results:
            return {"error": "No analysis results available"}
        
        # Start with highest confidence result
        best_source = max(self.confidence_scores.items(), key=lambda x: x[1])[0]
        merged = self.results[best_source].copy()
        
        # Priority: CAD > OpenAI > Gemini > YOLO > OCR
        priority_order = ['cad_parser', 'openai', 'gemini', 'yolo', 'ocr']
        
        # Merge dimensions (take most confident or average if close)
        all_dimensions = {}
        for source in priority_order:
            if source in self.results:
                dims = self.results[source].get('dimensions', {})
                for key, value in dims.items():
                    if value and value > 0:
                        if key not in all_dimensions:
                            all_dimensions[key] = []
                        all_dimensions[key].append({
                            'value': value,
                            'source': source,
                            'confidence': self.confidence_scores.get(source, 0.5)
                        })
        
        # Smart dimension merging - PRIORITIZE CAD PARSER AND OCR OVER AI
        merged_dims = {}
        for key, values in all_dimensions.items():
            if not values:
                continue
            
            # Priority 1: CAD Parser (100% accurate)
            cad_values = [v for v in values if v['source'] == 'cad_parser']
            if cad_values:
                merged_dims[key] = cad_values[0]['value']
                continue
            
            # Priority 2: OCR (reads actual text, 85-90% accurate)
            ocr_values = [v for v in values if v['source'] == 'ocr']
            if ocr_values:
                # Use OCR value (more reliable than AI interpretation)
                merged_dims[key] = ocr_values[0]['value']
                continue
            
            # Priority 3: AI Vision (OpenAI/Gemini) - only if no CAD/OCR
            # But weight them lower since they're less accurate for dimensions
            ai_values = [v for v in values if v['source'] in ['openai', 'gemini']]
            if ai_values:
                # Use AI but with lower confidence
                # Prefer the value with highest confidence
                best_ai = max(ai_values, key=lambda x: x['confidence'])
                merged_dims[key] = best_ai['value']
                # Add warning that this is AI-interpreted
                print(f"⚠️ Warning: Dimension {key} from AI interpretation (may be inaccurate)")
                continue
            
            # Fallback: Weighted average
            total_weight = sum(v['confidence'] for v in values)
            if total_weight > 0:
                weighted_avg = sum(v['value'] * v['confidence'] for v in values) / total_weight
                merged_dims[key] = weighted_avg
            else:
                # Simple average
                merged_dims[key] = sum(v['value'] for v in values) / len(values)
        
        merged['dimensions'] = merged_dims
        
        # Merge features (combine unique features from all sources)
        all_features = []
        seen_features = set()
        for source in priority_order:
            if source in self.results:
                features = self.results[source].get('features', [])
                for feat in features:
                    feat_key = (
                        feat.get('type', ''),
                        str(feat.get('specification', '')),
                        feat.get('diameter_mm')
                    )
                    if feat_key not in seen_features:
                        all_features.append(feat)
                        seen_features.add(feat_key)
        
        merged['features'] = all_features
        
        # Merge material (prefer AI vision over OCR)
        for source in ['openai', 'gemini', 'ocr', 'cad_parser']:
            if source in self.results:
                material = self.results[source].get('material_on_drawing')
                if material:
                    merged['material_on_drawing'] = material
                    break
        
        # Merge part type (majority vote or highest confidence)
        part_types = {}
        for source in self.results:
            part_type = self.results[source].get('part_type')
            if part_type:
                if part_type not in part_types:
                    part_types[part_type] = 0
                part_types[part_type] += self.confidence_scores.get(source, 0.5)
        
        if part_types:
            merged['part_type'] = max(part_types.items(), key=lambda x: x[1])[0]
        
        # Merge confidence (weighted average)
        if self.confidence_scores:
            avg_confidence = sum(self.confidence_scores.values()) / len(self.confidence_scores)
            if avg_confidence >= 0.9:
                merged['confidence'] = 'high'
            elif avg_confidence >= 0.7:
                merged['confidence'] = 'medium'
            else:
                merged['confidence'] = 'low'
        
        # Merge tight tolerances (true if any source detects it)
        merged['has_tight_tolerances'] = any(
            self.results[source].get('has_tight_tolerances', False)
            for source in self.results
        )
        
        # Add collaboration metadata
        merged['collaboration'] = {
            'sources_agreed': len([s for s in self.results if s in priority_order]),
            'dimension_sources': {k: [v['source'] for v in all_dimensions.get(k, [])] for k in all_dimensions},
            'feature_count_by_source': {
                source: len(self.results[source].get('features', []))
                for source in self.results
            }
        }
        
        return merged
