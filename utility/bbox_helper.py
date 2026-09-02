def concert_to_bbox(bbox: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    if bbox[0] < bbox[2]:
        min_lat = bbox[0]
        max_lat = bbox[2]
    else:
        min_lat = bbox[2]
        max_lat = bbox[0]

    if bbox[1] < bbox[3]:
        min_lon = bbox[1]
        max_lon = bbox[3]
    else:
        min_lon = bbox[3]
        max_lon = bbox[1]

    return min_lon, min_lat, max_lon, max_lat
