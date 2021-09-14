from pomodoro_timer import PomodoroTimer


class PomodoroSettings:
    # static variables
    SETTINGS_WINDOW_TAG = "Settings GUI"
    CONFIGURATION_COMBO_WIDTH = 400
    CONFIGURATION_ITEM_PADDING = 15

    def __init__(self, dpg):
        self.dpg = dpg
        self.list_time = self.create_time_list()

        with self.dpg.window(label="Pomodoro Timer Settings",
                             id="Settings GUI",
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width()):
            self.create_items()

        self.dpg.set_primary_window(PomodoroSettings.SETTINGS_WINDOW_TAG, value=True)

    def create_items(self):
        self.dpg.add_dummy(width=30)
        self.dpg.add_same_line()
        self.add_and_load_image('resources/images/tomato-banner.png', "Settings GUI")

        self.dpg.add_dummy(height=50)
        self.dpg.add_dummy(width=275)
        self.dpg.add_same_line()
        with self.dpg.child(label="configurations",
                            height=300,
                            width=800):
            # themes for the configurations window
            with self.dpg.theme(default_theme=True):
                self.dpg.add_theme_color(self.dpg.mvThemeCol_ChildBg, (196, 45, 45), category=self.dpg.mvThemeCat_Core)
                self.dpg.add_theme_color(self.dpg.mvThemeCol_Button, (65, 157, 161), category=self.dpg.mvThemeCat_Core)
                self.dpg.add_theme_color(self.dpg.mvThemeCol_ScrollbarGrab, (65, 157, 161),
                                         category=self.dpg.mvThemeCat_Core)
                self.dpg.add_theme_style(self.dpg.mvStyleVar_ChildBorderSize, 0)
                self.dpg.add_theme_style(self.dpg.mvStyleVar_FrameRounding, 6)

            # combo focus timer
            self.dpg.add_combo(id="Focus Time Combo",
                               items=self.list_time,
                               width=PomodoroSettings.CONFIGURATION_COMBO_WIDTH,
                               default_value=25)
            self.dpg.add_dummy(height=PomodoroSettings.CONFIGURATION_ITEM_PADDING)

            # combo for small break
            self.dpg.add_combo(id="Small Break Combo",
                               items=self.list_time,
                               width=PomodoroSettings.CONFIGURATION_COMBO_WIDTH,
                               default_value=2)
            self.dpg.add_dummy(height=PomodoroSettings.CONFIGURATION_ITEM_PADDING)

            # combo for long break
            self.dpg.add_combo(id="Long Break Combo",
                               items=self.list_time,
                               width=PomodoroSettings.CONFIGURATION_COMBO_WIDTH,
                               default_value=15)
            self.dpg.add_dummy(height=PomodoroSettings.CONFIGURATION_ITEM_PADDING)

            # start button
            self.dpg.add_dummy(width=100)
            self.dpg.add_same_line()
            self.dpg.add_button(label="Start Pomodoro!",
                                id="Start",
                                height=100,
                                width=200,
                                callback=self.start_button_callback)

            self.create_hover_items()

    def create_hover_items(self):
        with self.dpg.tooltip("Focus Time Combo"):
            self.dpg.add_text("Focus Mins")

        with self.dpg.tooltip("Small Break Combo"):
            self.dpg.add_text("Small Break")

        with self.dpg.tooltip("Long Break Combo"):
            self.dpg.add_text("Long Break")

        with self.dpg.tooltip("Start"):
            self.dpg.add_text("Start Pomodoro Session")

    # grabbed from the documents
    def add_and_load_image(self, image_path, parent=None):
        width, height, channels, data = self.dpg.load_image(image_path)

        with self.dpg.texture_registry() as reg_id:
            texture_id = self.dpg.add_static_texture(width, height, data, parent=reg_id)

        if parent is None:
            return self.dpg.add_image(texture_id)
        else:
            return self.dpg.add_image(texture_id, parent=parent)

    def start_button_callback(self):
        PomodoroTimer(self.dpg, self)  # starts the timer
        self.dpg.hide_item(PomodoroSettings.SETTINGS_WINDOW_TAG)

    def get_focus_time(self):
        return int(self.dpg.get_value("Focus Time Combo"))

    def get_small_break(self):
        return int(self.dpg.get_value("Small Break Combo"))

    def get_long_break(self):
        return int(self.dpg.get_value("Long Break Combo"))

    def create_time_list(self):
        time_list = []
        for i in range(1, 61):  # creates a list between 1 - 60 mins to choose for the time
            time_list.append(i)

        # debug purposes
        # for i in range(0, 2):
        #     time_list.append(i)

        return time_list
