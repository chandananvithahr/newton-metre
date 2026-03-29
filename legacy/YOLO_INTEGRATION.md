# YOLO Integration for Engineering Drawing Analysis

## Overview

YOLO (You Only Look Once) is integrated for object detection in engineering drawings, specifically for:
- GD&T symbol detection
- Dimension line/text detection
- Feature detection (holes, threads, chamfers, grooves)
- Tolerance symbol recognition

## Package Used

**ultralytics** - Modern YOLO implementation
- Supports YOLOv8, YOLOv9, YOLOv10
- Easy to use, well-maintained
- Can use pre-trained or custom models

## Installation

```bash
pip install ultralytics
```

## How It Works

### 1. **Pre-trained Model (Default)**
- Uses YOLOv8n (nano) - general purpose object detection
- Fast, lightweight
- Good for basic detection

### 2. **Custom Model (Recommended)**
- Train YOLO on engineering drawing dataset
- Detect specific symbols: GD&T, dimensions, features
- Much more accurate for engineering drawings

## Detection Classes

YOLO can detect:
- `dimension_line` - Dimension lines
- `dimension_text` - Dimension text/labels
- `gd_t_symbol` - GD&T symbols (tolerance callouts)
- `thread_symbol` - Thread representation symbols
- `hole` - Holes and bores
- `chamfer` - Chamfer symbols
- `groove` - Groove features
- `surface_finish` - Surface finish symbols
- `tolerance` - Tolerance annotations
- `material_callout` - Material specifications
- `title_block` - Drawing title blocks
- `center_line` - Center lines
- `hidden_line` - Hidden lines
- `section_line` - Section lines

## Integration Points

### 1. **Feature Detection**
- YOLO detects features → Merged with AI analysis
- Improves feature count accuracy
- Better thread/hole detection

### 2. **GD&T Symbol Detection**
- Detects tolerance symbols
- Automatically flags tight tolerances
- More reliable than AI text recognition

### 3. **Dimension Line Detection**
- Finds dimension lines in drawings
- Can extract dimension values with OCR
- Helps validate AI-extracted dimensions

## Usage in App

1. **Enable YOLO**: Checkbox in UI "Use YOLO for feature detection"
2. **Automatic**: Runs before AI analysis
3. **Combined Results**: YOLO features merged with AI results

## Training Custom Model

To train YOLO on engineering drawings:

1. **Prepare Dataset**:
   - Collect engineering drawings
   - Annotate with bounding boxes for symbols
   - Use tools like LabelImg or Roboflow

2. **Train Model**:
   ```python
   from ultralytics import YOLO
   model = YOLO('yolov8n.pt')
   model.train(data='drawing_dataset.yaml', epochs=100)
   ```

3. **Save Model**:
   - Save trained model to `models/drawing_detector.pt`
   - App will automatically use it

## Benefits

- **Accuracy**: Better feature detection than AI alone
- **Speed**: Fast object detection
- **Cost**: Free (runs locally)
- **Reliability**: Consistent symbol detection

## Limitations

- **Custom Training Required**: Pre-trained YOLO doesn't know engineering symbols
- **Annotation Needed**: Requires labeled dataset
- **Model Size**: Trained models can be large (50-200MB)

## Future Enhancements

- Pre-trained model for common GD&T symbols
- Real-time detection visualization
- Confidence threshold adjustment
- Multi-model ensemble (YOLO + AI)
