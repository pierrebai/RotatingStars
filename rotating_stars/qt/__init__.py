# Ignore errors when importing these in case the Qt5 packages are not installed.
try:
    from .step_scene_animator import step_scene_animator
    #from .anim_scene_animator import anim_scene_animator
except:
    pass
