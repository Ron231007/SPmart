from hal import hal_usonic as usonic


def got_movement() -> bool:
    dist = usonic.get_distance()
    return True if dist < 10 else False

