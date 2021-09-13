import dearpygui.dearpygui as dpg
from pomodoro_settings import PomodoroSettings

def create_windows():
    dpg.setup_viewport()
    dpg.set_viewport_title("Pomodoro Timer GUI")
    dpg.set_viewport_height(700)
    dpg.set_viewport_width(1000)
    dpg.set_global_font_scale(1.25)
    PomodoroSettings(dpg)
    dpg.mvStyleVar_ItemInnerSpacing = 20
    dpg.start_dearpygui()

if __name__ == '__main__':
    dpg.show_style_editor()
    dpg.show_documentation()
    create_windows()
    print("Main thread ends")


