import dearpygui.dearpygui as dpg
from pomodoro_settings import pomodoro_settings
from pomodoro_timer import pomodoro_timer

def create_windows():
    pSettings = pomodoro_settings(dpg)
    pTimer = pomodoro_timer(dpg, pSettings)

    dpg.setup_viewport()
    dpg.set_viewport_title("Pomodoro Timer GUI")
    dpg.set_viewport_height(500)
    dpg.set_viewport_width(800)
    dpg.start_dearpygui()


if __name__ == '__main__':
    create_windows()
