from pomodoro_timer import PomodoroTimer
from tools import Tools


# Description: this class creates the GUI for the pomodoro settings
# where the user can select their focus timer, small break timer, and long break time
class PomodoroSettings:
    # static variables
    SETTINGS_WINDOW_ID = "Settings GUI"
    FOCUS_COMBO_ID = "Focus Timer Combo"
    SMALL_BREAK_COMBO_ID = "Small Break Combo"
    LONG_BREAK_COMBO_ID = "Long Break Combo"
    START_BUTTON_ID = "Start"
    CONFIGURATION_COMBO_WIDTH = 400
    CONFIGURATION_ITEM_HEIGHT_PADDING = 15

    def __init__(self, dpg):
        self.dpg = dpg
        self.list_time = self.create_time_list()
        self.create_pomodoro_settings_window()

    def create_pomodoro_settings_window(self):
        with self.dpg.window(label="Pomodoro Timer Settings",
                             id=PomodoroSettings.SETTINGS_WINDOW_ID,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width(),
                             no_resize=True):
            self.create_pomodoro_settings_items()

    def create_pomodoro_settings_items(self):
        Tools.add_padding(self.dpg, 30, 0, True)
        Tools.add_and_load_image(self.dpg, 'resources/images/tomato-banner.png', PomodoroSettings.SETTINGS_WINDOW_ID)

        Tools.add_padding(self.dpg, 275, 20, True)
        self.create_configuration_window()

    def create_configuration_window(self):
        with self.dpg.child(label="configurations",
                            height=300,
                            width=800):
            self.add_configurations_theme()
            self.create_configuration_items()

    def create_configuration_items(self):
        # combo focus timer
        self.dpg.add_combo(id=PomodoroSettings.FOCUS_COMBO_ID,
                           items=self.list_time,
                           width=PomodoroSettings.CONFIGURATION_COMBO_WIDTH,
                           default_value=25)
        Tools.add_padding(self.dpg, 0, PomodoroSettings.CONFIGURATION_ITEM_HEIGHT_PADDING, False)

        # combo for small break
        self.dpg.add_combo(id=PomodoroSettings.SMALL_BREAK_COMBO_ID,
                           items=self.list_time,
                           width=PomodoroSettings.CONFIGURATION_COMBO_WIDTH,
                           default_value=2)
        Tools.add_padding(self.dpg, 0, PomodoroSettings.CONFIGURATION_ITEM_HEIGHT_PADDING, False)

        # combo for long break
        self.dpg.add_combo(id=PomodoroSettings.LONG_BREAK_COMBO_ID,
                           items=self.list_time,
                           width=PomodoroSettings.CONFIGURATION_COMBO_WIDTH,
                           default_value=15)
        Tools.add_padding(self.dpg, 0, PomodoroSettings.CONFIGURATION_ITEM_HEIGHT_PADDING, False)

        # start button
        Tools.add_padding(self.dpg, 100, 0, True)
        self.dpg.add_button(label="Start Pomodoro!",
                            id=PomodoroSettings.START_BUTTON_ID,
                            height=100,
                            width=200,
                            callback=self.start_button_callback)

        self.create_configuration_hover_items()

    def add_configurations_theme(self):
        with self.dpg.theme(default_theme=True):
            self.dpg.add_theme_color(self.dpg.mvThemeCol_ChildBg, (196, 45, 45),
                                     category=self.dpg.mvThemeCat_Core)
            self.dpg.add_theme_color(self.dpg.mvThemeCol_Button, (65, 157, 161),
                                     category=self.dpg.mvThemeCat_Core)
            self.dpg.add_theme_color(self.dpg.mvThemeCol_ScrollbarGrab, (65, 157, 161),
                                     category=self.dpg.mvThemeCat_Core)
            self.dpg.add_theme_style(self.dpg.mvStyleVar_ChildBorderSize, 0)
            self.dpg.add_theme_style(self.dpg.mvStyleVar_FrameRounding, 6)

    def create_configuration_hover_items(self):
        with self.dpg.tooltip(PomodoroSettings.FOCUS_COMBO_ID):
            self.dpg.add_text("Focus Mins")

        with self.dpg.tooltip(PomodoroSettings.SMALL_BREAK_COMBO_ID):
            self.dpg.add_text("Small Break")

        with self.dpg.tooltip(PomodoroSettings.LONG_BREAK_COMBO_ID):
            self.dpg.add_text("Long Break")

        with self.dpg.tooltip(PomodoroSettings.START_BUTTON_ID):
            self.dpg.add_text("Start Pomodoro Session")

    def start_button_callback(self):
        self.dpg.hide_item(PomodoroSettings.SETTINGS_WINDOW_ID)

        # loads the pomodoro timer gui
        PomodoroTimer(self.dpg, self)

    def create_time_list(self):
        time_list = []

        # user has the option to choose between 1 min to 60 mins
        for i in range(1, 61):
            time_list.append(i)

        return time_list

    def get_focus_time(self):
        return int(self.dpg.get_value(PomodoroSettings.FOCUS_COMBO_ID))

    def get_small_break(self):
        return int(self.dpg.get_value(PomodoroSettings.SMALL_BREAK_COMBO_ID))

    def get_long_break(self):
        return int(self.dpg.get_value(PomodoroSettings.LONG_BREAK_COMBO_ID))
