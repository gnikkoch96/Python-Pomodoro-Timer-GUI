import threading
import pomodoro_settings
from timer import Timer
from playsound import playsound
from tools import Tools

# ids
POMODORO_WINDOW_ID = "Pomodoro Timer"
FINISHED_WINDOW_ID = "Finished Window"
POMODORO_COUNTER_FIELD_ID = "Pomodoro Counter"
MINUTE_FIELD_ID = "Minute"
SECOND_FIELD_ID = "Second"
PAUSE_BUTTON_ID = "Pause"
STOP_BUTTON_ID = "Stop"
RESTART_BUTTON_ID = "Restart"
RESUME_BUTTON_ID = "Resume"
FOCUS_BUTTON_ID = "Focus"
SMALL_BREAK_BUTTON_ID = "Small Break"
LONG_BREAK_BUTTON_ID = "Long Break"
CONFIG_THEME_ID = "config-theme"

# fonts
DEFAULT_FONT_TAG = "default"
TIMER_FONT_TAG = "timer-font"

# vars
SOUND_PATH = "resources/sounds/bell.mp3"
STUDYING_IMAGE_PATH = "resources/images/studying.png"
DISPLAY_TEXT_WIDTH = 200


# Description: this class handles the display of the timer to the user (how much mins and secs are left)
class PomodoroTimer:

    def __init__(self, dpg, settings):
        self.dpg = dpg
        self.settings = settings
        self.local_pomodoro_counter = 0
        
        # creates the timer thread
        self.timer = Timer(self.settings.get_focus_time())

        self.create_pomodoro_timer_gui_window()

        # threading and events
        self.event = threading.Event()
        self.pomodoro_timer_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.pomodoro_timer_thread.start()

    def create_pomodoro_timer_gui_window(self):
        with self.dpg.window(label="Pomodoro Timer",
                             tag=POMODORO_WINDOW_ID,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width()) as timer_window:
            self.dpg.bind_item_theme(timer_window, CONFIG_THEME_ID)
            self.create_pomodoro_timer_gui_items()
        
    def create_pomodoro_timer_gui_items(self):
        with self.dpg.group(horizontal=True) as study_img:
            self.dpg.add_spacer(width=280)
            Tools.add_and_load_image(self.dpg, STUDYING_IMAGE_PATH, study_img)

        self.dpg.add_spacer(height=25)
        self.create_displays()

        self.dpg.add_spacer(height=25)
        self.create_buttons()

        self.dpg.bind_item_font(MINUTE_FIELD_ID, "timer-font")
        self.dpg.bind_item_font(SECOND_FIELD_ID, "timer-font")

    def create_displays(self):
        with self.dpg.group(horizontal=True) as displays:
            self.dpg.add_spacer(height=10, width=125)
            self.dpg.add_input_text(label="min",
                                    tag=MINUTE_FIELD_ID,
                                    height=DISPLAY_TEXT_WIDTH,
                                    width=DISPLAY_TEXT_WIDTH,
                                    default_value=self.timer.get_min_value())
            self.dpg.configure_item(MINUTE_FIELD_ID, enabled=False)

            self.dpg.add_spacer(width=35)
            self.dpg.add_input_text(label="sec",
                                    tag=SECOND_FIELD_ID,
                                    height=DISPLAY_TEXT_WIDTH,
                                    width=DISPLAY_TEXT_WIDTH,
                                    default_value=self.timer.get_sec_value())
            self.dpg.configure_item(SECOND_FIELD_ID, enabled=False)

        self.dpg.add_spacer(height=75)
        with self.dpg.group(horizontal=True) as pomodoro_counter:
            self.dpg.add_spacer(width=125)
            self.dpg.add_input_text(label="Pomodoros",
                                    tag=POMODORO_COUNTER_FIELD_ID,
                                    width=550,
                                    default_value=0)
            self.dpg.configure_item(POMODORO_COUNTER_FIELD_ID, enabled=False)

    def create_buttons(self):
        with self.dpg.group(horizontal=True) as func_buttons:
            self.dpg.add_spacer(width=300)
            self.dpg.add_button(label="Stop", tag=STOP_BUTTON_ID, callback=self.stop_callback)

            self.dpg.add_button(label="Restart", tag=RESTART_BUTTON_ID, callback=self.restart_callback)

            self.dpg.add_button(label="Pause", tag=PAUSE_BUTTON_ID, callback=self.pause_callback)

            self.dpg.add_button(label="Resume", tag=RESUME_BUTTON_ID, callback=self.resume_callback)

            self.dpg.hide_item(RESUME_BUTTON_ID)

    # this is a thread function used to update the gui with the timer min and sec values
    def update_gui(self):
        self.update_min_and_sec()

        # only add to counter if the timer finishes (not when the user presses stop or restart)
        if self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0:

            # only update counter if it was a focus session
            if self.timer.isFocus:
                self.update_pomodoro_counters()

            self.create_finished_dialog()

            # change the sound here (block allows the program to continue w/o waiting for sound to finish)
            playsound(SOUND_PATH)

            # pomodoro_timer gui waits for user to press a button or close dialog
            self.event.wait()
            self.event.clear()
            self.dpg.delete_item(FINISHED_WINDOW_ID)
            self.restart_threads()

    def update_min_and_sec(self):
        while not self.timer.timer_stop:
            if not self.dpg.is_dearpygui_running() or (self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0):
                break

            self.dpg.set_value(MINUTE_FIELD_ID, self.timer.get_min_value())
            self.dpg.set_value(SECOND_FIELD_ID, self.timer.get_sec_value())

        # waits for values to be set before deleting window (to prevent updating errors)
        if self.timer.timer_stop:
            self.dpg.delete_item(POMODORO_WINDOW_ID)

    def update_pomodoro_counters(self):
        pomodoro_counter = int(self.dpg.get_value(POMODORO_COUNTER_FIELD_ID)) + 1
        self.local_pomodoro_counter = pomodoro_counter
        self.dpg.set_value(POMODORO_COUNTER_FIELD_ID, str(pomodoro_counter))

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

    def create_finished_dialog(self):
        with self.dpg.window(label="Finished!",
                             id=FINISHED_WINDOW_ID,
                             on_close=self.focus_callback,
                             height=self.dpg.get_viewport_height() / 2,
                             width=self.dpg.get_viewport_width() / 2,
                             modal=True,
                             show=True) as finished_win:
            
            self.dpg.bind_item_theme(finished_win, CONFIG_THEME_ID)
            with self.dpg.group(horizontal=True) as finished_img:
                self.dpg.add_spacer(width=80)
                Tools.add_and_load_image(self.dpg, "resources/images/finished.png")

            self.create_buttons_for_finished_session()

    def create_buttons_for_finished_session(self):
        with self.dpg.group(parent=FINISHED_WINDOW_ID,
                            horizontal=True):
            self.dpg.add_spacer(width=80)
            self.dpg.add_button(label="Focus Time", tag=FOCUS_BUTTON_ID, callback=self.focus_callback)

            if self.local_pomodoro_counter >= 4:
                self.dpg.add_button(label="Long Break", tag=LONG_BREAK_BUTTON_ID, callback=self.longbreak_callback)
            else:
                self.dpg.add_button(label="Small Break", tag=SMALL_BREAK_BUTTON_ID,
                                    callback=self.smallbreak_callback)

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
        # replaces pause button with resume button
        self.dpg.hide_item(PAUSE_BUTTON_ID)
        self.dpg.show_item(RESUME_BUTTON_ID)
        self.timer.pause_timer()

    def resume_callback(self):
        # replaces replaces button with pause button
        self.dpg.show_item(PAUSE_BUTTON_ID)
        self.dpg.hide_item(RESUME_BUTTON_ID)
        self.timer.resume_timer()

    # returns user to the settings
    def stop_callback(self):
        # 1. stop the timer and gui thread
        self.timer.stop_timer()

        # 2. pomodoro timer window is deleted in the update to prevent item not found errors

        # 3. show the settings gui again
        self.dpg.show_item(pomodoro_settings.SETTINGS_WINDOW_ID)

    def restart_callback(self):
        # 1. resets the timer (in the Timer Class)
        self.timer.restart_timer()

        # 2. resets the counter for the pomodoro cycle (in the GUI Class)
        self.local_pomodoro_counter = 0
