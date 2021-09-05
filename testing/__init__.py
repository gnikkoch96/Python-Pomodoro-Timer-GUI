import dearpygui.dearpygui as dpg


def save_callback():
    print('Save Clicked')


if __name__ == '__main__':
    with dpg.window(label='Example Window'):
        dpg.add_text('Hello World')
        dpg.add_button(label='Save', callback=save_callback) # we applied an onClickListener
        dpg.add_input_text(label='string') # can input text
        dpg.add_slider_float(label='float') # slider that allows a float to be chosen

    dpg.setup_viewport()
    dpg.start_dearpygui()
