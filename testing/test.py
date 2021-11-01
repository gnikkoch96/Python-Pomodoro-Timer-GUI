import dearpygui.dearpygui as dpg

VIEWPORT_HEIGHT = 700
VIEWPORT_WIDTH = 1000

dpg.create_context()
dpg.create_viewport(title="(DearPyGUI) Pomodoro Timer", width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT)
dpg.setup_dearpygui()
dpg.set_global_font_scale(1.25)

with dpg.window(label="Pomodoro Timer Settings",
                             height=dpg.get_viewport_height(),
                             width=dpg.get_viewport_width(),
                             no_resize=True):

    dpg.add_spacer(height=100)  
    with dpg.group(horizontal=True):    
        dpg.add_button(label="Button")
        dpg.add_spacer(width=100)  
        dpg.add_button(label="Button1")


dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

