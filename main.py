import dearpygui.dearpygui as dpg
import configs
from pomodoro_settings import PomodoroSettings


def create_windows():
    dpg.create_context()
    dpg.create_viewport(title=configs.VIEWPORT_TITLE, 
                        width=configs.VIEWPORT_WIDTH, 
                        height=configs.VIEWPORT_HEIGHT)
    dpg.setup_dearpygui()
    dpg.set_global_font_scale(configs.DPG_FONT_SCALE)

    # creating fonts
    create_dpg_fonts()

    # creating themes
    create_dpg_themes()

    # start pomodoro settings window
    PomodoroSettings(dpg)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def create_dpg_fonts():
    with dpg.font_registry():
        dpg.add_font(configs.DEFAULT_FONT_PATH, 20, tag=configs.DEFAULT_FONT_TAG)
        dpg.add_font(configs.TIMER_FONT_PATH, 60, tag=configs.TIMER_FONT_TAG)

        # implement the default font
        dpg.bind_font(configs.DEFAULT_FONT_TAG)


def create_dpg_themes():
    # default theme
    with dpg.theme(tag=configs.DEFAULT_THEME_ID):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (196, 45, 45),
                                category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (196, 45, 45),
                                category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (38, 177, 181),
                                category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 20, 0,
                                category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (65, 157, 161),
                                category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (65, 157, 161),
                                category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)

    dpg.bind_theme(configs.DEFAULT_THEME_ID)


if __name__ == '__main__':
    create_windows()
