import dearpygui.dearpygui as dpg
from pomodoro_settings import PomodoroSettings

VIEWPORT_HEIGHT = 700
VIEWPORT_WIDTH = 1000

DEFAULT_FONT_TAG = "default"
TIMER_FONT_TAG = "timer-font"
CONFIG_THEME_ID = "config-theme"

def create_windows():
    dpg.create_context()
    dpg.create_viewport(title="(DearPyGUI) Pomodoro Timer", width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT)
    dpg.setup_dearpygui()
    dpg.set_global_font_scale(1.25)

    # adding font to the dearpygui's font pool
    create_dpg_fonts()

    # adding default theme
    create_dpg_themes()

    # setting up pomodoro settings
    PomodoroSettings(dpg)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def create_dpg_fonts():
    with dpg.font_registry():
        dpg.add_font("resources/fonts/Simpleton-Gothic.ttf", 20, tag=DEFAULT_FONT_TAG)
        dpg.add_font("resources/fonts/Simpleton-Gothic.ttf", 60, tag=TIMER_FONT_TAG)
        dpg.bind_font(DEFAULT_FONT_TAG)
        
def create_dpg_themes():
    with dpg.theme(default_theme=True) as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (196, 45, 45), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (38, 177, 181), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 0, category=dpg.mvThemeCat_Core)

    with dpg.theme():
        with dpg.theme_component(tag=CONFIG_THEME_ID):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (196, 45, 45),
                                    category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (65, 157, 161),
                                    category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (65, 157, 161),
                                    category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
    dpg.bind_theme(global_theme)


if __name__ == '__main__':
    dpg.show_style_editor()
    create_windows()
