"""
Chatbot-like interface for interactive drawing analysis
Provides conversational assistance for cost estimation
"""
import streamlit as st
from typing import Dict, List, Optional
from pathlib import Path
from PIL import Image

class DrawingAnalysisChatbot:
    """Chatbot interface for drawing analysis assistance."""
    
    def __init__(self):
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'current_analysis' not in st.session_state:
            st.session_state.current_analysis = None
        if 'chat_mode' not in st.session_state:
            st.session_state.chat_mode = False
    
    def add_message(self, role: str, content: str, data: Optional[Dict] = None):
        """Add message to chat history."""
        st.session_state.chat_history.append({
            'role': role,
            'content': content,
            'data': data
        })
    
    def analyze_and_chat(self, image: Image.Image, file_name: str = "drawing") -> Dict:
        """Analyze drawing and provide conversational feedback."""
        self.add_message("assistant", f"🔍 Analyzing your drawing: {file_name}...")
        
        try:
            # Try CAD parsing first
            cad_result = None
            try:
                from enhanced_cad_parser import parse_cad_file_enhanced
                # Note: This would need the file saved temporarily
                # For now, we'll use vision analysis
                pass
            except:
                pass
            
            # Use vision AI
            from vision import analyze_drawing
            analysis = analyze_drawing(image)
            
            if "error" in analysis:
                self.add_message("assistant", f"❌ I encountered an issue: {analysis['error']}")
                self.add_message("assistant", "💡 Would you like to:\n1. Try uploading in a different format?\n2. Enter dimensions manually?\n3. Get help with the error?")
                return analysis
            
            # Provide conversational analysis
            self.add_message("assistant", "✅ Analysis complete! Let me tell you what I found:")
            
            # Part type
            part_type = analysis.get('part_type', 'unknown')
            part_emoji = "🔄" if part_type == "turning" else "⚙️" if part_type == "milling" else "❓"
            self.add_message("assistant", f"{part_emoji} **Part Type**: This appears to be a {part_type} part.")
            
            # Dimensions
            dims = analysis.get('dimensions', {})
            dim_text = "📐 **Dimensions I found**:\n"
            if dims.get('max_diameter_mm'):
                dim_text += f"  • Outer Diameter: {dims['max_diameter_mm']} mm\n"
            if dims.get('inner_diameter_mm'):
                dim_text += f"  • Inner Diameter: {dims['inner_diameter_mm']} mm\n"
            if dims.get('length_mm'):
                dim_text += f"  • Length: {dims['length_mm']} mm\n"
            if dims.get('width_mm'):
                dim_text += f"  • Width: {dims['width_mm']} mm\n"
            if dims.get('height_mm'):
                dim_text += f"  • Height: {dims['height_mm']} mm\n"
            
            if dim_text != "📐 **Dimensions I found**:\n":
                self.add_message("assistant", dim_text)
            else:
                self.add_message("assistant", "⚠️ I couldn't extract dimensions clearly. Could you help me by confirming the dimensions?")
            
            # Material
            material = analysis.get('material_on_drawing')
            if material:
                self.add_message("assistant", f"🔩 **Material**: I see {material} specified on the drawing.")
            else:
                self.add_message("assistant", "🔩 **Material**: I couldn't find a material specification. Please select one from the sidebar.")
            
            # Features
            features = analysis.get('features', [])
            if features:
                feat_text = f"⚙️ **Features detected**: I found {len(features)} feature(s):\n"
                for feat in features[:5]:
                    feat_type = feat.get('type', 'unknown')
                    feat_spec = feat.get('specification') or feat.get('diameter_mm')
                    if feat_spec:
                        feat_text += f"  • {feat_type.title()}: {feat_spec}\n"
                self.add_message("assistant", feat_text)
            
            # Confidence
            confidence = analysis.get('confidence', 'unknown')
            if confidence == 'high':
                self.add_message("assistant", "✅ I'm confident about this analysis!")
            elif confidence == 'medium':
                self.add_message("assistant", "⚠️ I'm moderately confident. Please review the results.")
            else:
                self.add_message("assistant", "⚠️ I'm not very confident. Please verify the dimensions manually.")
            
            # Store analysis
            st.session_state.current_analysis = analysis
            
            # Offer next steps
            self.add_message("assistant", "💡 **What would you like to do next?**\n1. Get a cost estimate\n2. Adjust any dimensions\n3. Ask questions about the analysis")
            
            return analysis
            
        except Exception as e:
            self.add_message("assistant", f"❌ Oops! Something went wrong: {str(e)}")
            self.add_message("assistant", "💡 Please try:\n- Uploading the file again\n- Using a different format (PNG, JPG, DXF, STL)\n- Contacting support if the issue persists")
            return {"error": str(e)}
    
    def handle_user_question(self, question: str) -> str:
        """Handle user questions about the analysis."""
        question_lower = question.lower()
        
        # Check if analysis exists
        if not st.session_state.current_analysis:
            return "I haven't analyzed a drawing yet. Please upload a drawing first!"
        
        analysis = st.session_state.current_analysis
        
        # Answer common questions
        if "dimension" in question_lower or "size" in question_lower:
            dims = analysis.get('dimensions', {})
            response = "Here are the dimensions I found:\n"
            for key, value in dims.items():
                if value:
                    response += f"  • {key.replace('_', ' ').title()}: {value} mm\n"
            return response
        
        elif "material" in question_lower:
            material = analysis.get('material_on_drawing')
            if material:
                return f"I found the material specification: {material}"
            else:
                return "I couldn't find a material specification on the drawing. Please select one from the sidebar."
        
        elif "feature" in question_lower or "hole" in question_lower or "thread" in question_lower:
            features = analysis.get('features', [])
            if features:
                response = f"I detected {len(features)} feature(s):\n"
                for feat in features:
                    response += f"  • {feat.get('type', 'unknown')}\n"
                return response
            else:
                return "I didn't detect any specific features. The part might be simple, or the features weren't clearly visible."
        
        elif "cost" in question_lower or "price" in question_lower or "estimate" in question_lower:
            return "To get a cost estimate, please:\n1. Select a material from the sidebar\n2. Enter the quantity\n3. The cost will be calculated automatically below"
        
        elif "confidence" in question_lower or "accurate" in question_lower:
            confidence = analysis.get('confidence', 'unknown')
            if confidence == 'high':
                return "I'm highly confident in this analysis. The drawing was clear and I could extract all the key information."
            elif confidence == 'medium':
                return "I'm moderately confident. Some information might need verification. Please review the extracted dimensions."
            else:
                return "I'm not very confident. The drawing might be unclear or in an unsupported format. Please verify the dimensions manually."
        
        else:
            return "I understand you're asking about the drawing. Could you be more specific? I can help with:\n- Dimensions\n- Material\n- Features\n- Cost estimation\n- Analysis confidence"
