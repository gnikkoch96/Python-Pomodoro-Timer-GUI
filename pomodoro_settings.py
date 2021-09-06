
class pomodoro_settings():
    def __init__(self, dpg):
        with dpg.window(label="Pomodoro Timer Settings", width=300):
            self.inputFocusTimeInt = dpg.add_input_int(label="Focus Time", default_value=25)
            self.inputSmallBreakInt = dpg.add_input_int(label="Small Break", default_value=2)
            self.inputLongBreakInt = dpg.add_input_int(label="Long Break", default_value=15)

            # dpg.configure_item(inputFocusTimeInt, enabled=False)

    def get_focus_time(self):
        return self.inputFocusTimeInt

    def get_small_break(self):
        return self.inputSmallBreakInt

    def get_long_break(self):
        return self.inputLongBreakInt
