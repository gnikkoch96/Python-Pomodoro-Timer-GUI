import time

# Pomodoro_Timer used to handle/create the GUI for the timer
class pomodoro_timer():
    def __init__(self, dpg, settings):
        self.dpg = dpg
        self.settings = settings
        self.timer = Timer() # starts the timer as soon as the gui is generated

        with dpg.window(label="Pomdoro Timer",
                        height=self.dpg.get_viewport_height(),
                        width=self.dpg.get_viewport_width()):
            self.create_displays()
            self.create_buttons()


    def create_displays(self):
        displayMinTime = self.dpg.add_input_text(label="min", default_value=self.settings.get_focus_time())
        self.dpg.configure_item(displayMinTime, enabled=False)

        displaySecTime = self.dpg.add_input_text(label="sec", default_value=0)
        self.dpg.configure_item(displaySecTime, enabled=False)

    def create_buttons(self):
        buttonPause = self.dpg.add_button(label="Pause", id="Pause", callback=self.pause_callback)
        self.dpg.add_same_line()
        buttonResume = self.dpg.add_button(label="Resume", id="Resume", callback=self.resume_callback)
        self.dpg.add_same_line()
        buttonStop = self.dpg.add_button(label="Stop", id="Stop", callback=self.stop_callback)
        self.dpg.add_same_line()
        buttonRestart = self.dpg.add_button(label="Restart", id="Restart", callback=self.restart_callback)
        self.dpg.add_same_line()
        buttonSettings = self.dpg.add_button(label="Settings", id="Settings", callback=self.settings_callback)


    def settings_callback(self):
        # 1. destroys the pomodoro timer window
        # 2. launches the settings window
        pass

    def pause_callback(self):
        # 1. pauses the timer
        pass

    def resume_callback(self):
        # 1. resume the timer
        pass

    def stop_callback(self):
        # 1. resets the timer of focus
        pass

    def restart_callback(self):
        # 1. resets the timer back to focus time
        # 2. resets the counter for the pomodoro cycle
        pass


# Timer class used to handle the timer functionalities
class Timer:
    # initialize the timer with a min
    def __init__(self, min):
        # initialize values
        self.min = min
        self.sec = 0
        self.continue_timer = True # bool used to control the timer
        self.start_timer()

    def start_timer(self):
        # continue the timer until user stops, pauses, or restarts the timer
        # and when the min counter >= 0 and sec is greater than 0
        while self.continue_timer || (self.min >= 0 and self.sec > 0):
            if self.sec <= 0:
                self.min -= self.min - 1
                self.sec = 60
            else:
                self.sec -= 1
                time.sleep(1)

    def restart_timer(self):
        self.continue_timer = False;

    def stop_timer(self):
        self.continue_timer = False;

    def pause_timer(self):
        self.continue_timer = False;


    def get_min_value(self):
        pass

    def get_sec_value(self):
        pass
