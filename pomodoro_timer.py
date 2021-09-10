import threading
from timer import Timer

# Pomodoro_Timer used to handle/create the GUI for the timer
class PomodoroTimer:
    def __init__(self, dpg, settings):
        self.dpg = dpg
        self.settings = settings
        self.timer = Timer(self.settings.get_focus_time())  # starts the timer as soon as the gui is generated

        with dpg.window(label="Pomdoro Timer",
                        height=self.dpg.get_viewport_height(),
                        width=self.dpg.get_viewport_width()) as pomodoro_window:
            self.create_displays()
            self.create_buttons()

        self.dpg.set_primary_window(pomodoro_window, value=True)

        # creates a new thread
        self.pomodoro_timer_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.pomodoro_timer_thread.start()

    def update_gui(self):  # this is a thread function used to update the gui with the timer min and sec values
        while self.timer.get_min_value() >= 0 and self.timer.get_sec_value() >= 0:
            self.dpg.set_value("Minute", self.timer.get_min_value())
            self.dpg.set_value("Second", self.timer.get_sec_value())


    def create_displays(self):
        display_min_time = self.dpg.add_input_text(label="min", id="Minute", default_value=self.timer.get_min_value())
        self.dpg.configure_item(display_min_time, enabled=False)

        display_sec_time = self.dpg.add_input_text(label="sec", id="Second", default_value=self.timer.get_sec_value())
        self.dpg.configure_item(display_sec_time, enabled=False)

        display_pomodoro_counter = self.dpg.add_input_text(label="# of Pomodoros", id="Pomdodoro Counter", default_value=0) # later on default value will be read from a file
        self.dpg.configure_item(display_pomodoro_counter, enabled=False)

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
        # 1. stop the timer and gui thread
        self.pomodoro_timer_thread.exit()
        # 2. show the settings gui again
        self.dpg.show_item("Settings GUI")


    def pause_callback(self):
        self.timer.pause_timer()

    def resume_callback(self):
        self.timer.resume_timer()

    def stop_callback(self):
        self.timer.stop_timer()

    def restart_callback(self):
        self.timer.restart_timer()
