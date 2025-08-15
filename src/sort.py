def sort(width, height, length, mass):
    volume = width * height * length
    is_bulky = volume >= 1000000
    is_heavy = mass >= 20
    has_negative_mass = mass <= 0

    if has_negative_mass or (is_bulky and is_heavy):
        return "REJECTED"
    elif is_bulky or is_heavy:
        return "SPECIAL"
    else:
        return "STANDARD"
