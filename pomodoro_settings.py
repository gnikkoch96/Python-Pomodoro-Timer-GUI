import configs
import json
from pomodoro_timer import PomodoroTimer
from tools import Tools
from os.path import exists


# Description: this class creates the GUI for the pomodoro settings
# where the user can select their focus timer, small break timer, and long break time
class PomodoroSettings:
    def __init__(self, dpg):
        self.dpg = dpg
        self.list_time = PomodoroSettings.create_time_list()
        self.default_time = [configs.SETTINGS_FOCUS_COMBO_DEFAULT_VALUE,
                             configs.SETTINGS_SMALL_BREAK_COMBO_DEFAULT_VALUE,
                             configs.SETTINGS_LONG_BREAK_COMBO_DEFAULT_VALUE]

        # check if settings file exists
        if exists(configs.USERDATA_FILEPATH):
            user_data = open(configs.USERDATA_FILEPATH)
            data = json.load(user_data)

            self.default_time[0] = data[configs.USERDATA_FOCUS_MINS]
            self.default_time[1] = data[configs.USERDATA_SMALLBREAK_MINS]
            self.default_time[2] = data[configs.USERDATA_LONGBREAK_MINS]

            user_data.close()
        else:
            Tools.create_default_user_data()

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

            # check data button
            with self.dpg.group(horizontal=True):
                self.dpg.add_spacer(width=configs.SETTINGS_DATA_BTN_SPACER[0])
                self.dpg.add_button(tag=configs.SETTINGS_DATA_BTN_ID,
                                    label=configs.SETTINGS_DATA_BTN_LABEL,
                                    callback=self.data_callback)

    # launches another window that display user information (i.e. # of mins productive)
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
            self.create_data_win_items()

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
        # read from file if it exists
        focus_mins = 0
        pomodoros = 0
        if exists(configs.USERDATA_FILEPATH):
            data_file = open(configs.USERDATA_FILEPATH)
            data = json.load(data_file)

            focus_mins = data[configs.USERDATA_TOTAL_FOCUS_MINS]
            pomodoros = data[configs.USERDATA_TOTAL_POMODOROS]

            data_file.close()

        # number of mins focused
        self.dpg.add_text(configs.SETTINGS_DATA_WINDOW_MINS_FIELD_LABEL)
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.SETTINGS_DATA_WINDOW_MINS_FIELD_SPACER[0])
            self.dpg.add_input_text(tag=configs.SETTINGS_DATA_WINDOW_MINS_FIELD_ID,
                                    default_value=focus_mins,
                                    enabled=False)

        # number of pomodoros so far
        self.dpg.add_text(configs.SETTINGS_DATA_WINDOW_POMODOROS_FIELD_LABEL)
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.SETTINGS_DATA_WINDOW_POMODOROS_FIELD_SPACER[0])
            self.dpg.add_input_text(tag=configs.SETTINGS_DATA_WINDOW_POMODOROS_FIELD_ID,
                                    default_value=pomodoros,
                                    enabled=False)

        # close button
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
                           default_value=self.default_time[0])
        self.dpg.add_spacer(height=configs.SETTINGS_COMBO_HEIGHT_PADDING)

        # combo for small break
        self.dpg.add_combo(tag=configs.SETTINGS_SMALL_BREAK_COMBO_ID,
                           items=self.list_time,
                           width=configs.SETTINGS_COMBO_WIDTH,
                           default_value=self.default_time[1])
        self.dpg.add_spacer(height=configs.SETTINGS_COMBO_HEIGHT_PADDING)

        # combo for long break
        self.dpg.add_combo(tag=configs.SETTINGS_LONG_BREAK_COMBO_ID,
                           items=self.list_time,
                           width=configs.SETTINGS_COMBO_WIDTH,
                           default_value=self.default_time[2])
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
        PomodoroTimer(self.dpg, self)

    def save_settings(self):
        data_file = open(configs.USERDATA_FILEPATH)
        user_data = json.load(data_file)
        user_data[configs.USERDATA_FOCUS_MINS] = self.get_focus_time()
        user_data[configs.USERDATA_SMALLBREAK_MINS] = self.get_small_break()
        user_data[configs.USERDATA_LONGBREAK_MINS] = self.get_long_break()

        data_file.close()

    def get_focus_time(self):
        return int(self.dpg.get_value(configs.SETTINGS_FOCUS_COMBO_ID))

    def get_small_break(self):
        return int(self.dpg.get_value(configs.SETTINGS_SMALL_BREAK_COMBO_ID))

    def get_long_break(self):
        return int(self.dpg.get_value(configs.SETTINGS_LONG_BREAK_COMBO_ID))
