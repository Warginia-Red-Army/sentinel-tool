osielsko = (53.22115742505095, 18.03493039560999, 53.15767589384705, 18.087654949632693)
bydgoszcz = (53.25627789162541, 17.892984388560755, 53.03017154781619, 18.179591743432372)
swiecie = (53.36020041996112, 18.367892082072338, 53.44000380525687, 18.449839932805425)
fordon = (53.180588193962755, 18.173470761568595, 53.120798890215475, 18.112850455336627)


def convertToCorrectBbox(bbox: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
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

    return min_lon,  min_lat, max_lon, max_lat

# output test
print(convertToCorrectBbox(osielsko))
print(convertToCorrectBbox(bydgoszcz))
print(convertToCorrectBbox(swiecie))
print(convertToCorrectBbox(fordon))