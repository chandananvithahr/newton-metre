# Extraction Golden Dataset

Place drawing images here (PNG, 300+ DPI) alongside their expected JSON output.

## File naming convention

```
shaft_ss304.png          # Drawing image
shaft_ss304.json         # Expected extraction result (ground truth)

bracket_al6061.png
bracket_al6061.json

flange_en8.png
flange_en8.json
```

## JSON format

Must match `_ExtractionResult` schema from `extractors/vision.py`:

```json
{
  "part_type": "turning",
  "dimensions": {
    "outer_diameter_mm": 50.0,
    "inner_diameter_mm": null,
    "length_mm": 120.0,
    "width_mm": null,
    "height_mm": null,
    "hole_diameter_mm": 8.0,
    "hole_count": 4,
    "thread_count": 1,
    "thread_length_mm": 20.0,
    "groove_count": 2,
    "surface_area_cm2": null
  },
  "material": "SS304",
  "tolerances": {
    "has_tight_tolerances": true,
    "tightest_tolerance_mm": 0.02
  },
  "surface_finish": "Ra 1.6",
  "suggested_processes": ["turning", "facing", "drilling", "threading"],
  "confidence": "high",
  "notes": "Stepped shaft with keyway"
}
```

## How to create golden data

1. Extract with current cloud API (Gemini/GPT-4o)
2. Manually verify and correct every field
3. Save corrected JSON as ground truth
4. The training data logger (`evals/training_logger.py`) auto-saves these when users correct extractions
