import rotating_stars
#from rotating_stars.qt.anim_scene_animator import anim_scene_animator
from rotating_stars.qt.step_scene_animator import step_scene_animator
from qt_helpers import *

app = create_app()

timer = create_timer(1)
timer.setSingleShot(True)
playing = False

star = rotating_stars.star()
#animator = anim_scene_animator(star, lambda: playing and timer.start(), 500)
animator = step_scene_animator(star)
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

animate_option = create_option("Animate", anim_layout)
delay_box = create_number_range("Animation duration (ms)", 0, 10000, 500, anim_layout)
#show_arrow_option = create_option("Show movement arrow", anim_layout)
#show_cross_option = create_option("Show collision cross", anim_layout)
add_stretch(anim_layout)

gen_dock, gen_layout = create_dock("Star Type")

sides_box = create_number_text("Number of sides", 3, 100, star.sides, gen_layout)
skip_box = create_number_text("Star branch skip", 1, 100, star.skip, gen_layout)
add_stretch(gen_layout)

window = create_main_window("Rotating Stars", animator.widget())
add_dock(window, control_dock)
add_dock(window, anim_dock)
add_dock(window, gen_dock)


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

@animate_option.stateChanged.connect
def on_animate(state):
    animator.animate = bool(state)

# @show_arrow_option.stateChanged.connect
# def on_show_arrow(state):
#     animator.show_movement_arrow = bool(state)

# @show_cross_option.stateChanged.connect
# def on_show_cross(state):
#     animator.show_collision_cross = bool(state)

@timer.timeout.connect
def on_timer():
    advance_step()

start_app(app, window)

