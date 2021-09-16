import threading
from timer import Timer
from playsound import playsound


# Pomodoro_Timer used to handle/create the GUI for the timer
class PomodoroTimer:
    # static vars
    DISPLAY_TEXT_WIDTH = 200  # width

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

            # padding
            self.dpg.add_dummy(width=280)
            self.dpg.add_same_line()
            self.add_and_load_image("resources/images/studying.png")

            # padding
            self.dpg.add_dummy(height=10)
            self.dpg.add_dummy(width=125)
            self.dpg.add_same_line()
            self.create_displays()

            # padding
            self.dpg.add_dummy(height=100)
            self.dpg.add_dummy(width=325)
            self.dpg.add_same_line()

            self.create_buttons()

            # apply fonts to items
            self.dpg.set_item_font("Minute", "Timer Font")
            self.dpg.set_item_font("Second", "Timer Font")

        self.dpg.set_primary_window(self.pomodoro_window, value=True)

        # creates a new thread
        self.event = threading.Event()
        self.pomodoro_timer_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.pomodoro_timer_thread.start()

    def update_gui(self):  # this is a thread function used to update the gui with the timer min and sec values
        print("---Update Pomodoro Timer GUI Thread Started---")
        self.update_min_and_sec()

        # only add to counter if the timer finishes (not when the user presses stop or restart)
        if self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0:
            self.update_pomodoro_counters()

            # create a new window for the finished session
            with self.dpg.window(label="Pomodoro Timer Finished!",
                                 id="FinishedWindow",
                                 height=self.dpg.get_viewport_height() / 2,
                                 width=self.dpg.get_viewport_width() / 2) as finished_session_window:
                self.create_buttons_for_finished_session()
                playsound('resources/sounds/chime.wav')
            self.dpg.set_item_theme(finished_session_window, "Red")
            self.event.wait()  # waits for the user to press one of the buttons
            self.event.clear()
            self.dpg.delete_item(finished_session_window)
            self.restart_threads()

        print("---Update Pomodoro Timer GUI Thread Ended---")

    def update_min_and_sec(self):
        while not self.timer.timer_stop and (self.timer.get_min_value() >= 0 and self.timer.get_sec_value() >= 0):
            if self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0:
                break

            self.dpg.set_value("Minute", self.timer.get_min_value())
            self.dpg.set_value("Second", self.timer.get_sec_value())
            
    def update_pomodoro_counters(self):
        pomodoro_counter = int(self.dpg.get_value("PomodoroCounter")) + 1
        self.local_pomodoro_counter = pomodoro_counter
        self.global_pomodoro_counter = pomodoro_counter
        self.dpg.set_value("PomodoroCounter", str(pomodoro_counter))

    def restart_threads(self):
        # restarts the timer and the gui threads
        # creates a new timer thread
        self.timer = Timer(self.settings.get_focus_time(),
                           self.settings.get_small_break(),
                           self.settings.get_long_break())

        # creates a new thread to update the gui
        self.pomodoro_timer_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.pomodoro_timer_thread.start()

    def create_displays(self):
        display_min_time = self.dpg.add_input_text(label="min",
                                                   id="Minute",
                                                   height=PomodoroTimer.DISPLAY_TEXT_WIDTH,
                                                   width=PomodoroTimer.DISPLAY_TEXT_WIDTH,
                                                   default_value=self.timer.get_min_value())
        self.dpg.configure_item(display_min_time, enabled=False)
        self.dpg.add_same_line()

        # padding
        self.dpg.add_dummy(width=50)
        self.dpg.add_same_line()

        display_sec_time = self.dpg.add_input_text(label="sec",
                                                   id="Second",
                                                   height=PomodoroTimer.DISPLAY_TEXT_WIDTH,
                                                   width=PomodoroTimer.DISPLAY_TEXT_WIDTH,
                                                   default_value=self.timer.get_sec_value())
        self.dpg.configure_item(display_sec_time, enabled=False)

        # padding
        self.dpg.add_dummy(height=50)
        self.dpg.add_dummy(width=125)
        self.dpg.add_same_line()

        display_pomodoro_counter = self.dpg.add_input_text(label="# of Pomodoros",
                                                           id="PomodoroCounter",
                                                           width=550,
                                                           default_value=0)  # later on default value will be read from a file
        self.dpg.configure_item(display_pomodoro_counter, enabled=False)

    def create_buttons(self):
        buttonStop = self.dpg.add_button(label="Stop", id="Stop", callback=self.stop_callback)
        self.dpg.add_same_line()
        buttonRestart = self.dpg.add_button(label="Restart", id="Restart", callback=self.restart_callback)
        self.dpg.add_same_line()
        buttonPause = self.dpg.add_button(label="Pause", id="Pause", callback=self.pause_callback)
        self.dpg.add_same_line()
        buttonResume = self.dpg.add_button(label="Resume", id="Resume", callback=self.resume_callback)
        self.dpg.hide_item(buttonResume)

    def create_buttons_for_finished_session(self):
        buttonFocus = self.dpg.add_button(label="Focus Time", id="Focus", callback=self.focus_callback)
        self.dpg.add_same_line()
        buttonSmallBreak = self.dpg.add_button(label="Small Break", id="SmallBreak", callback=self.smallbreak_callback)
        if self.local_pomodoro_counter >= 4:
            self.dpg.add_same_line()
            buttonLongBreak = self.dpg.add_button(label="Long Break", id="LongBreak", callback=self.longbreak_callback)

    def add_and_load_image(self, image_path, parent=None):
        print(type(self.dpg.load_image(image_path)))
        width, height, channels, data = self.dpg.load_image(image_path)

        with self.dpg.texture_registry() as reg_id:
            texture_id = self.dpg.add_static_texture(width, height, data, parent=reg_id)

        if parent is None:
            return self.dpg.add_image(texture_id)
        else:
            return self.dpg.add_image(texture_id, parent=parent)

    def focus_callback(self):
        self.event.set()

        self.timer.isOnLongBreak = False
        self.timer.isFocus = True
        self.timer.isOnSmallBreak = False

    def smallbreak_callback(self):
        self.event.set()

        self.timer.isOnLongBreak = False
        self.timer.isFocus = False
        self.timer.isOnSmallBreak = True

    def longbreak_callback(self):
        self.event.set()

        # I'll let the user choose when to take a long break only after they have at least 4 focus sessions
        self.local_pomodoro_counter = 0
        self.timer.isOnLongBreak = True
        self.timer.isFocus = False
        self.timer.isOnSmallBreak = False

    def pause_callback(self):
        self.dpg.hide_item("Pause")
        self.dpg.show_item("Resume")
        self.timer.pause_timer()

    def resume_callback(self):
        self.dpg.show_item("Pause")
        self.dpg.hide_item("Resume")
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
