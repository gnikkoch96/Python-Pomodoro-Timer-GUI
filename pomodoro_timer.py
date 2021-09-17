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
        self.timer = Timer(self.settings.get_focus_time())
        self.local_pomodoro_counter = 0
        # self.global_pomodoro_counter = 0

        self.isFinished = False  # used to disable the buttons until user closes the finished window screen

        with self.dpg.window(label="Pomdoro Timer",
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width()) as self.pomodoro_window:

            self.add_padding(280, 0, True)
            self.add_and_load_image("resources/images/studying.png")

            self.add_padding(125, 10, True)
            self.create_displays()

            self.add_padding(325, 100, True)
            self.create_buttons()

            self.dpg.set_item_font("Minute", "Timer Font")
            self.dpg.set_item_font("Second", "Timer Font")

        self.dpg.set_primary_window(self.pomodoro_window, value=True)

        self.event = threading.Event()
        self.pomodoro_timer_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.pomodoro_timer_thread.start()

    # this is a thread function used to update the gui with the timer min and sec values
    def update_gui(self):
        print("---Update Pomodoro Timer GUI Thread Started---")
        self.update_min_and_sec()

        # only add to counter if the timer finishes (not when the user presses stop or restart)
        if self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0:

            # only update counter if it was a focus session
            if self.timer.isFocus:
                self.update_pomodoro_counters()

            self.create_finished_dialog()

            # change the sound here
            playsound('resources/sounds/chime.wav', block=False)

            # pomodoro_timer gui waits for user to press a button or close dialog
            self.event.wait()
            self.event.clear()
            self.dpg.delete_item("FinishedWindow")
            self.restart_threads()

        print("---Update Pomodoro Timer GUI Thread Ended---")

    def update_min_and_sec(self):
        while not self.timer.timer_stop:
            # todo: there is probably a better way of doing this
            if not self.dpg.is_dearpygui_running():
                break

            if self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0:
                break

            self.dpg.set_value("Minute", self.timer.get_min_value())
            self.dpg.set_value("Second", self.timer.get_sec_value())

    def update_pomodoro_counters(self):
        # increments current pomodoro counter by 1
        pomodoro_counter = int(self.dpg.get_value("PomodoroCounter")) + 1
        self.local_pomodoro_counter = pomodoro_counter
        self.dpg.set_value("PomodoroCounter", str(pomodoro_counter))

        # self.global_pomodoro_counter = pomodoro_counter

    # restarts the timer and the gui threads
    def restart_threads(self):
        if self.timer.isFocus:
            mins = self.settings.get_focus_time()
        elif self.timer.isOnSmallBreak:
            mins = self.settings.get_small_break()
        else:
            mins = self.settings.get_long_break()

        self.timer = Timer(mins)

        self.pomodoro_timer_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.pomodoro_timer_thread.start()

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

    def create_finished_dialog(self):
        with self.dpg.window(label="Finished!",
                             modal=True,
                             show=True,
                             id="FinishedWindow",
                             on_close=self.focus_callback,
                             height=self.dpg.get_viewport_height() / 2,
                             width=self.dpg.get_viewport_width() / 2):
            self.add_padding(80, 0, True)
            self.add_and_load_image("resources/images/finished.png")

            self.add_padding(80, 40, True)
            self.create_buttons_for_finished_session()

    def create_displays(self):
        display_min_time = self.dpg.add_input_text(label="min",
                                                   id="Minute",
                                                   height=PomodoroTimer.DISPLAY_TEXT_WIDTH,
                                                   width=PomodoroTimer.DISPLAY_TEXT_WIDTH,
                                                   default_value=self.timer.get_min_value())
        self.dpg.configure_item(display_min_time, enabled=False)
        self.dpg.add_same_line()

        self.add_padding(50, 0, True)
        display_sec_time = self.dpg.add_input_text(label="sec",
                                                   id="Second",
                                                   height=PomodoroTimer.DISPLAY_TEXT_WIDTH,
                                                   width=PomodoroTimer.DISPLAY_TEXT_WIDTH,
                                                   default_value=self.timer.get_sec_value())
        self.dpg.configure_item(display_sec_time, enabled=False)

        self.add_padding(125, 50, True)
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

        if self.local_pomodoro_counter >= 4:
            self.dpg.add_same_line()
            buttonLongBreak = self.dpg.add_button(label="Long Break", id="LongBreak", callback=self.longbreak_callback)
        else:
            self.dpg.add_same_line()
            buttonSmallBreak = self.dpg.add_button(label="Small Break", id="SmallBreak",
                                                   callback=self.smallbreak_callback)

    def add_and_load_image(self, image_path, parent=None):
        width, height, channels, data = self.dpg.load_image(image_path)

        with self.dpg.texture_registry() as reg_id:
            texture_id = self.dpg.add_static_texture(width, height, data, parent=reg_id)

        if parent is None:
            return self.dpg.add_image(texture_id)
        else:
            return self.dpg.add_image(texture_id, parent=parent)

    def add_padding(self, width_value=0, height_value=0, is_same_line=False):
        if height_value != 0:
            self.dpg.add_dummy(height=height_value)

        if width_value != 0:
            self.dpg.add_dummy(width=width_value)

        if is_same_line:
            self.dpg.add_same_line()