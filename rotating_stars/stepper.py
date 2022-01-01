from .star import star
from .animator import animator

class stepper:
    """
    Holds a star and animator and step through its animation.
    """
    def __init__(self, animator: animator):
        self.animator = animator
        self.reset()

    def reset(self):
        self.step_state = 0
        self.animator.reset()

    steps = {
        0: (lambda x: x.generate_outer_circle(), "Add outer circle"),
        1: (lambda x: x.generate_inner_circle(), "Add inner circle"),
        2: (lambda x: x.generate_inner_circle_dot(), "Add inner circle dot"),
        3: (lambda x: x.generate_star(), "Generate the star"),
        4: (lambda x: x.generate_other_inner_circle_dots(), "Generate other inner circle dots"),
        5: (lambda x: x.generate_inner_circle_polygon(), "Generate the inner circle polygon"),
        6: (lambda x: x.generate_other_inner_circles(), "Duplicate the inner circle"),
        7: (lambda x: x.generate_inter_circle_polygons(), "Generate the inter-circle polygons"),
        8: (lambda x: x.animate_all(), "Animate all"),
        9: (lambda x: x.reset(), "Reset"),
    }

    def step(self):
        func, name = stepper.steps[self.step_state]
        self.step_name = name
        func(self.animator)
        if self.step_state != 8:
            self.step_state = (self.step_state+1) % len(stepper.steps)
