def ohml(i: float = None, V: float = None, R: float = None):
    if len([var for var in [i, V, R] if var is not None]) != 2:
        raise ValueError("Incorrect ammount of parameters informed")

    if i is None:
        return V/R

    if V is None:
        return i*R

    if R is None:
        return V/i
