import configs
from pomodoro_timer import PomodoroTimer
from tools import Tools


# Description: this class creates the GUI for the pomodoro settings
# where the user can select their focus timer, small break timer, and long break time
class PomodoroSettings:
    def __init__(self, dpg):
        self.dpg = dpg
        self.list_time = PomodoroSettings.create_time_list()
        self.create_pomodoro_settings_window()

    @staticmethod
    # generates the list of mins that user can choose from
    def create_time_list():
        time_list = []

        # user has the option to choose between 1 min to 60 mins
        for i in range(1, 61):
            time_list.append(i)

        return time_list

    def create_pomodoro_settings_window(self):
        with self.dpg.window(tag=configs.SETTINGS_WINDOW_ID,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width(),
                             no_resize=True) as config_window:
            self.dpg.set_primary_window(configs.SETTINGS_WINDOW_ID, True)

            # todo might need to remove this as I wanted to make this the global theme
            # load theme
            self.dpg.bind_item_theme(config_window, configs.DEFAULT_THEME_ID)

            self.create_pomodoro_settings_items()

    def create_pomodoro_settings_items(self):
        # banner image
        self.dpg.add_spacer(height=configs.SETTINGS_BANNER_HEIGHT_SPACER)
        with self.dpg.group(horizontal=True) as image_group:
            self.dpg.add_spacer(width=configs.SETTINGS_BANNER_WIDTH_SPACER)
            Tools.add_and_load_image(self.dpg, configs.BANNER_IMG_PATH, image_group)

        # combos
        self.dpg.add_spacer(height=configs.SETTINGS_COMBOS_HEIGHT_SPACER)
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.SETTINGS_COMBOS_WIDTH_SPACER)
            self.create_configuration_window()

    def create_configuration_window(self):
        with self.dpg.child_window(width=configs.SETTINGS_CONFIG_WINDOW_DIMENSIONS[0],
                                   height=configs.SETTINGS_CONFIG_WINDOW_DIMENSIONS[1]):
            self.create_configuration_items()

    def create_configuration_items(self):
        # combo focus timer
        self.dpg.add_combo(tag=configs.SETTINGS_FOCUS_COMBO_ID,
                           items=self.list_time,
                           width=configs.SETTINGS_COMBO_WIDTH,
                           default_value=configs.SETTINGS_FOCUS_COMBO_DEFAULT_VALUE)
        self.dpg.add_spacer(height=configs.SETTINGS_COMBO_HEIGHT_PADDING)

        # combo for small break
        self.dpg.add_combo(tag=configs.SETTINGS_SMALL_BREAK_COMBO_ID,
                           items=self.list_time,
                           width=configs.SETTINGS_COMBO_WIDTH,
                           default_value=configs.SETTINGS_SMALL_BREAK_COMBO_DEFAULT_VALUE)
        self.dpg.add_spacer(height=configs.SETTINGS_COMBO_HEIGHT_PADDING)

        # combo for long break
        self.dpg.add_combo(tag=configs.SETTINGS_LONG_BREAK_COMBO_ID,
                           items=self.list_time,
                           width=configs.SETTINGS_COMBO_WIDTH,
                           default_value=configs.SETTINGS_LONG_BREAK_COMBO_DEFAULT_VALUE)
        self.dpg.add_spacer(height=configs.SETTINGS_COMBO_HEIGHT_PADDING)

        # start button
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.SETTINGS_START_BTN_WIDTH_SPACER)
            self.dpg.add_button(label=configs.SETTINGS_START_BUTTON_LABEL,
                                tag=configs.SETTINGS_START_BUTTON_ID,
                                height=configs.SETTINGS_START_BUTTON_HEIGHT,
                                width=configs.SETTINGS_START_BUTTON_WIDTH,
                                callback=self.start_button_callback)

        self.create_configuration_hover_items()

    def create_configuration_hover_items(self):
        with self.dpg.tooltip(configs.SETTINGS_FOCUS_COMBO_ID):
            self.dpg.add_text(configs.SETTINGS_FOCUS_COMBO_TOOLTIP)

        with self.dpg.tooltip(configs.SETTINGS_SMALL_BREAK_COMBO_ID):
            self.dpg.add_text(configs.SETTINGS_SMALL_BREAK_COMBO_TOOLTIP)

        with self.dpg.tooltip(configs.SETTINGS_LONG_BREAK_COMBO_ID):
            self.dpg.add_text(configs.SETTINGS_LONG_BREAK_COMBO_TOOLTIP)

        with self.dpg.tooltip(configs.SETTINGS_START_BUTTON_ID):
            self.dpg.add_text(configs.SETTINGS_START_BTN_TOOLTIP)

    def start_button_callback(self):
        self.dpg.hide_item(configs.SETTINGS_WINDOW_ID)

        # loads the pomodoro timer gui
        PomodoroTimer(self.dpg, self)

    def get_focus_time(self):
        return int(self.dpg.get_value(configs.SETTINGS_FOCUS_COMBO_ID))

    def get_small_break(self):
        return int(self.dpg.get_value(configs.SETTINGS_SMALL_BREAK_COMBO_ID))

    def get_long_break(self):
        return int(self.dpg.get_value(configs.SETTINGS_LONG_BREAK_COMBO_ID))
