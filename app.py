"""
Main Streamlit app for Costimize MVP
"""
import streamlit as st
import json
from pathlib import Path
from PIL import Image
from vision import analyze_drawing
from cost_engine import estimate_turning_cost
from material_price_fetcher import get_material_price, get_price_source_info

# Page configuration
st.set_page_config(
    page_title="Costimize - AI Manufacturing Cost Estimator",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, Professional CSS - Minimal and Functional
st.markdown("""
    <style>
    /* Clean, Minimal Design */
    .stApp {
        background: #ffffff;
    }
    
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Clean Typography */
    h1 {
        font-size: 2rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #374151;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: #4b5563;
    }
    
    /* Simple Cost Card */
    .cost-card {
        background: #f9fafb;
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        text-align: center;
        margin: 1.5rem 0;
    }
    
    .cost-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #111827;
        margin: 0.5rem 0;
    }
    
    /* Confidence Badges - Simple */
    .confidence-high {
        color: #059669;
        font-weight: 600;
        background: #d1fae5;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        display: inline-block;
    }
    
    .confidence-medium {
        color: #d97706;
        font-weight: 600;
        background: #fef3c7;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        display: inline-block;
    }
    
    .confidence-low {
        color: #dc2626;
        font-weight: 600;
        background: #fee2e2;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        display: inline-block;
    }
    
    /* Clean Inputs */
    .stNumberInput>div>div>input,
    .stTextInput>div>div>input,
    .stSelectbox>div>div {
        border-radius: 6px;
        border: 1px solid #d1d5db;
    }
    
    .stNumberInput>div>div>input:focus,
    .stTextInput>div>div>input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Simple Buttons */
    .stButton>button {
        border-radius: 6px;
        font-weight: 500;
        background: #3b82f6;
        color: white;
    }
    
    .stButton>button:hover {
        background: #2563eb;
    }
    
    /* Clean Metrics */
    [data-testid="stMetricContainer"] {
        background: #f9fafb;
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
    }
    
    /* Simple Expanders */
    .streamlit-expanderHeader {
        background: #f9fafb;
        border-radius: 6px;
        font-weight: 500;
    }
    
    /* Better Spacing */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* Clean Sidebar */
    [data-testid="stSidebar"] {
        background: #f9fafb;
    }
    </style>
""", unsafe_allow_html=True)

# Load materials database
@st.cache_data
def load_materials():
    """Load materials from JSON file."""
    materials_file = Path(__file__).parent / "sample_data" / "materials.json"
    try:
        with open(materials_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [mat['name'] for mat in data.get('materials', [])]
    except Exception as e:
        st.error(f"Failed to load materials: {e}")
        return []

# Load regions database
@st.cache_data
def load_regions():
    """Load regions from JSON file."""
    regions_file = Path(__file__).parent / "sample_data" / "regions.json"
    try:
        with open(regions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('regions', [])
    except Exception as e:
        st.error(f"Failed to load regions: {e}")
        return []

def get_region_by_code(regions, code):
    """Get region data by country code."""
    for region in regions:
        if region['code'] == code:
            return region
    # Default to India if not found
    return regions[0] if regions else None

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'manual_dimensions' not in st.session_state:
    st.session_state.manual_dimensions = {}
if 'use_manual_dimensions' not in st.session_state:
    st.session_state.use_manual_dimensions = False
if 'uploaded_pages' not in st.session_state:
    st.session_state.uploaded_pages = []
if 'selected_pages' not in st.session_state:
    st.session_state.selected_pages = []

# Clean Header
st.title("🏭 Costimize")
st.markdown("**AI-Powered Manufacturing Cost Estimator**")
st.markdown("---")

# Sidebar - Clean and Simple
with st.sidebar:
    st.header("Parameters")
    
    # Quantity input
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=10000,
        value=100,
        step=1,
        help="Number of pieces to manufacture"
    )
    
    # Material dropdown
    materials = load_materials()
    material_options = ["Auto-detect from drawing"] + materials
    selected_material = st.selectbox(
        "Material",
        options=material_options,
        help="Select material or let AI detect from drawing"
    )
    
    st.markdown("---")
    st.subheader("Region & Currency")
    regions = load_regions()
    if regions:
        region_options = [f"{r['name']} ({r['currency_symbol']} {r['currency']})" for r in regions]
        selected_region_index = st.selectbox(
            "Select Country/Region",
            options=range(len(regions)),
            format_func=lambda x: region_options[x],
            index=0,
            help="Select your country to get local pricing and currency"
        )
        selected_region = regions[selected_region_index]
        
        # Display region info
        col1, col2 = st.columns(2)
        with col1:
            st.caption(f"Currency: {selected_region['currency_symbol']} {selected_region['currency']}")
        with col2:
            st.caption(f"Default Machine Rate: {selected_region['currency_symbol']}{selected_region['machine_rate_per_hr']}/hr")
    else:
        selected_region = {
            "code": "IN",
            "name": "India",
            "currency": "INR",
            "currency_symbol": "₹",
            "machine_rate_per_hr": 800,
            "overhead_percent": 15,
            "profit_percent": 20
        }
        st.warning("⚠️ Region data not loaded. Using default (India)")
    
    # Machine rate override (now can use selected_region)
    st.subheader("Advanced Options")
    use_custom_rate = st.checkbox("Override machine rate")
    machine_rate = None
    if use_custom_rate:
        default_rate = selected_region.get('machine_rate_per_hr', 800)
        currency_symbol = selected_region.get('currency_symbol', '₹')
        machine_rate = st.number_input(
            f"Machine Rate ({currency_symbol}/hr)",
            min_value=1.0,
            max_value=10000.0,
            value=float(default_rate),
            step=1.0,
            help=f"Custom machine hour rate (default: {currency_symbol}{default_rate}/hr for {selected_region.get('name', 'selected region')})"
        )
    
    # Price source option
    use_live_prices = st.checkbox(
        "Use live web prices",
        value=True,
        help="Fetch current market prices from web (cached for 24 hours)"
    )
    
    if st.button("🔄 Refresh Material Prices", help="Force refresh prices from web"):
        from material_price_fetcher import refresh_all_prices
        with st.spinner("Refreshing prices from web..."):
            try:
                prices = refresh_all_prices(force=True)
                st.success(f"✅ Refreshed {len(prices)} material prices!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to refresh prices: {e}")
    
    # Display region-specific note
    if selected_region.get('name') != 'India':
        st.info(f"💡 **{selected_region.get('name')} Mode**: Prices converted to {selected_region.get('currency_symbol')} {selected_region.get('currency')} with regional adjustments for material costs and labor rates.")
    
    st.markdown("---")

# Main area - Clean and Simple
st.header("Upload Drawing")
st.caption("Supports: Images (PNG, JPG), PDFs, CAD files (DXF, STEP, STL, IGES)")

if st.session_state.get('chat_mode', True):
    st.info("💬 Chatbot mode active")

# File uploader - support multiple files
# Chatbot mode toggle
st.session_state.chat_mode = st.sidebar.checkbox(
    "💬 Chatbot Mode",
    value=st.session_state.get('chat_mode', False),
    help="Enable interactive chatbot for drawing analysis assistance"
)

uploaded_files = st.file_uploader(
    "Choose files (supports multiple files/pages)",
    type=['png', 'jpg', 'jpeg', 'pdf', 'dxf', 'stl', 'step', 'stp', 'iges', 'igs', 'obj', 'ply', 'fcstd', 'brep'],
    accept_multiple_files=True,
    help="Upload drawings in any format: Images (PNG/JPG), PDFs, or native CAD files (DXF, STL, STEP, IGES, OBJ, PLY, FCStd, BREP)"
)

if uploaded_files and len(uploaded_files) > 0:
    # Initialize chatbot if in chat mode
    if st.session_state.get('chat_mode', False):
        from chatbot_interface import DrawingAnalysisChatbot
        chatbot = DrawingAnalysisChatbot()
        chatbot.add_message("assistant", "👋 Hello! I'm here to help you analyze your engineering drawings and estimate manufacturing costs. Upload your drawing and I'll guide you through the process!")
    
    # Process all uploaded files
    all_pages = []
    page_info = []
    
    try:
        for file_idx, uploaded_file in enumerate(uploaded_files):
            file_type = uploaded_file.type
            file_name = uploaded_file.name
            file_ext = Path(file_name).suffix.lower()
            
            # Check if it's a native CAD file
            cad_formats = ['.dxf', '.stl', '.step', '.stp', '.iges', '.igs', '.obj', '.ply', '.brep', '.fcstd']
            if file_ext in cad_formats:
                # Save uploaded CAD file temporarily
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = Path(tmp_file.name)
                    uploaded_file.seek(0)  # Reset for potential reuse
                
                # Store file path for AI agent
                if 'uploaded_file_paths' not in st.session_state:
                    st.session_state.uploaded_file_paths = {}
                st.session_state.uploaded_file_paths[file_name] = tmp_path
                
                try:
                    # Try enhanced CAD parser first
                    from enhanced_cad_parser import parse_cad_file_enhanced
                    cad_result = parse_cad_file_enhanced(tmp_path)
                    
                    # Fallback to basic parser if enhanced fails
                    if "error" in cad_result:
                        try:
                            from cad_parser import parse_cad_file
                            cad_result = parse_cad_file(tmp_path)
                        except:
                            pass
                    
                    if "error" not in cad_result:
                        # Convert CAD result to image for display (if possible)
                        # For now, create a placeholder
                        st.success(f"✅ Parsed {file_name} ({cad_result.get('format', 'CAD')})")
                        
                        # Store CAD data
                        if 'cad_data' not in st.session_state:
                            st.session_state.cad_data = []
                        st.session_state.cad_data.append({
                            'file_name': file_name,
                            'data': cad_result,
                            'format': cad_result.get('format', 'CAD')
                        })
                        
                        # Use CAD data directly for cost calculation
                        if cad_result.get('dimensions'):
                            # Create a minimal analysis result from CAD data
                            analysis_from_cad = {
                                'part_type': 'turning' if cad_result['dimensions'].get('max_diameter_mm') else 'milling',
                                'dimensions': cad_result['dimensions'],
                                'features': cad_result.get('features', []),
                                'material_on_drawing': None,
                                'has_tight_tolerances': False,
                                'confidence': cad_result.get('confidence', 'high'),
                                'source': 'cad_parser',
                                'format': cad_result.get('format')
                            }
                            
                            # Merge with existing analysis or set as primary
                            if not st.session_state.analysis_result:
                                st.session_state.analysis_result = analysis_from_cad
                            else:
                                # Merge CAD data with AI analysis (CAD takes precedence for dimensions)
                                existing = st.session_state.analysis_result
                                existing['dimensions'].update(cad_result['dimensions'])
                                existing['confidence'] = 'high'  # CAD data is more reliable
                    else:
                        st.warning(f"⚠️ {cad_result.get('error', 'Could not parse CAD file')}")
                        # Fallback to image/AI analysis if CAD parsing fails
                        if file_ext in ['.stl', '.obj', '.ply']:
                            # Try to render 3D model as image
                            try:
                                from cad_parser import parse_stl_file
                                stl_result = parse_stl_file(tmp_path)
                                if "error" not in stl_result:
                                    st.info(f"📐 Extracted dimensions from {file_name}")
                            except:
                                pass
                
                except ImportError as e:
                    st.warning(f"⚠️ CAD parsing not available. Install: pip install ezdxf trimesh")
                    st.info("💡 Falling back to AI vision analysis (if image format)")
                except Exception as e:
                    st.error(f"❌ Error parsing CAD file {file_name}: {str(e)}")
                finally:
                    # Clean up temp file
                    try:
                        tmp_path.unlink()
                    except:
                        pass
            
            elif file_type == "application/pdf":
                # Extract PDF pages
                try:
                    from pdf_processor import extract_pdf_pages
                    pdf_pages = extract_pdf_pages(uploaded_file)
                    
                    if pdf_pages:
                        for page_idx, page_image in enumerate(pdf_pages):
                            all_pages.append(page_image)
                            page_info.append({
                                'file_name': file_name,
                                'page_number': page_idx + 1,
                                'total_pages': len(pdf_pages),
                                'type': 'PDF'
                            })
                        st.success(f"✅ Extracted {len(pdf_pages)} page(s) from {file_name}")
                    else:
                        st.warning(f"⚠️ Could not extract pages from {file_name}")
                except ImportError as e:
                    st.error(f"❌ PDF processing requires pdf2image. Install with: pip install pdf2image")
                    st.info("💡 For now, please convert PDF to images or install pdf2image and poppler")
                except Exception as e:
                    st.error(f"❌ Error processing PDF {file_name}: {str(e)}")
            else:
                # Process image files
                try:
                    image = Image.open(uploaded_file)
                    all_pages.append(image)
                    page_info.append({
                        'file_name': file_name,
                        'page_number': 1,
                        'total_pages': 1,
                        'type': 'Image'
                    })
                except Exception as e:
                    st.error(f"❌ Error processing image {file_name}: {str(e)}")
        
        if all_pages:
            st.session_state.uploaded_pages = all_pages
            st.session_state.page_info = page_info
            
            # Display pages
            st.subheader(f"📄 Uploaded Files ({len(all_pages)} page(s))")
            
            # Page selection for analysis
            if len(all_pages) > 1:
                st.info(f"📋 **Multiple pages detected:** Select which pages to analyze")
                selected_page_indices = st.multiselect(
                    "Select pages to analyze",
                    options=range(len(all_pages)),
                    default=list(range(len(all_pages))),  # Select all by default
                    format_func=lambda x: f"Page {x+1}: {page_info[x]['file_name']} (Page {page_info[x]['page_number']})"
                )
                if not selected_page_indices:
                    st.warning("⚠️ Please select at least one page to analyze")
                    st.stop()
                st.session_state.selected_pages = selected_page_indices
            else:
                st.session_state.selected_pages = [0]
            
            # Display selected pages in a grid
            pages_to_show = [all_pages[i] for i in st.session_state.selected_pages] if st.session_state.selected_pages else all_pages
            
            if not pages_to_show:
                st.error("❌ No pages selected for analysis")
                st.stop()
            
            if pages_to_show:
                cols = st.columns(min(3, len(pages_to_show)))
                for idx, (col, page_image) in enumerate(zip(cols[:len(pages_to_show)], pages_to_show)):
                    with col:
                        page_num = st.session_state.selected_pages[idx] if st.session_state.selected_pages else idx
                        info = page_info[page_num]
                        st.caption(f"Page {page_num + 1}: {info['file_name']}")
                        st.image(page_image, use_container_width=True)
                
                # Analyze selected pages
                st.subheader("🔍 Analysis Results")
                
                # Improved AI Agent - Production-ready with better accuracy
                with st.spinner("🤖 AI Agent: Running comprehensive analysis with all AI tools..."):
                    try:
                        from improved_ai_agent import ImprovedDrawingAnalysisAgent
                        agent = ImprovedDrawingAnalysisAgent()
                    except ImportError:
                        # Fallback to original agent
                        from ai_agent import DrawingAnalysisAgent
                        agent = DrawingAnalysisAgent()
                    
                    # Get file path if available (for CAD parsing)
                    file_path = None
                    if page_info and len(page_info) > 0:
                        # Try to get original file path from session state
                        if 'uploaded_file_paths' in st.session_state:
                            file_path = st.session_state.uploaded_file_paths.get(page_info[0]['file_name'])
                    
                    # Run comprehensive analysis - automatically uses all available tools
                    try:
                        analysis = agent.analyze_drawing_comprehensive(
                            pages_to_show[0],
                            file_path=file_path
                        )
                    except Exception as e:
                        st.error(f"❌ Analysis error: {str(e)}")
                        st.info("💡 **Try:**\n1. Upload CAD file (DXF/STEP) for accurate dimensions\n2. Use manual dimension input\n3. Ensure image is clear")
                        analysis = {"error": str(e)}
                    
                    # Store agent for later use
                    st.session_state.current_agent = agent
                    
                    # Display agent results
                    if 'agent_analysis' in analysis:
                        agent_info = analysis['agent_analysis']
                        tools_used = agent_info.get('tools_used', [])
                        if tools_used:
                            st.success(f"✅ AI Agent collaborated with {len(tools_used)} tools: {', '.join(tools_used)}")
                            
                            # Show validation warnings if any
                            if 'validation_notes' in analysis:
                                validation_notes = analysis['validation_notes']
                                if validation_notes:
                                    with st.expander("⚠️ Dimension Validation Warnings", expanded=True):
                                        for key, note in validation_notes.items():
                                            st.warning(f"**{key.replace('_', ' ').title()}**: {note}")
                                    
                                    if 'suggestions' in analysis:
                                        suggestions = analysis['suggestions']
                                        if suggestions:
                                            st.info("💡 **Suggestions**: " + "; ".join(suggestions.values()))
                            
                            with st.expander("🔍 View Agent Collaboration Details", expanded=False):
                                st.write("**Tools Used & Performance:**")
                                for tool in tools_used:
                                    conf = agent_info['confidence_scores'].get(tool, 0)
                                    time_taken = agent_info['execution_times'].get(tool, 0)
                                    st.write(f"  • **{tool}**: {conf*100:.0f}% confidence, {time_taken:.2f}s")
                                
                                # Show collaboration results if available
                                if 'collaboration' in analysis:
                                    collab = analysis['collaboration']
                                    st.write("**Collaboration Results:**")
                                    st.write(f"  • Sources that agreed: {collab.get('sources_agreed', 0)}")
                                    if 'feature_count_by_source' in collab:
                                        st.write("  • Features detected by each tool:")
                                        for source, count in collab['feature_count_by_source'].items():
                                            st.write(f"    - {source}: {count} features")
                                    
                                    # Show dimension sources
                                    if 'dimension_sources' in collab:
                                        st.write("**Dimension Sources:**")
                                        for dim, sources in collab['dimension_sources'].items():
                                            st.write(f"  • {dim}: from {', '.join(sources)}")
                
                # Chatbot interface if enabled
                if st.session_state.get('chat_mode', False):
                    from chatbot_interface import DrawingAnalysisChatbot
                    chatbot = DrawingAnalysisChatbot()
                    
                    # Display chat history
                    st.subheader("💬 Analysis Chat")
                    for msg in st.session_state.chat_history[-10:]:  # Show last 10 messages
                        with st.chat_message(msg['role']):
                            st.markdown(msg['content'])
                    
                    # User input for questions
                    user_question = st.chat_input("Ask me anything about the drawing analysis...")
                    if user_question:
                        chatbot.add_message("user", user_question)
                        response = chatbot.handle_user_question(user_question)
                        chatbot.add_message("assistant", response)
                        st.rerun()
                
                # Check for errors (only if not in chatbot mode, chatbot handles errors)
                if "error" in analysis and not st.session_state.get('chat_mode', False):
                    error_msg = analysis['error']
                    st.error(f"❌ Analysis Error: {error_msg}")
                    
                    # Check if it's an API key error
                    if "API key" in error_msg or "api_key" in error_msg.lower():
                        st.error("🔑 **API Error:** Please check your API keys in the .env file. Make sure OPENAI_API_KEY or GOOGLE_API_KEY is set correctly.")
                    elif "API" in error_msg:
                        st.warning("⚠️ **API Error:** The AI service may be temporarily unavailable. Please try again or use manual dimension input below.")
                    
                    if "raw_response" in analysis:
                        with st.expander("View raw response"):
                            st.text(analysis['raw_response'])
                    
                    # Set analysis result to None so we can use manual input
                    st.session_state.analysis_result = None
                else:
                    st.session_state.analysis_result = analysis
                    st.session_state.use_manual_dimensions = False
                    
                    # Display extracted data
                    pages_analyzed = analysis.get('pages_analyzed', len(pages_to_show))
                    if pages_analyzed > 1:
                        st.success(f"✅ Successfully analyzed {pages_analyzed} page(s) and combined results!")
                    else:
                        st.success("✅ Drawing analyzed successfully!")
                    
                    # Part type
                    part_type = analysis.get('part_type', 'unknown')
                    part_type_emoji = "🔄" if part_type == "turning" else "⚙️" if part_type == "milling" else "❓"
                    st.markdown(f"**Part Type:** {part_type_emoji} {part_type.title()}")
                    
                    # Dimensions with accuracy warnings
                    st.markdown("**Dimensions:**")
                    dims = analysis.get('dimensions', {})
                    
                    # Check dimension source and show warnings
                    dim_sources = []
                    if 'collaboration' in analysis and 'dimension_sources' in analysis['collaboration']:
                        dim_sources = set([s for sources in analysis['collaboration']['dimension_sources'].values() for s in sources])
                    
                    # Warn if dimensions are only from AI (not accurate)
                    if dim_sources and not any(s in ['cad_parser', 'ocr'] for s in dim_sources):
                        st.error("❌ **WARNING**: Dimensions extracted only from AI vision interpretation - **NOT ACCURATE**. For accurate dimensions:")
                        st.markdown("""
                        - ✅ **Upload CAD file** (DXF, STEP, STL) - 100% accurate
                        - ✅ **Ensure dimensions are written as text** on drawing - OCR will read them
                        - ✅ **Use manual input** below to enter exact dimensions
                        """)
                    elif 'cad_parser' in dim_sources:
                        st.success("✅ Dimensions from CAD file - **100% accurate**")
                    elif 'ocr' in dim_sources:
                        st.info("ℹ️ Dimensions from text reading - **85-90% accurate** (verify if unclear)")
                    
                    if dims.get('max_diameter_mm'):
                        st.write(f"  • Max Diameter: **{dims['max_diameter_mm']} mm**")
                    if dims.get('inner_diameter_mm'):
                        st.write(f"  • Inner Diameter: **{dims['inner_diameter_mm']} mm**")
                    if dims.get('length_mm'):
                        st.write(f"  • Length: **{dims['length_mm']} mm**")
                    if dims.get('width_mm'):
                        st.write(f"  • Width: **{dims['width_mm']} mm**")
                    if dims.get('height_mm'):
                        st.write(f"  • Height: **{dims['height_mm']} mm**")
                    
                    # Show dimension sources
                    if dim_sources:
                        st.caption(f"📊 Dimension sources: {', '.join(dim_sources)}")
                    
                    # Material detected
                    material_detected = analysis.get('material_on_drawing')
                    if material_detected:
                        st.markdown(f"**Material on Drawing:** {material_detected}")
                    else:
                        st.markdown("**Material on Drawing:** Not specified")
                    
                    # Features
                    features = analysis.get('features', [])
                    if features:
                        st.markdown(f"**Features Identified:** {len(features)}")
                        for feat in features[:5]:  # Show first 5
                            feat_type = feat.get('type', 'unknown')
                            feat_spec = feat.get('specification') or feat.get('diameter_mm')
                            if feat_spec:
                                st.write(f"  • {feat_type.title()}: {feat_spec}")
                    
                    # Surface finish
                    surface_finish = analysis.get('surface_finish_ra')
                    if surface_finish:
                        st.markdown(f"**Surface Finish:** Ra {surface_finish} μm")
                    
                    # Confidence level
                    confidence = analysis.get('confidence', 'unknown')
                    confidence_class = {
                        'high': 'confidence-high',
                        'medium': 'confidence-medium',
                        'low': 'confidence-low'
                    }.get(confidence, '')
                    st.markdown(f"**Confidence:** <span class='{confidence_class}'>{confidence.upper()}</span>", unsafe_allow_html=True)
                    
                    # Pages analyzed info
                    if pages_analyzed > 1:
                        st.info(f"📄 Analysis combined from {pages_analyzed} page(s)")
                    
                    # YOLO detection info
                    if analysis.get('yolo_detections'):
                        st.success(f"🎯 YOLO detected {analysis.get('yolo_detections')} feature(s)")
                    
                    # Tight tolerances
                    if analysis.get('has_tight_tolerances'):
                        st.warning("⚠️ Tight tolerances detected (< ±0.05mm) - 30% surcharge applied")
                    
                    # Show YOLO detections if available (YOLO runs automatically via AI Agent)
                    agent_info = analysis.get('agent_analysis', {})
                    if pages_to_show and 'yolo' in agent_info.get('tools_used', []):
                        try:
                            # Get YOLO result from agent if available
                            current_agent = st.session_state.get('current_agent')
                            if current_agent and hasattr(current_agent, 'results') and 'yolo' in current_agent.results:
                                yolo_result = current_agent.results['yolo']
                                if yolo_result.get('detections'):
                                    from yolo_detector import create_annotated_image
                                    with st.expander("🎯 View YOLO Detections", expanded=False):
                                        st.write(f"**Total detections:** {yolo_result.get('total_detections', 0)}")
                                        
                                        # Show grouped detections
                                        grouped = yolo_result.get('grouped', {})
                                        if grouped:
                                            st.write("**Detected elements:**")
                                            for cls, dets in grouped.items():
                                                st.write(f"  • {cls}: {len(dets)}")
                                        
                                        # Show annotated image
                                        annotated = create_annotated_image(pages_to_show[0], yolo_result.get('detections', []))
                                        st.image(annotated, caption="YOLO Detection Results (red boxes)", use_container_width=True)
                        except Exception as e:
                            # Silently fail - YOLO visualization is optional
                            pass
            
            # Manual dimension input fallback
            dims = {}
            if st.session_state.analysis_result:
                dims = st.session_state.analysis_result.get('dimensions', {})
            
            # Check if dimensions are missing or invalid
            has_valid_dimensions = (
                dims.get('max_diameter_mm') and dims.get('max_diameter_mm') > 0 and
                dims.get('length_mm') and dims.get('length_mm') > 0
            )
            
            if not has_valid_dimensions:
                st.warning("⚠️ **Could not extract dimensions from drawing. Please enter manually:**")
                with st.expander("📏 Manual Dimension Input", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        manual_od = st.number_input(
                            "Max Diameter (OD) [mm]",
                            min_value=0.0,
                            value=float(st.session_state.manual_dimensions.get('max_diameter_mm', 0)),
                            step=0.1,
                            key="manual_od"
                        )
                        manual_id = st.number_input(
                            "Inner Diameter (ID) [mm]",
                            min_value=0.0,
                            value=float(st.session_state.manual_dimensions.get('inner_diameter_mm', 0)),
                            step=0.1,
                            key="manual_id",
                            help="Enter 0 for solid parts"
                        )
                    with col2:
                        manual_length = st.number_input(
                            "Length [mm]",
                            min_value=0.0,
                            value=float(st.session_state.manual_dimensions.get('length_mm', 0)),
                            step=0.1,
                            key="manual_length"
                        )
                        manual_width = st.number_input(
                            "Width [mm] (for milling)",
                            min_value=0.0,
                            value=float(st.session_state.manual_dimensions.get('width_mm', 0)),
                            step=0.1,
                            key="manual_width"
                        )
                    with col3:
                        manual_height = st.number_input(
                            "Height [mm] (for milling)",
                            min_value=0.0,
                            value=float(st.session_state.manual_dimensions.get('height_mm', 0)),
                            step=0.1,
                            key="manual_height"
                        )
                    
                    if st.button("✅ Use Manual Dimensions"):
                        st.session_state.manual_dimensions = {
                            'max_diameter_mm': manual_od if manual_od > 0 else None,
                            'inner_diameter_mm': manual_id if manual_id > 0 else None,
                            'length_mm': manual_length,
                            'width_mm': manual_width if manual_width > 0 else None,
                            'height_mm': manual_height if manual_height > 0 else None
                        }
                        st.session_state.use_manual_dimensions = True
                        st.success("✅ Manual dimensions saved!")
                        st.rerun()
                
                # Use manual dimensions if available
                if st.session_state.use_manual_dimensions and st.session_state.manual_dimensions:
                    dims = st.session_state.manual_dimensions
                    if not st.session_state.analysis_result:
                        # Create a minimal analysis result for cost calculation
                        st.session_state.analysis_result = {
                            'part_type': 'turning',
                            'dimensions': dims,
                            'features': [],
                            'has_tight_tolerances': False,
                            'confidence': 'manual'
                        }
            
            # Cost Estimate Section
            if (st.session_state.analysis_result and "error" not in st.session_state.analysis_result) or st.session_state.use_manual_dimensions:
                st.markdown("---")
                st.header("💰 Cost Estimate")
                
                # Determine material to use
                material_to_use = None
                if selected_material != "Auto-detect from drawing":
                    material_to_use = selected_material
                else:
                    # Try to match detected material
                    analysis_data = st.session_state.analysis_result or {}
                    detected_material = analysis_data.get('material_on_drawing', '')
                    if detected_material:
                        # Try to find matching material in database
                        for mat in materials:
                            if mat.lower() in detected_material.lower() or detected_material.lower() in mat.lower():
                                material_to_use = mat
                                break
                    
                    # Default to first material if no match
                    if not material_to_use and materials:
                        material_to_use = materials[0]
                        st.info(f"⚠️ Using default material: {material_to_use}")
                
                if material_to_use:
                    # Get dimensions - use manual if available, otherwise from analysis
                    if st.session_state.use_manual_dimensions:
                        dimensions_to_use = st.session_state.manual_dimensions
                        has_tight_tolerances = st.checkbox("Has tight tolerances (< ±0.05mm)", value=False)
                        features_to_use = []
                    else:
                        dimensions_to_use = st.session_state.analysis_result.get('dimensions', {})
                        has_tight_tolerances = st.session_state.analysis_result.get('has_tight_tolerances', False)
                        features_to_use = st.session_state.analysis_result.get('features', [])
                    
                    # Validate dimensions before calculating
                    if not dimensions_to_use.get('max_diameter_mm') or not dimensions_to_use.get('length_mm'):
                        st.error("❌ **Missing required dimensions:** Please provide Max Diameter (OD) and Length to calculate cost.")
                    else:
                        # Calculate cost
                        try:
                            cost_result = estimate_turning_cost(
                                dimensions=dimensions_to_use,
                                material_type=material_to_use,
                                quantity=quantity,
                                has_tight_tolerances=has_tight_tolerances,
                                features=features_to_use,
                                machine_hour_rate=machine_rate,
                                use_live_prices=use_live_prices,
                                region=selected_region
                            )
                        
                            if "error" in cost_result:
                                st.error(f"❌ Cost Calculation Error: {cost_result['error']}")
                            else:
                                # Display cost in card format with region currency
                                currency_symbol = selected_region.get('currency_symbol', '₹')
                                st.markdown("""
                                <div class="cost-card">
                                    <div style="font-size: 1rem; color: #6b7280; margin-bottom: 0.5rem;">Cost Per Piece</div>
                                    <div class="cost-value">{symbol}{:.2f}</div>
                                    <div style="font-size: 0.9rem; color: #6b7280; margin-top: 0.5rem;">Total ({quantity} pieces): {symbol}{total:.2f}</div>
                                </div>
                                """.format(
                                    cost_result['cost_per_piece'],
                                    quantity=quantity,
                                    total=cost_result['total_cost'],
                                    symbol=currency_symbol
                                ), unsafe_allow_html=True)
                                
                                # Expandable breakdown
                                with st.expander("📊 Detailed Cost Breakdown", expanded=False):
                                    breakdown = cost_result.get('breakdown', {})
                                    
                                    # Material breakdown
                                    st.subheader("📦 Material Cost")
                                    mat_breakdown = breakdown.get('material', {})
                                    col1, col2, col3 = st.columns(3)
                                    currency_symbol = selected_region.get('currency_symbol', '₹')
                                    with col1:
                                        st.metric("Weight (with wastage)", f"{mat_breakdown.get('weight_with_wastage_kg', 0):.3f} kg")
                                    with col2:
                                        price_per_kg = mat_breakdown.get('price_per_kg_inr', 0)
                                        try:
                                            price_source = get_price_source_info(material_to_use)
                                            st.metric("Price per kg", f"{currency_symbol}{price_per_kg:.2f}", help=f"Source: {price_source}")
                                        except:
                                            st.metric("Price per kg", f"{currency_symbol}{price_per_kg:.2f}")
                                    with col3:
                                        st.metric("Material Cost", f"{currency_symbol}{cost_result['material_cost']:.2f}")
                                    
                                    st.markdown("---")
                                    
                                    # Machining breakdown
                                    st.subheader("⚙️ Machining Cost")
                                    mach_breakdown = breakdown.get('machining', {})
                                    col1, col2, col3 = st.columns(3)
                                    currency_symbol = selected_region.get('currency_symbol', '₹')
                                    with col1:
                                        st.metric("Total Time", f"{cost_result['machining_time_min']:.2f} min")
                                    with col2:
                                        st.metric("Machine Rate", f"{currency_symbol}{mach_breakdown.get('machine_rate_per_hr', 0)}/hr")
                                    with col3:
                                        st.metric("Machining Cost", f"{currency_symbol}{cost_result['machining_cost']:.2f}")
                                    
                                    st.write("**Time Breakdown:**")
                                    st.write(f"  • Base time: {mach_breakdown.get('base_time_min', 0):.2f} min")
                                    st.write(f"  • Facing: {mach_breakdown.get('facing_time_min', 0):.2f} min")
                                    st.write(f"  • Roughing: {mach_breakdown.get('roughing_time_min', 0):.2f} min")
                                    st.write(f"  • Finishing: {mach_breakdown.get('finishing_time_min', 0):.2f} min")
                                    st.write(f"  • Boring: {mach_breakdown.get('boring_time_min', 0):.2f} min")
                                    st.write(f"  • Features: {mach_breakdown.get('feature_time_min', 0):.2f} min")
                                    st.write(f"  • Parting: {mach_breakdown.get('parting_time_min', 0):.2f} min")
                                    
                                    currency_symbol = selected_region.get('currency_symbol', '₹')
                                    st.metric("Setup Cost (amortized)", f"{currency_symbol}{cost_result['setup_cost_per_piece']:.2f}")
                                    
                                    st.markdown("---")
                                    
                                    # Pricing breakdown
                                    st.subheader("💵 Pricing Breakdown")
                                    pricing = breakdown.get('pricing', {})
                                    currency_symbol = selected_region.get('currency_symbol', '₹')
                                    overhead_pct = selected_region.get('overhead_percent', 15)
                                    profit_pct = selected_region.get('profit_percent', 20)
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        st.metric("Base Cost", f"{currency_symbol}{pricing.get('base_cost_per_piece', 0):.2f}")
                                    with col2:
                                        st.metric(f"Overhead ({overhead_pct}%)", f"{currency_symbol}{cost_result['overhead']:.2f}")
                                    with col3:
                                        st.metric(f"Profit ({profit_pct}%)", f"{currency_symbol}{cost_result['profit']:.2f}")
                                
                                # DFM Analysis (aPriori-inspired)
                                st.markdown("---")
                                st.subheader("🔧 Design for Manufacturability (DFM) Analysis")
                                
                                try:
                                    from dfm_analyzer import DFMAnalyzer
                                    dfm_analyzer = DFMAnalyzer()
                                    dfm_result = dfm_analyzer.analyze_dfm(analysis, cost_result)
                                    
                                    # DFM Score
                                    dfm_score = dfm_result.get('dfm_score', 0)
                                    manufacturability = dfm_result.get('manufacturability', 'unknown')
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        if dfm_score >= 80:
                                            st.success(f"✅ **DFM Score: {dfm_score:.0f}/100** - Good manufacturability")
                                        elif dfm_score >= 60:
                                            st.warning(f"⚠️ **DFM Score: {dfm_score:.0f}/100** - Needs attention")
                                        else:
                                            st.error(f"❌ **DFM Score: {dfm_score:.0f}/100** - Significant issues")
                                    
                                    with col2:
                                        if manufacturability == 'good':
                                            st.success("✅ Manufacturability: Good")
                                        else:
                                            st.warning("⚠️ Manufacturability: Needs Attention")
                                    
                                    # Cost Drivers
                                    cost_drivers = dfm_result.get('cost_drivers', [])
                                    if cost_drivers:
                                        st.markdown("**💰 Cost Drivers:**")
                                        for driver in cost_drivers:
                                            st.write(f"  • **{driver['feature']}**: {driver['percentage']:.1f}% of total cost")
                                            if 'recommendation' in driver:
                                                st.caption(f"    💡 {driver['recommendation']}")
                                    
                                    # Issues
                                    issues = dfm_result.get('issues', [])
                                    if issues:
                                        with st.expander(f"⚠️ Manufacturability Issues ({len(issues)})", expanded=True):
                                            for issue in issues:
                                                severity_icon = "🔴" if issue['severity'] == 'high' else "🟡"
                                                st.markdown(f"{severity_icon} **{issue['type'].replace('_', ' ').title()}**")
                                                st.write(f"  • {issue['message']}")
                                                st.write(f"  • Cost Impact: {issue['cost_impact']}")
                                                st.write(f"  • Recommendation: {issue['recommendation']}")
                                                st.markdown("---")
                                    
                                    # Recommendations
                                    recommendations = dfm_result.get('recommendations', [])
                                    if recommendations:
                                        st.info("💡 **Recommendations:**\n" + "\n".join(f"  • {r}" for r in recommendations))
                                    
                                except Exception as e:
                                    st.caption(f"DFM analysis unavailable: {str(e)}")
                                
                                # Similarity Search (CADDi-inspired)
                                if st.session_state.get('analysis_result'):
                                    st.markdown("---")
                                    st.subheader("🔍 Similar Parts Search")
                                    st.info("💡 Find similar parts from your history to reuse designs and pricing")
                                    
                                    if st.button("🔎 Find Similar Parts", use_container_width=True):
                                        try:
                                            from similarity_search import DrawingSimilaritySearch
                                            similarity_search = DrawingSimilaritySearch()
                                            
                                            # For now, show placeholder
                                            st.info("📊 Similarity search feature - Coming soon! This will help you:")
                                            st.markdown("""
                                            - Find similar parts from your history
                                            - Reuse previous cost estimates
                                            - Identify design patterns
                                            - Reduce duplicate designs
                                            """)
                                        except:
                                            st.info("Similarity search feature coming soon!")
                                
                                # DFM Analysis (aPriori-inspired)
                                st.markdown("---")
                                st.subheader("🔧 Design for Manufacturability (DFM) Analysis")
                                
                                try:
                                    from dfm_analyzer import DFMAnalyzer
                                    dfm_analyzer = DFMAnalyzer()
                                    dfm_result = dfm_analyzer.analyze_dfm(st.session_state.analysis_result or {}, cost_result)
                                    
                                    # DFM Score
                                    dfm_score = dfm_result.get('dfm_score', 0)
                                    manufacturability = dfm_result.get('manufacturability', 'unknown')
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        if dfm_score >= 80:
                                            st.success(f"✅ **DFM Score: {dfm_score:.0f}/100** - Good manufacturability")
                                        elif dfm_score >= 60:
                                            st.warning(f"⚠️ **DFM Score: {dfm_score:.0f}/100** - Needs attention")
                                        else:
                                            st.error(f"❌ **DFM Score: {dfm_score:.0f}/100** - Significant issues")
                                    
                                    with col2:
                                        if manufacturability == 'good':
                                            st.success("✅ Manufacturability: Good")
                                        else:
                                            st.warning("⚠️ Manufacturability: Needs Attention")
                                    
                                    # Cost Drivers
                                    cost_drivers = dfm_result.get('cost_drivers', [])
                                    if cost_drivers:
                                        st.markdown("**💰 Cost Drivers:**")
                                        for driver in cost_drivers:
                                            pct = driver.get('percentage', 0)
                                            st.write(f"  • **{driver['feature']}**: {pct:.1f}% of total cost ({currency_symbol}{driver.get('cost_impact', 0):.2f})")
                                            if 'recommendation' in driver:
                                                st.caption(f"    💡 {driver['recommendation']}")
                                    
                                    # Issues
                                    issues = dfm_result.get('issues', [])
                                    if issues:
                                        with st.expander(f"⚠️ Manufacturability Issues ({len(issues)})", expanded=True):
                                            for issue in issues:
                                                severity_icon = "🔴" if issue['severity'] == 'high' else "🟡"
                                                st.markdown(f"{severity_icon} **{issue['type'].replace('_', ' ').title()}**")
                                                st.write(f"  • {issue['message']}")
                                                st.write(f"  • Cost Impact: {issue['cost_impact']}")
                                                st.write(f"  • Recommendation: {issue['recommendation']}")
                                                st.markdown("---")
                                    
                                    # Recommendations
                                    recommendations = dfm_result.get('recommendations', [])
                                    if recommendations:
                                        st.info("💡 **Recommendations:**\n" + "\n".join(f"  • {r}" for r in recommendations))
                                    
                                except Exception as e:
                                    st.caption(f"DFM analysis unavailable: {str(e)}")
                                
                                # Similarity Search (CADDi-inspired)
                                st.markdown("---")
                                st.subheader("🔍 Similar Parts Search")
                                st.info("💡 Find similar parts from your history to reuse designs and pricing")
                                
                                if st.button("🔎 Find Similar Parts", use_container_width=True):
                                    try:
                                        from similarity_search import DrawingSimilaritySearch
                                        similarity_search = DrawingSimilaritySearch()
                                        
                                        # For now, show placeholder with future features
                                        st.success("📊 Similarity search feature - Coming soon!")
                                        st.markdown("""
                                        **This will help you:**
                                        - ✅ Find similar parts from your history
                                        - ✅ Reuse previous cost estimates
                                        - ✅ Identify design patterns
                                        - ✅ Reduce duplicate designs
                                        - ✅ Access historical pricing data
                                        """)
                                    except Exception as e:
                                        st.info(f"Similarity search feature coming soon! ({str(e)})")
                                
                                # Download Quote PDF button
                                st.markdown("---")
                                if st.button("📥 Download Quote PDF", use_container_width=True):
                                    st.info("📄 PDF generation feature coming soon!")
                        except Exception as e:
                            st.error(f"❌ Error calculating cost: {str(e)}")
                            import traceback
                            with st.expander("Technical Details"):
                                st.code(traceback.format_exc())
                else:
                    st.error("❌ No material selected. Please select a material from the sidebar.")
        
    except Exception as e:
        st.error(f"❌ Error processing files: {str(e)}")
        import traceback
        with st.expander("Technical Details"):
            st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer-note">
        <strong>⚠️ Note:</strong> This is an AI-assisted estimate. Actual costs may vary ±15-20% based on shop rates, 
        material availability, and specific manufacturing requirements. Always consult with your manufacturing partner 
        for final pricing.
    </div>
""", unsafe_allow_html=True)
