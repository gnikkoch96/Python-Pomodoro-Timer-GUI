import dearpygui.dearpygui as dpg
from pomodoro_settings import PomodoroSettings

def create_windows():
    dpg.setup_viewport()
    dpg.set_viewport_title("Pomodoro Timer GUI")
    dpg.set_viewport_height(700)
    dpg.set_viewport_width(1000)

    # adding font to the dearpygui's font pool
    with dpg.font_registry():
        dpg.add_font("resources/fonts/Simpleton-Gothic.ttf", 20, default_font=True)
        # dpg.add_font("resources/fonts/simplto2.ttf", 60, id="Timer Font")
        dpg.add_font("resources/fonts/Simpleton-Gothic.ttf", 60, id="Timer Font")

    # adding default theme
    with dpg.theme(default_theme=True) as theme_id:
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (196, 45, 45), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 0, category=dpg.mvThemeCat_Core)

    dpg.set_global_font_scale(1.25)

    # loads the pomodoro settings
    PomodoroSettings(dpg)

    dpg.start_dearpygui()

if __name__ == '__main__':
    # dpg.show_documentation()
    create_windows()
    print("Main thread ends")


