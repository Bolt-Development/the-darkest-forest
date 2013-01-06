from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from common.Scene import *
    from common.Stage import *

    def on_menu_one_tick():
        print 'menu one tick'

    def print_event(event, **kwargs):
        print event

    menu1 = Scene("Menu One")
    menu1.on('tick', on_menu_one_tick)
    
    stage = Stage()
    stage.start(menu1)
    
    

