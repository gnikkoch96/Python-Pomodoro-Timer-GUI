
class pomodoro_timer():
    def __init__(self, dpg, settings):
        self.dpg = dpg
        self.settings = settings

        with dpg.window(label="Pomdoro Timer", height=100, width=300):
            self.create_displays()
            self.create_buttons()


    def create_displays(self):
        displayTime = self.dfg.add_input_text(label="Time Left", default_value=self.settings.get)

    def create_buttons(self):
        buttonPause = self.dpg.add_button(label="Pause", id="Pause")
        buttonResume = self.dpg.add_button(label="Resume", id="Resume")
        buttonStop = self.dpg.add_button(label="Stop", id="Stop")
        buttonRestart = self.dpg.add_button(label="Restart", id="Restart")