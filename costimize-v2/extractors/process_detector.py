"""Detect manufacturing processes from vision extraction results."""


def detect_processes_from_extraction(extraction: dict) -> list[str]:
    ai_suggestions = extraction.get("suggested_processes", [])
    if ai_suggestions:
        return ai_suggestions

    processes = []
    dims = extraction.get("dimensions", {})
    part_type = extraction.get("part_type", "general")

    od = dims.get("outer_diameter_mm")
    id_mm = dims.get("inner_diameter_mm")
    width = dims.get("width_mm")
    hole_count = dims.get("hole_count", 0)
    thread_count = dims.get("thread_count", 0)
    groove_count = dims.get("groove_count", 0)

    if part_type == "turning" or (od and not width):
        processes.append("turning")
        processes.append("facing")
        if id_mm and id_mm > 0:
            processes.append("boring")
    elif part_type == "milling" or (width and not od):
        processes.append("milling_face")

    if hole_count and hole_count > 0:
        processes.append("drilling")
    if thread_count and thread_count > 0:
        if part_type == "turning":
            processes.append("threading")
        else:
            processes.append("tapping")
    if groove_count and groove_count > 0:
        processes.append("knurling")

    surface_finish = extraction.get("surface_finish")
    if surface_finish:
        try:
            ra = float(str(surface_finish).replace("Ra", "").replace("ra", "").strip())
            if ra <= 0.8:
                if part_type == "turning":
                    processes.append("grinding_cylindrical")
                else:
                    processes.append("grinding_surface")
        except (ValueError, TypeError):
            pass

    return processes if processes else ["turning", "facing"]
