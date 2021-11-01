from pomodoro_timer import PomodoroTimer
from tools import Tools

# static variables
SETTINGS_WINDOW_ID = "Settings GUI"
FOCUS_COMBO_ID = "Focus Timer Combo"
SMALL_BREAK_COMBO_ID = "Small Break Combo"
LONG_BREAK_COMBO_ID = "Long Break Combo"
START_BUTTON_ID = "Start"
CONFIG_THEME_ID = "config-theme"
CONFIGURATION_COMBO_WIDTH = 400
CONFIGURATION_COMBO_HEIGHT_PADDING = 15


# Description: this class creates the GUI for the pomodoro settings
# where the user can select their focus timer, small break timer, and long break time
class PomodoroSettings:
    def __init__(self, dpg):
        self.dpg = dpg
        self.list_time = self.create_time_list()
        self.create_pomodoro_settings_window()

    def create_pomodoro_settings_window(self):
        with self.dpg.window(label="Pomodoro Timer Settings",
                             id=SETTINGS_WINDOW_ID,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width(),
                             no_resize=True):
            self.create_pomodoro_settings_items()

    def create_pomodoro_settings_items(self):
        with self.dpg.group(horizontal=True) as image_group:
            self.dpg.add_spacer(width=30)
            Tools.add_and_load_image(self.dpg, 'resources/images/tomato-banner.png', image_group)

        with self.dpg.group(horizontal=True) as config_group:
            self.dpg.add_spacer(height=20,
                                width=275)
            self.create_configuration_window()

    def create_configuration_window(self):
        with self.dpg.child_window(label="configurations",
                            height=300,
                            width=800) as config_window:
            self.dpg.bind_item_theme(config_window, CONFIG_THEME_ID)
            self.create_configuration_items()

    def create_configuration_items(self):
        # combo focus timer
        self.dpg.add_combo(tag=FOCUS_COMBO_ID,
                           items=self.list_time,
                           width=CONFIGURATION_COMBO_WIDTH,
                           default_value=25)
        self.dpg.add_spacer(height=CONFIGURATION_COMBO_HEIGHT_PADDING)

        # combo for small break
        self.dpg.add_combo(tag=SMALL_BREAK_COMBO_ID,
                           items=self.list_time,
                           width=CONFIGURATION_COMBO_WIDTH,
                           default_value=2)
        self.dpg.add_spacer(height=CONFIGURATION_COMBO_HEIGHT_PADDING)

        # combo for long break
        self.dpg.add_combo(tag=LONG_BREAK_COMBO_ID,
                           items=self.list_time,
                           width=CONFIGURATION_COMBO_WIDTH,
                           default_value=15)
        self.dpg.add_spacer(height=CONFIGURATION_COMBO_HEIGHT_PADDING)

        # start button
        with self.dpg.group(horizontal=True) as button_item:
            self.dpg.add_spacer(width=100)
            self.dpg.add_button(label="Start Pomodoro!",
                                tag=START_BUTTON_ID,
                                height=100,
                                width=200,
                                callback=self.start_button_callback)

        self.create_configuration_hover_items()

    def create_configuration_hover_items(self):
        with self.dpg.tooltip(FOCUS_COMBO_ID):
            self.dpg.add_text("Focus Mins")

        with self.dpg.tooltip(SMALL_BREAK_COMBO_ID):
            self.dpg.add_text("Small Break")

        with self.dpg.tooltip(LONG_BREAK_COMBO_ID):
            self.dpg.add_text("Long Break")

        with self.dpg.tooltip(START_BUTTON_ID):
            self.dpg.add_text("Start Pomodoro Session")

    def create_time_list(self):
        time_list = []

        # user has the option to choose between 1 min to 60 mins
        for i in range(1,61):
            time_list.append(i)

        return time_list

    def start_button_callback(self):
        self.dpg.hide_item(SETTINGS_WINDOW_ID)

        # loads the pomodoro timer gui
        PomodoroTimer(self.dpg, self)

    def get_focus_time(self):
        return int(self.dpg.get_value(FOCUS_COMBO_ID))

    def get_small_break(self):
        return int(self.dpg.get_value(SMALL_BREAK_COMBO_ID))

    def get_long_break(self):
        return int(self.dpg.get_value(LONG_BREAK_COMBO_ID))
