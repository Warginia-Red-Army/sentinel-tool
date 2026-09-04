from utility.bbox_helper import concert_to_bbox

osielsko = (53.22115742505095, 18.03493039560999, 53.15767589384705, 18.087654949632693)
bydgoszcz = (53.25627789162541, 17.892984388560755, 53.03017154781619, 18.179591743432372)
swiecie = (53.36020041996112, 18.367892082072338, 53.44000380525687, 18.449839932805425)
fordon = (53.180588193962755, 18.173470761568595, 53.120798890215475, 18.112850455336627)




# output test
if __name__ == "main":
    print(concert_to_bbox(osielsko))
    print(concert_to_bbox(bydgoszcz))
    print(concert_to_bbox(swiecie))
    print(concert_to_bbox(fordon))