import dearpygui.dearpygui as dpg

VIEWPORT_HEIGHT = 700
VIEWPORT_WIDTH = 1000

dpg.create_context()
dpg.create_viewport(title="(DearPyGUI) Pomodoro Timer", width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT)
dpg.setup_dearpygui()
dpg.set_global_font_scale(1.25)


dpg.show_viewport()
dpg.show_documentation()
dpg.start_dearpygui()
dpg.destroy_context()
