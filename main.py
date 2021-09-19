import dearpygui.dearpygui as dpg
from pomodoro_settings import PomodoroSettings

VIEWPORT_HEIGHT = 700
VIEWPORT_WIDTH = 1000


def create_windows():
    dpg.setup_viewport()
    dpg.set_viewport_title("(DearPyGUI) Pomodoro Timer ")
    dpg.set_viewport_height(VIEWPORT_HEIGHT)
    dpg.set_viewport_width(VIEWPORT_WIDTH)
    dpg.set_global_font_scale(1.25)

    # adding font to the dearpygui's font pool
    create_dpg_fonts()

    # adding default theme
    create_dpg_themes()

    # setting up pomodoro settings
    PomodoroSettings(dpg)

    dpg.start_dearpygui()


def create_dpg_fonts():
    with dpg.font_registry():
        dpg.add_font("resources/fonts/Simpleton-Gothic.ttf", 20, default_font=True)
        dpg.add_font("resources/fonts/Simpleton-Gothic.ttf", 60, id="Timer Font")


def create_dpg_themes():
    with dpg.theme(default_theme=True):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (196, 45, 45), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (38, 177, 181), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 0, category=dpg.mvThemeCat_Core)


if __name__ == '__main__':
    create_windows()
