class star:
    """
    Describes a rotating stars.
    """
    def __init__(self, sides: int = 7, skip: int = 3):
        self.sides = sides
        self.skip = skip
        self.inner_circle_ratio = float(skip) / float(sides)
        self.inner_circle_dot_ratio = 0.9
