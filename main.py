import dearpygui.dearpygui as dpg
from pomodoro_settings import PomodoroSettings

def create_windows():
    dpg.setup_viewport()
    dpg.set_viewport_title("Pomodoro Timer GUI")
    dpg.set_viewport_height(500)
    dpg.set_viewport_width(800)
    dpg.set_global_font_scale(1.25)
    PomodoroSettings(dpg)
    dpg.start_dearpygui()

if __name__ == '__main__':
    create_windows()
    print("Main thread ends")


