import rotating_stars
from rotating_stars.qt.step_scene_animator import step_scene_animator
from qt_helpers import *

app = create_app()

star = rotating_stars.star()
options = rotating_stars.star_options()

timer_delay = 20
timer = create_timer(timer_delay)
timer.setSingleShot(False)
playing = False
animator = step_scene_animator(star, options)

stepper = rotating_stars.stepper(animator)
step_names = list(map(lambda i: i[1][1], sorted(stepper.steps.items())))

control_dock, control_layout = create_dock("Play Controls")

step_name_list = create_list("Current Step", step_names, control_layout)
step_button = create_button("Step", control_layout)
play_button = create_button("Play", control_layout)
stop_button = create_button("Stop", control_layout)
reset_button = create_button("Reset", control_layout)
add_stretch(control_layout)

anim_dock, anim_layout = create_dock("Animation Controls")

delay_box = create_number_range("Animation duration (ms)", 0, 10000, timer_delay, anim_layout)
add_stretch(anim_layout)

star_dock, star_layout = create_dock("Star Type")

sides_box = create_number_text("Number of sides", 3, 100, star.sides, star_layout)
skip_box = create_number_text("Star branch skip", 1, 100, star.skip, star_layout)
add_stretch(star_layout)

draw_dock, draw_layout = create_dock("Draw")

draw_intra_option = create_option("Draw intra-circle polygons", draw_layout, options.draw_intra_circle_polygons)
draw_inter_option = create_option("Draw inter-circle polygons", draw_layout, options.draw_inter_circle_polygons)
draw_dots_option = create_option("Draw dots", draw_layout, options.draw_dots)
draw_inner_option = create_option("Draw inner circles", draw_layout, options.draw_inner_circles)
draw_outer_option = create_option("Draw outer circle", draw_layout, options.draw_outer_circle)

window = create_main_window("Rotating Stars", animator.widget())
add_dock(window, control_dock)
add_dock(window, anim_dock)
add_dock(window, star_dock)
add_dock(window, draw_dock)


def advance_step():
    stepper.step()
    select_in_list(stepper.step_name, step_name_list)

@reset_button.clicked.connect
def on_reset():
    stepper.reset()

@step_button.clicked.connect
def on_step():
    advance_step()

@play_button.clicked.connect
def on_play():
    global playing
    playing = True
    timer.start()

@stop_button.clicked.connect
def on_stop():
    global playing
    playing = False
    timer.stop()

@delay_box.valueChanged.connect
def on_delay_changed(value):
    animator.anim_duration = int(value)
    timer.setInterval(int(value))

@sides_box.textChanged.connect
def on_sides(value):
    try:
        new_sides = int(value)
    except:
        return
    global star
    star = rotating_stars.star(new_sides, star.skip)
    animator.star = star

@skip_box.textChanged.connect
def on_skip(value):
    try:
        new_skip = int(value)
    except:
        return
    global star
    star = rotating_stars.star(star.sides, new_skip)
    animator.star = star

@timer.timeout.connect
def on_timer():
    advance_step()

@draw_intra_option.stateChanged.connect
def on_draw_intra(state):
    options.draw_intra_circle_polygons = bool(state)

@draw_inter_option.stateChanged.connect
def on_draw_inter(state):
    options.draw_inter_circle_polygons = bool(state)

@draw_dots_option.stateChanged.connect
def on_draw_dots(state):
    options.draw_dots = bool(state)

@draw_inner_option.stateChanged.connect
def on_draw_inner(state):
    options.draw_inner_circles = bool(state)

@draw_outer_option.stateChanged.connect
def on_draw_outer(state):
    options.draw_outer_circle = bool(state)

start_app(app, window)

