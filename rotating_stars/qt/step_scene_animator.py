from .base_scene_animator import base_scene_animator
from ..star import star_options
from . import qt_drawings

from PyQt5.QtGui import QTransform, QPolygonF
from PyQt5.QtCore import QPointF, QLineF

class step_scene_animator(base_scene_animator):
    """
    animator using a Qt graphics scene to show step-by-step changes.
    """

    def __init__(self, star, options, *args, **kwargs):
        super(step_scene_animator, self).__init__(star, options, *args, **kwargs)
        self.reset()


    #################################################################
    #
    # Helper functions

    def _get_outer_angle(self, rot_pos: int, rot_steps: int):
        if rot_steps:
            return 360. * float(rot_pos) / float(rot_steps)
        return 0.

    def _get_anti_skip_ratio(self):
        if self.star.sides != self.star.skip:
            return 1. / float(self.star.sides - self.star.skip)
        return 1.

    def _get_inner_center(self, which_inner: int, rot_pos: int, rot_steps: int):
        """
        Calculate the center position of an inner circle.
        """
        inner_center = QPointF(1. - self.star.inner_circle_ratio, 0)
        if self.star.sides != self.star.skip:
            outer_angle = self._get_outer_angle(rot_pos, rot_steps)
            angle = 360. * which_inner * self._get_anti_skip_ratio()
            inner_center = QTransform().rotate(angle + outer_angle).map(inner_center)
        return inner_center

    def _gen_all_dots_for_rot(self, rot_pos: int, rot_steps: int):
        """
        Generate all positions for all dots on all inner circle.
        Fills a 2D array called inner_dots_pos indexed by inner circle
        and dots.
        """
        outer_angle = self._get_outer_angle(rot_pos, rot_steps)
        ratio = float(self.star.skip) * self._get_anti_skip_ratio()
        inner_angle = -outer_angle / ratio
        dots_pos = []
        inner_count = self.star.sides - self.star.skip
        for which_inner in range(0, inner_count):
            dots_pos.append(list())
            inner_center = self._get_inner_center(which_inner, rot_pos, rot_steps)
            for which_dot in range(0, self.star.skip):
                dot_pos = QPointF(self.star.inner_circle_ratio * self.star.inner_circle_dot_ratio, 0)
                dot_angle = 360.0 * which_dot / float(max(self.star.skip, 1))
                dot_pos = QTransform().rotate(dot_angle + inner_angle).map(dot_pos)
                dot_pos += inner_center
                dot_pos *= qt_drawings.outer_size
                dots_pos[which_inner].append(dot_pos)
        return dots_pos

    def _gen_all_dots_pos(self):
        """
        Generate all positions for all dots on all inner circle.
        Fills a 2D array called inner_dots_pos indexed by inner circle
        and dots.
        """
        self.inner_dots_pos = self._gen_all_dots_for_rot(self.circle_rotation_pos, self.circle_rotation_pos_steps)

    def _gen_dot(self, which_dot: int, which_inner: int):
        dot_pos = self.inner_dots_pos[which_inner][which_dot]
        dot = qt_drawings.create_disk(qt_drawings.dot_size, qt_drawings.orange_color)
        dot.setPos(dot_pos)
        self.scene.addItem(dot)
        return dot

    def _gen_star_points(self):
        """
        Create the star by rotating the inner circle leaving a trail
        formed by the dot on the inner circle, forming the star.
        Keep it in the animator to avoid re-recreating on each frame.
        """
        star_segments = 240 // max(self.star.skip, 1)
        all_pos = []
        for i in range(star_segments * self.star.skip + 1):
            new_pos = self._gen_all_dots_for_rot(i, star_segments)
            if len(new_pos) and len(new_pos[0]):
                new_point = new_pos[0][0]
                all_pos.append(new_point)
        if len(all_pos):
            self.star_points = all_pos
        else:
            self.star_points = None


    #################################################################
    #
    # Animator base class function overrides

    def reset(self):
        super(step_scene_animator, self).reset()
        self.circle_rotation_pos = 0.
        self.circle_rotation_pos_steps = 1000 // max(self.star.skip, 1)
        self._gen_all_dots_pos()
        self._gen_star_points()
        
    def generate_outer_circle(self):
        """
        Draw the outer circle inside which the star will be made.
        """
        color = qt_drawings.dark_blue_color if self.options.draw_outer_circle else qt_drawings.no_color
        circle = qt_drawings.create_circle(qt_drawings.outer_size + qt_drawings.line_width, color, qt_drawings.line_width * 2)
        circle.setPos(0, 0)
        self.scene.addItem(circle)
        self.adjust_view_to_fit()

    def generate_inner_circle(self, which_inner: int = 0):
        """
        Draw the inner circle with a radius a fraction of the outer circle.
        That fraction is given as the ratio.
        """
        if not self.options.draw_inner_circles:
            return

        inner_center = self._get_inner_center(which_inner, self.circle_rotation_pos, self.circle_rotation_pos_steps)
        circle = qt_drawings.create_disk(self.star.inner_circle_ratio * qt_drawings.outer_size)
        circle.setPos(inner_center * qt_drawings.outer_size)
        self.scene.addItem(circle)
        self.adjust_view_to_fit()

    def generate_inner_circle_dot(self, which_inner: int = 0):
        """
        Draw the dot on the inner circle at the radius ratio given.
        The ratio should be between 0 and 1.
        """
        if not self.options.draw_dots:
            return

        self._gen_dot(0, which_inner)
        self.adjust_view_to_fit()

    def generate_star(self):
        """
        Draw the star by rotating the inner circle leaving a trail
        formed by the dot on the inner circle, forming the star.
        """
        if not self.options.draw_star:
            return

        if not self.star_points:
            return

        poly = qt_drawings.create_polygon(self.star_points, qt_drawings.dark_gray_color)
        self.scene.addItem(poly)
        self.adjust_view_to_fit()

    def generate_other_inner_circle_dots(self, which_inner: int = 0):
        """
        Draw the other dots on the inner circle that are added
        when the circle passes over the star's spikes.
        """
        if not self.options.draw_dots:
            return

        for which_dot in range(1, self.star.skip):
            self._gen_dot(which_dot, which_inner)
        self.adjust_view_to_fit()

    def generate_inner_circle_polygon(self, which_inner: int = 0):
        """
        Draw the polygon generated by the inner circle dots.
        """
        if not self.options.draw_intra_circle_polygons:
            return

        for which_dot in range(0, self.star.skip):
            p1 = self.inner_dots_pos[which_inner][which_dot]
            p2 = self.inner_dots_pos[which_inner][(which_dot + 1) % self.star.skip]
            line = qt_drawings.create_line(QLineF(p1, p2))
            self.scene.addItem(line)
        self.adjust_view_to_fit()

    def generate_other_inner_circles(self, starting_from: int = 1):
        """
        Draw the additional inner circles and their dots and polygon.
        """
        count = self.star.sides - self.star.skip
        for which_inner in range(starting_from, count):
            self.generate_inner_circle(which_inner)
            self.generate_inner_circle_dot(which_inner)
            self.generate_other_inner_circle_dots(which_inner)
            self.generate_inner_circle_polygon(which_inner)

    def generate_inter_circle_polygons(self):
        """
        Draw the polygon generated by the corresponding dots
        in all inner circles.
        """
        if not self.options.draw_inter_circle_polygons:
            return

        count = self.star.sides - self.star.skip
        for which_dot in range(0, self.star.skip):
            for which_inner in range(0, count):
                p1 = self.inner_dots_pos[which_inner][which_dot]
                p2 = self.inner_dots_pos[(which_inner + 1) % count][which_dot]
                line = qt_drawings.create_line(QLineF(p1, p2), qt_drawings.blue_color)
                self.scene.addItem(line)
        self.adjust_view_to_fit()

    def animate_all(self):
        """
        Animate all the inner circles and their polygons.
        """
        self.circle_rotation_pos = (self.circle_rotation_pos + 1) % (self.circle_rotation_pos_steps * self.star.sides)
        self._gen_all_dots_pos()
        self.reallocate_scene()
        self.generate_outer_circle()
        self.generate_other_inner_circles(0)
        self.generate_star()
        self.generate_inter_circle_polygons()
