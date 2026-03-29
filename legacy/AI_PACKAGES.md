# AI Packages Used in Costimize

## Current AI Stack

### 1. **OpenAI** (`openai` package)
- **Model**: GPT-4o (GPT-4 Vision)
- **Purpose**: Primary vision AI for drawing analysis
- **Capabilities**:
  - Image understanding
  - Text extraction from drawings
  - Dimension recognition
  - Feature detection
- **API**: OpenAI Chat Completions API with vision
- **Cost**: Pay-per-use (varies by image size)
- **Location**: `vision.py` → `analyze_with_openai()`

### 2. **Google Generative AI** (`google-generativeai` package)
- **Model**: Gemini 2.0 Flash
- **Purpose**: Fallback vision AI
- **Capabilities**: Same as OpenAI
- **API**: Google Gemini Vision API
- **Cost**: Free tier available, then pay-per-use
- **Location**: `vision.py` → fallback in `_analyze_single_drawing()`

## Enhanced AI Stack (Optional)

### 3. **PaddleOCR** (`paddleocr` package)
- **Purpose**: Free, local OCR alternative
- **Capabilities**:
  - Text extraction from images
  - Dimension text recognition
  - Material callout detection
  - Multi-language support
- **Accuracy**: 85-90% on printed text
- **Cost**: FREE (runs locally, unlimited)
- **Location**: `ocr_extractor.py`
- **Use Case**: Fallback when AI APIs fail or for cost savings

### 4. **YOLO** (`ultralytics` package)
- **Model**: YOLOv8 (or custom trained model)
- **Purpose**: Object detection for engineering symbols
- **Capabilities**:
  - GD&T symbol detection
  - Dimension line/text detection
  - Feature detection (holes, threads, chamfers)
  - Tolerance symbol recognition
- **Accuracy**: 90-95% with custom training
- **Cost**: FREE (runs locally)
- **Location**: `yolo_detector.py`
- **Use Case**: Feature detection, GD&T symbols, tolerance recognition

## AI Workflow

```
User Uploads Drawing
    ↓
Check File Format
    ↓
┌─────────────────┬──────────────────┬─────────────────┐
│   Native CAD    │   Raster Image   │      PDF        │
│   (DXF, STL)    │   (PNG, JPG)     │                 │
└─────────────────┴──────────────────┴─────────────────┘
         ↓                  ↓                  ↓
    CAD Parser      AI Vision API      PDF → Images
    (100% acc)      (85-95% acc)            ↓
         ↓                  ↓          AI Vision API
    Direct Data      OpenAI GPT-4o
         ↓          (Primary)
    Use CAD Data     ↓ Failed?
         ↓          Gemini 2.0 Flash
    High Confidence  (Fallback)
         ↓          ↓ Failed?
         └──────────┴─→ PaddleOCR
                      (Free Fallback)
```

## Package Comparison

| Package | Accuracy | Cost | Speed | Format Support |
|---------|----------|------|-------|----------------|
| **OpenAI GPT-4o** | 90-95% | $$$ | Fast | Images |
| **Gemini 2.0 Flash** | 85-90% | $ | Fast | Images |
| **YOLO (custom)** | 90-95% | FREE | Fast | Images (objects) |
| **PaddleOCR** | 85-90% | FREE | Medium | Images (text) |
| **ezdxf (DXF)** | 100% | FREE | Very Fast | DXF files |
| **trimesh (STL)** | 100% | FREE | Very Fast | STL/OBJ/PLY |

## Recommended Strategy

### Priority Order:
1. **Native CAD Parsers** (if available) - 100% accurate, free
2. **YOLO Detection** - Feature/symbol detection (if enabled)
3. **OpenAI GPT-4o** - Best AI accuracy
4. **Gemini 2.0 Flash** - Good fallback
5. **PaddleOCR** - Free text extraction fallback

### Cost Optimization:
- Use CAD parsers when possible (free, accurate)
- Use YOLO for feature detection (free, fast)
- Use PaddleOCR for simple text extraction (free)
- Reserve AI APIs for complex analysis

## Installation

```bash
# Core AI packages
pip install openai google-generativeai

# Optional enhancements
pip install ultralytics              # YOLO object detection
pip install paddlepaddle paddleocr  # Free OCR
pip install ezdxf                    # DXF parsing
pip install trimesh                  # 3D mesh analysis
```

## API Keys Required

- `OPENAI_API_KEY` - For GPT-4o Vision
- `GOOGLE_API_KEY` - For Gemini 2.0 Flash
- No keys needed for: YOLO, PaddleOCR, ezdxf, trimesh (all local/free)
