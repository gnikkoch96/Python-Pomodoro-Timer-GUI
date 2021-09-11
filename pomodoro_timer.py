import threading
from timer import Timer


# Pomodoro_Timer used to handle/create the GUI for the timer
class PomodoroTimer:
    def __init__(self, dpg, settings):
        # initialize values
        self.dpg = dpg
        self.settings = settings
        self.timer = Timer(self.settings.get_focus_time(),
                           self.settings.get_small_break(),
                           self.settings.get_long_break())
        self.local_pomodoro_counter = 0
        self.global_pomodoro_counter = 0  # n: later I want to read from a file to see how many pomodoros the user has done for the day

        # Window
        with dpg.window(label="Pomdoro Timer",
                        height=self.dpg.get_viewport_height(),
                        width=self.dpg.get_viewport_width()) as self.pomodoro_window:
            self.create_displays()
            self.create_buttons()

        self.dpg.set_primary_window(self.pomodoro_window, value=True)

        # creates a new thread
        self.pomodoro_timer_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.pomodoro_timer_thread.start()

    def update_gui(self):  # this is a thread function used to update the gui with the timer min and sec values
        print("Pomdoro Timer GUI Thread Started")
        while not self.timer.timer_stop and (self.timer.get_min_value() >= 0 and self.timer.get_sec_value() >= 0):
            self.dpg.set_value("Minute", self.timer.get_min_value())
            self.dpg.set_value("Second", self.timer.get_sec_value())

            # n: currently used for testing b/c breaking from a program is never good practice
            if self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0:
                break

        # only add to counter if the timer finishes (not when the user presses stop or restart)
        if self.timer.isFocus and self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0:
            pomodoro_counter = int(self.dpg.get_value("PomodoroCounter")) + 1
            self.local_pomodoro_counter = pomodoro_counter
            if self.local_pomodoro_counter == 4:
                self.timer.isOnLongBreak = True
                self.timer.isFocus = False
                self.local_pomodoro_counter = 0
            else:
                self.timer.isOnSmallBreak = True
                self.timer.isFocus = False
            self.dpg.set_value("PomodoroCounter", str(pomodoro_counter))
        else:  # either on small break or long break
            self.timer.isFocus = True
            self.timer.isOnSmallBreak = False
            self.timer.isOnLongBreak = False

        print("Pomodoro Timer GUI Thread Ended")

    def create_displays(self):
        display_min_time = self.dpg.add_input_text(label="min", id="Minute", default_value=self.timer.get_min_value())
        self.dpg.configure_item(display_min_time, enabled=False)

        display_sec_time = self.dpg.add_input_text(label="sec", id="Second", default_value=self.timer.get_sec_value())
        self.dpg.configure_item(display_sec_time, enabled=False)

        display_pomodoro_counter = self.dpg.add_input_text(label="# of Pomodoros",
                                                           id="PomodoroCounter",
                                                           default_value=0)  # later on default value will be read from a file
        self.dpg.configure_item(display_pomodoro_counter, enabled=False)

    def create_buttons(self):
        buttonPause = self.dpg.add_button(label="Pause", id="Pause", callback=self.pause_callback)
        self.dpg.add_same_line()
        buttonResume = self.dpg.add_button(label="Resume", id="Resume", callback=self.resume_callback)
        self.dpg.add_same_line()
        buttonStop = self.dpg.add_button(label="Stop", id="Stop", callback=self.stop_callback)
        self.dpg.add_same_line()
        buttonRestart = self.dpg.add_button(label="Restart", id="Restart", callback=self.restart_callback)

    def pause_callback(self):
        self.timer.pause_timer()

    def resume_callback(self):
        self.timer.resume_timer()

    def stop_callback(self):
        # returns user to the settings
        # 1. stop the timer and gui thread
        self.timer.stop_timer()

        # 2. destroy the PomodoroTimer GUI
        self.dpg.delete_item(self.pomodoro_window)

        # 3. show the settings gui again
        self.dpg.show_item("Settings GUI")

    def restart_callback(self):
        # 1. resets the timer (in the Timer Class)
        self.timer.restart_timer()
        # 2. resets the counter for the pomodoro cycle (in the GUI Class)
        self.local_pomodoro_counter = 0
