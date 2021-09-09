from pomodoro_timer import PomodoroTimer


class PomodoroSettings:
    def __init__(self, dpg):
        self.dpg = dpg
        self.list_time = self.create_time_list()

        with dpg.window(label="Pomodoro Timer Settings",
                        id="Settings GUI",
                        height=self.dpg.get_viewport_height(),
                        width=self.dpg.get_viewport_width()) :
            self.comboFocusTime = dpg.add_combo(label="Focus Time",
                                                id="Focus Time Combo",
                                                items=self.list_time,
                                                default_value=25)
            self.comboSmallBreak = dpg.add_combo(label="Small Break",
                                                 id="Small Break Combo",
                                                 items=self.list_time,
                                                 default_value=2)
            self.comboLongBreak = dpg.add_combo(label="Long Break",
                                                id="Long Break Combo",
                                                items=self.list_time,
                                                default_value=15)
            self.buttonStart = dpg.add_button(label="Start Pomodoro!",
                                              id="Start",
                                              callback=self.start_button_callback)

    def start_button_callback(self):
        PomodoroTimer(self.dpg, self)  # starts the timer
        self.dpg.hide_item("Settings GUI")

    def get_focus_time(self):
        return self.dpg.get_value("Focus Time Combo")

    def get_small_break(self):
        return self.dpg.get_value("Small Break Combo")

    def get_long_break(self):
        return self.dpg.get_value("Long Break Combo")

    def create_time_list(self):
        time_list = []
        for i in range(1, 61):  # creates a list between 1 - 60 mins to choose for the time
            time_list.append(i)
        return time_list
