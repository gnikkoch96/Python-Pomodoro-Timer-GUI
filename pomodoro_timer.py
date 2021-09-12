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
        with self.dpg.window(label="Pomdoro Timer",
                        height=self.dpg.get_viewport_height(),
                        width=self.dpg.get_viewport_width()) as self.pomodoro_window:
            self.create_displays()
            self.create_buttons()

        self.dpg.set_primary_window(self.pomodoro_window, value=True)

        # creates a new thread
        self.pomodoro_timer_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.pomodoro_timer_thread.start()

    def update_gui(self):  # this is a thread function used to update the gui with the timer min and sec values
        print("---Update Pomodoro Timer GUI Thread Started---")
        while not self.timer.timer_stop and (self.timer.get_min_value() >= 0 and self.timer.get_sec_value() >= 0):
            if self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0:
                break

            self.dpg.set_value("Minute", self.timer.get_min_value())
            self.dpg.set_value("Second", self.timer.get_sec_value())



        # only add to counter if the timer finishes (not when the user presses stop or restart)
        if self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0:
            pomodoro_counter = int(self.dpg.get_value("PomodoroCounter")) + 1
            self.local_pomodoro_counter = pomodoro_counter
            self.global_pomodoro_counter = pomodoro_counter
            self.dpg.set_value("PomodoroCounter", str(pomodoro_counter))

            # create a new window for the finished session
            with self.dpg.window(label="Pomodoro Timer Finished!",
                                 id="FinishedWindow",
                                 height=self.dpg.get_viewport_height() / 2,
                                 width=self.dpg.get_viewport_width() / 2) as finished_session_window:
                self.create_buttons_for_finished_session()
                # todo: implement playing of sound here

        print("---Update Pomodoro Timer GUI Thread Ended---")

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

    def create_buttons_for_finished_session(self):
        buttonFocus = self.dpg.add_button(label="Focus Time", id="Focus", callback=self.focus_callback)
        self.dpg.add_same_line()
        buttonSmallBreak = self.dpg.add_button(label="Small Break", id="SmallBreak", callback=self.smallbreak_callback)
        if self.local_pomodoro_counter >= 4:
            self.dpg.add_same_line()
            buttonLongBreak = self.dpg.add_button(label="Long Break", id="LongBreak", callback=self.longbreak_callback)

    def focus_callback(self):
        # creates a new timer thread
        self.timer = Timer(self.settings.get_focus_time(),
                           self.settings.get_small_break(),
                           self.settings.get_long_break())

        # creates a new thread to update the gui
        self.pomodoro_timer_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.pomodoro_timer_thread.start()

        self.dpg.delete_item("FinishedWindow")
        self.timer.isOnLongBreak = False
        self.timer.isFocus = True
        self.timer.isOnSmallBreak = False

    def smallbreak_callback(self):
        self.timer = Timer(self.settings.get_focus_time(),
                           self.settings.get_small_break(),
                           self.settings.get_long_break())

        self.pomodoro_timer_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.pomodoro_timer_thread.start()

        self.dpg.delete_item("FinishedWindow")
        self.timer.isOnLongBreak = False
        self.timer.isFocus = False
        self.timer.isOnSmallBreak = True

    def longbreak_callback(self):
        self.timer = Timer(self.settings.get_focus_time(),
                           self.settings.get_small_break(),
                           self.settings.get_long_break())

        self.pomodoro_timer_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.pomodoro_timer_thread.start()

        self.dpg.delete_item("FinishedWindow")

        # I'll let the user choose when to take a long break only after they have at least 4 focus sessions
        self.local_pomodoro_counter = 0
        self.timer.isOnLongBreak = True
        self.timer.isFocus = False
        self.timer.isOnSmallBreak = False

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
        self.dpg.set_primary_window("Settings GUI", value=True)


    def restart_callback(self):
        # 1. resets the timer (in the Timer Class)
        self.timer.restart_timer()
        # 2. resets the counter for the pomodoro cycle (in the GUI Class)
        self.local_pomodoro_counter = 0
