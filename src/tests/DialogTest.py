from TestingUtils import *

if __name__ == '__main__':
    add_source_folder()
    add_resource_folder()

    from common.Scene import *
    from common.Stage import *
    from common.Transitions import *

    
    from common.gui.Buttons import *
    from common.gui.Dialogs import *
    from models.TextModels import *
    from views.TextViews import *
    from ResourceLoader import *
    
    fonts = ResourceLoader().load_resources_by_type('font')

    font = fonts[0]

    def on_init(event, **kwargs):
        dialog = Dialog(TextModel(font, 'Make a choice, please. The choice ' +
                                        'you make is not as important as ' +
                                        'making the choice.\n\nIt is better to ' +
                                        'do something and be afraid, than to ' +
                                        'live with the fear of doing it.', 24), 625, 'okay', 'cancel')
        
        choose = ChooseDialog(TextModel(font, 'Choose your difficulty', 24), 'easy', 'medium', 'hard')
        
        def on_choice_made(event, **kwargs):
            choice = kwargs['choice']

            text = 'You decided on ' + choice + '.'
            if choice == 'nothing':
                text = 'You must choose something!'
            
            confirm = Confirm(TextModel(font, text, 24))
            confirm.x = confirm.y = 120
            scene.add_child(confirm)
            confirm.visible = True

        choose.on('choice_made', on_choice_made)
            
        def on_hard(event, **kwargs):
            long_str = \
                'Vast Active Living Intelligence System: A ' + \
                'perturbation in the reality field in which a ' + \
                'spontaneous self-monitoring negentropic vortex ' + \
                'is formed, tending progressively to subsume ' + \
                'and incorporate its environment into arrangements ' + \
                'of information. Characterized by quasi-consciousness, ' + \
                'purpose, intelligence, growth, and an armillary coherence.'
            

            choose.text = long_str

        def on_easy(event, **kwargs):
            choose.text = 'Nothing good is easy.'

        def on_medium(event, **kwargs):
            choose.text = 'Most people return small favors, acknowledge ' + \
                          'medium ones and repay greater ones - with ingratitude.'

        choose.on('easy_selected', on_easy)
        choose.on('medium_selected', on_medium)
        choose.on('hard_selected', on_hard)

        def on_okay(event, **kwargs):
            scene.add_child(choose)
            choose.visible = True

        def on_changed(event, **kwargs):
            dialog.center(scene)
            choose.center(scene)

        def on_choose_cancel(event, **kwargs):
            print 'here'
            dialog.visible = True

        choose.on('cancel', on_choose_cancel)
            
        dialog.on('changed', on_changed)
        choose.on('changed', on_changed)
        dialog.on('okay', on_okay)

        scene.add_child(dialog)

        scene.add_child(
            TextView(
                TextModel(font, "This test shows how to follow events " +
                                "on dialogs, if no dialogs are visible, " +
                                "then restart the test.", 12
                          )
                )
            )
                
    
    stage = Stage()
    
    scene = Scene("Dialog Scene")
    scene.width = stage.width
    scene.height = stage.height
    scene.fill_color=(132, 134, 0)
    scene.on('init', on_init)

    stage.start(scene)
    
    

