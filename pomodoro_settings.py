import configs
from pomodoro_timer import PomodoroTimer
from tools import Tools


# desc: loads the pomodoro settings gui
class PomodoroSettings:
    # user_data references to the loaded user_data.json file
    def __init__(self, dpg, user_data):
        self.dpg = dpg

        self.user_data = user_data

        # loads a list of numbers from 1 to 60 (used to fill the combos)
        self.list_time = Tools.create_time_list()

        self.create_pomodoro_settings_window()

    def create_pomodoro_settings_window(self):
        with self.dpg.window(tag=configs.SETTINGS_WINDOW_ID,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width(),
                             no_resize=True) as config_window:
            self.dpg.set_primary_window(configs.SETTINGS_WINDOW_ID, True)
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

            # check data button
            with self.dpg.group(horizontal=True):
                self.dpg.add_spacer(width=configs.SETTINGS_DATA_BTN_SPACER[0])
                self.dpg.add_button(tag=configs.SETTINGS_DATA_BTN_ID,
                                    label=configs.SETTINGS_DATA_BTN_LABEL,
                                    callback=self.data_callback)

    # launches another window that displays user information (i.e. total pomodoros and total mins)
    def data_callback(self):
        self.create_data_win()

    def create_data_win(self):
        with self.dpg.window(tag=configs.SETTINGS_DATA_WINDOW_ID,
                             label=configs.SETTINGS_DATA_WINDOW_LABEL,
                             width=configs.SETTINGS_DATA_WINDOW_DIMENSIONS[0],
                             height=configs.SETTINGS_DATA_WINDOW_DIMENSIONS[1],
                             pos=configs.SETTINGS_DATA_WINDOW_POS,
                             on_close=self.cleanup_aliases,
                             no_resize=True,
                             modal=True):
            self.dpg.bind_item_theme(configs.SETTINGS_DATA_WINDOW_ID, configs.POPUP_THEME_ID)
            self.create_data_win_items()

    # removes aliases that are no longer being used by the data window
    def cleanup_aliases(self):
        if self.dpg.does_alias_exist(configs.SETTINGS_DATA_WINDOW_ID):
            self.dpg.remove_alias(configs.SETTINGS_DATA_WINDOW_ID)

        if self.dpg.does_alias_exist(configs.SETTINGS_DATA_WINDOW_MINS_FIELD_ID):
            self.dpg.remove_alias(configs.SETTINGS_DATA_WINDOW_MINS_FIELD_ID)

        if self.dpg.does_alias_exist(configs.SETTINGS_DATA_WINDOW_POMODOROS_FIELD_ID):
            self.dpg.remove_alias(configs.SETTINGS_DATA_WINDOW_POMODOROS_FIELD_ID)

        if self.dpg.does_alias_exist(configs.SETTINGS_DATA_WINDOW_CLOSE_BTN_ID):
            self.dpg.remove_alias(configs.SETTINGS_DATA_WINDOW_CLOSE_BTN_ID)

    def create_data_win_items(self):
        # total of mins focused
        self.dpg.add_spacer(height=configs.SETTINGS_DATA_WINDOW_MINS_FIELD_SPACER[1])
        with self.dpg.group(horizontal=True):  # label
            self.dpg.add_spacer(width=configs.SETTINGS_DATA_WINDOW_MINS_FIELD_SPACER[0])
            self.dpg.add_text(configs.SETTINGS_DATA_WINDOW_MINS_FIELD_LABEL)

        with self.dpg.group(horizontal=True):  # input field
            self.dpg.add_spacer(width=configs.SETTINGS_DATA_WINDOW_MINS_FIELD_SPACER[0])
            self.dpg.add_input_text(tag=configs.SETTINGS_DATA_WINDOW_MINS_FIELD_ID,
                                    default_value=self.user_data[configs.USERDATA_TOTAL_FOCUS_MINS],
                                    enabled=False)

        # total of pomodoros
        self.dpg.add_spacer(height=configs.SETTINGS_DATA_WINDOW_POMODOROS_FIELD_SPACER[1])
        with self.dpg.group(horizontal=True):  # label
            self.dpg.add_spacer(width=configs.SETTINGS_DATA_WINDOW_POMODOROS_FIELD_SPACER[0])
            self.dpg.add_text(configs.SETTINGS_DATA_WINDOW_POMODOROS_FIELD_LABEL)

        with self.dpg.group(horizontal=True):  # input field
            self.dpg.add_spacer(width=configs.SETTINGS_DATA_WINDOW_POMODOROS_FIELD_SPACER[0])
            self.dpg.add_input_text(tag=configs.SETTINGS_DATA_WINDOW_POMODOROS_FIELD_ID,
                                    default_value=self.user_data[configs.USERDATA_TOTAL_POMODOROS],
                                    enabled=False)

        # close button
        self.dpg.add_spacer(height=configs.SETTINGS_DATA_WINDOW_CLOSE_BTN_SPACER[1])
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.SETTINGS_DATA_WINDOW_CLOSE_BTN_SPACER[0])
            self.dpg.add_button(tag=configs.SETTINGS_DATA_WINDOW_CLOSE_BTN_ID,
                                label=configs.SETTINGS_DATA_WINDOW_CLOSE_BTN_LABEL,
                                callback=self.close_data_win_callback)

    def close_data_win_callback(self):
        self.dpg.delete_item(configs.SETTINGS_DATA_WINDOW_ID)
        self.cleanup_aliases()

    def create_configuration_items(self):
        # combo focus timer
        self.dpg.add_combo(tag=configs.SETTINGS_FOCUS_COMBO_ID,
                           items=self.list_time,
                           width=configs.SETTINGS_COMBO_WIDTH,
                           default_value=self.user_data[configs.USERDATA_FOCUS_MINS])
        self.dpg.add_spacer(height=configs.SETTINGS_COMBO_HEIGHT_PADDING)

        # combo for small break
        self.dpg.add_combo(tag=configs.SETTINGS_SMALL_BREAK_COMBO_ID,
                           items=self.list_time,
                           width=configs.SETTINGS_COMBO_WIDTH,
                           default_value=self.user_data[configs.USERDATA_SMALLBREAK_MINS])
        self.dpg.add_spacer(height=configs.SETTINGS_COMBO_HEIGHT_PADDING)

        # combo for long break
        self.dpg.add_combo(tag=configs.SETTINGS_LONG_BREAK_COMBO_ID,
                           items=self.list_time,
                           width=configs.SETTINGS_COMBO_WIDTH,
                           default_value=self.user_data[configs.USERDATA_LONGBREAK_MINS])
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

        # save setting configurations
        self.save_settings()

        # loads the pomodoro timer gui
        PomodoroTimer(self.dpg, self, self.user_data)

    def save_settings(self):
        # update data to be stored in the user_data.json
        self.user_data[configs.USERDATA_FOCUS_MINS] = self.get_focus_time()
        self.user_data[configs.USERDATA_SMALLBREAK_MINS] = self.get_small_break()
        self.user_data[configs.USERDATA_LONGBREAK_MINS] = self.get_long_break()

        # update json file
        Tools.update_user_data(self.user_data)

    def get_focus_time(self):
        return int(self.dpg.get_value(configs.SETTINGS_FOCUS_COMBO_ID))

    def get_small_break(self):
        return int(self.dpg.get_value(configs.SETTINGS_SMALL_BREAK_COMBO_ID))

    def get_long_break(self):
        return int(self.dpg.get_value(configs.SETTINGS_LONG_BREAK_COMBO_ID))
