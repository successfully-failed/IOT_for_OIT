def is_standing(scale, diff_y) -> bool:
    # [pl] diff_z nie działa, opncv błędnie go wykrywa.
    if diff_y > 2*scale:
        return True
    else: return False