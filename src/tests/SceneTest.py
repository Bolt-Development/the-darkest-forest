from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from common.Scene import *


    def print_event(event, **kwards):
        print event

    intro_scene = Scene(None)
    child_scene = Scene(intro_scene)
    intro_scene.add_child(child_scene)


    intro_scene.engine.on("on_child_added", print_event)
    intro_scene.engine.start()

