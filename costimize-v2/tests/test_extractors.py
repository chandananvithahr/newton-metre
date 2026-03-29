from extractors.process_detector import detect_processes_from_extraction


def test_detect_from_ai_suggestions():
    extraction = {"part_type": "turning", "suggested_processes": ["turning", "facing", "drilling", "threading"]}
    result = detect_processes_from_extraction(extraction)
    assert result == ["turning", "facing", "drilling", "threading"]


def test_fallback_turning_part():
    extraction = {"part_type": "turning", "dimensions": {"outer_diameter_mm": 60, "length_mm": 100}}
    result = detect_processes_from_extraction(extraction)
    assert "turning" in result
    assert "facing" in result


def test_fallback_with_holes_and_threads():
    extraction = {"part_type": "turning", "dimensions": {"outer_diameter_mm": 60, "length_mm": 100, "hole_count": 4, "thread_count": 2}}
    result = detect_processes_from_extraction(extraction)
    assert "drilling" in result
    assert "threading" in result


def test_fallback_milling_part():
    extraction = {"part_type": "milling", "dimensions": {"length_mm": 100, "width_mm": 50, "height_mm": 30}}
    result = detect_processes_from_extraction(extraction)
    assert "milling_face" in result


def test_fallback_fine_surface_finish():
    extraction = {"part_type": "turning", "dimensions": {"outer_diameter_mm": 60, "length_mm": 100}, "surface_finish": "Ra 0.4"}
    result = detect_processes_from_extraction(extraction)
    assert "grinding_cylindrical" in result


def test_fallback_empty_extraction():
    extraction = {"part_type": "general", "dimensions": {}}
    result = detect_processes_from_extraction(extraction)
    assert result == ["turning", "facing"]
