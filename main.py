import dearpygui.dearpygui as dpg
from pomodoro_settings import pomodoro_settings

def create_windows():
    dpg.setup_viewport()
    dpg.set_viewport_title("Pomodoro Timer GUI")
    dpg.set_viewport_height(500)
    dpg.set_viewport_width(800)
    dpg.set_global_font_scale(1.25)

    pSettings = pomodoro_settings(dpg)

    dpg.start_dearpygui()

if __name__ == '__main__':
    create_windows()

