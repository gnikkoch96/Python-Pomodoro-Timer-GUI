import threading
import configs
from timer import Timer
from playsound import playsound
from tools import Tools


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
        with self.dpg.window(tag=configs.POMODORO_WINDOW_ID,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width()) as timer_window:
            # todo cleanup
            # binds theme
            self.dpg.bind_item_theme(timer_window, configs.DEFAULT_THEME_ID)
            self.dpg.set_primary_window(timer_window, True)
            self.create_pomodoro_timer_gui_items()

    def create_pomodoro_timer_gui_items(self):
        # student studying image
        # todo might change this to a dynamic image
        with self.dpg.group(horizontal=True) as study_img:
            self.dpg.add_spacer(width=configs.POMODORO_STUDY_IMG_SPACER[0])
            Tools.add_and_load_image(self.dpg, configs.STUDYING_IMAGE_PATH, study_img)

        self.dpg.add_spacer(height=configs.POMODORO_DISPLAYS_SPACER[1])
        self.create_displays()

        self.dpg.add_spacer(height=configs.POMODORO_BUTTONS_SPACER[1])
        self.create_buttons()

        # binds fonts to timer
        self.dpg.bind_item_font(configs.POMODORO_MIN_FIELD_ID, configs.TIMER_FONT_TAG)
        self.dpg.bind_item_font(configs.POMODORO_SEC_FIELD_ID, configs.TIMER_FONT_TAG)

    def create_displays(self):
        with self.dpg.group(horizontal=True):
            # min display
            self.dpg.add_spacer(height=configs.POMODORO_MIN_DISPLAY_SPACER[1],
                                width=configs.POMODORO_MIN_DISPLAY_SPACER[0])
            self.dpg.add_input_text(label=configs.POMODORO_MIN_FIELD_LABEL,
                                    tag=configs.POMODORO_MIN_FIELD_ID,
                                    width=configs.POMODORO_DISPLAY_TEXT_DIMENSION[0],
                                    height=configs.POMODORO_DISPLAY_TEXT_DIMENSION[1],
                                    default_value=self.timer.get_min_value())
            self.dpg.configure_item(configs.POMODORO_MIN_FIELD_ID, enabled=False)

            # sec display
            self.dpg.add_spacer(width=35)
            self.dpg.add_input_text(label=configs.POMODORO_SEC_FIELD_LABEL,
                                    tag=configs.POMODORO_SEC_FIELD_ID,
                                    width=configs.POMODORO_DISPLAY_TEXT_DIMENSION[0],
                                    height=configs.POMODORO_DISPLAY_TEXT_DIMENSION[1],
                                    default_value=self.timer.get_sec_value())
            self.dpg.configure_item(configs.POMODORO_SEC_FIELD_ID, enabled=False)

        # pomodoro counter field
        self.dpg.add_spacer(height=configs.POMODORO_COUNTER_FIELD_SPACER[1])
        with self.dpg.group(horizontal=True):
            self.dpg.add_spacer(width=configs.POMODORO_COUNTER_FIELD_SPACER[0])
            self.dpg.add_input_text(label=configs.POMODORO_COUNTER_FIELD_LABEL,
                                    tag=configs.POMODORO_COUNTER_FIELD_ID,
                                    width=configs.POMODORO_COUNTER_FIELD_WIDTH,
                                    default_value=0)
            self.dpg.configure_item(configs.POMODORO_COUNTER_FIELD_ID, enabled=False)

    def create_buttons(self):
        with self.dpg.group(horizontal=True):
            # stop btn
            self.dpg.add_spacer(width=configs.POMODORO_BTN_SPACER[0])
            self.dpg.add_button(label=configs.POMODORO_STOP_BTN_LABEL,
                                tag=configs.POMODORO_STOP_BTN_ID,
                                callback=self.stop_callback)

            # restart btn
            self.dpg.add_button(label=configs.POMODORO_RESTART_BTN_LABEL,
                                tag=configs.POMODORO_RESTART_BTN_ID,
                                callback=self.restart_callback)

            # pause btn
            self.dpg.add_button(label=configs.POMODORO_PAUSE_BTN_LABEL,
                                tag=configs.POMODORO_PAUSE_BTN_ID,
                                callback=self.pause_callback)

            # resume btn
            self.dpg.add_button(label=configs.POMODORO_RESUME_BTN_LABEL,
                                tag=configs.POMODORO_RESUME_BTN_ID,
                                callback=self.resume_callback)

            self.dpg.hide_item(configs.POMODORO_RESUME_BTN_ID)

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
            playsound(configs.SOUND_PATH)

            # pomodoro_timer gui waits for user to press a button or close dialog
            self.event.wait()
            self.event.clear()
            self.dpg.delete_item(configs.POMODORO_FINISHED_WINDOW_ID)

            # todo remove when patched
            if self.dpg.does_alias_exist(configs.POMODORO_FINISHED_WINDOW_ID):
                self.dpg.remove_alias(configs.POMODORO_FINISHED_WINDOW_ID)

            if self.dpg.does_alias_exist(configs.POMODORO_FOCUS_BTN_ID):
                self.dpg.remove_alias(configs.POMODORO_FOCUS_BTN_ID)

            if self.dpg.does_alias_exist(configs.POMODORO_SMALL_BREAK_BTN_ID):
                self.dpg.remove_alias(configs.POMODORO_SMALL_BREAK_BTN_ID)

            if self.dpg.does_alias_exist(configs.POMODORO_LONG_BREAK_BTN_ID):
                self.dpg.remove_alias(configs.POMODORO_LONG_BREAK_BTN_ID)
                self.restart_threads()

    def update_min_and_sec(self):
        while not self.timer.timer_stop:
            if not self.dpg.is_dearpygui_running():
                break

            # if not self.dpg.is_dearpygui_running() or (self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0):
            #     break

            self.dpg.set_value(configs.POMODORO_MIN_FIELD_ID, self.timer.get_min_value())
            self.dpg.set_value(configs.POMODORO_SEC_FIELD_ID, self.timer.get_sec_value())

            if self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0:
                self.dpg.set_value(configs.POMODORO_SEC_FIELD_ID, 0)
                break

        # waits for values to be set before deleting window (to prevent updating errors)
        if self.timer.timer_stop:
            self.dpg.delete_item(configs.POMODORO_WINDOW_ID)

            # todo this is currently a workaround and could be fixed in the next update
            self.remove_aliases()

    def remove_aliases(self):
        # displays
        if self.dpg.does_alias_exist(configs.POMODORO_MIN_FIELD_ID):
            self.dpg.remove_alias(configs.POMODORO_MIN_FIELD_ID)

        if self.dpg.does_alias_exist(configs.POMODORO_SEC_FIELD_ID):
            self.dpg.remove_alias(configs.POMODORO_SEC_FIELD_ID)

        if self.dpg.does_alias_exist(configs.POMODORO_COUNTER_FIELD_ID):
            self.dpg.remove_alias(configs.POMODORO_COUNTER_FIELD_ID)

        # buttons
        if self.dpg.does_alias_exist(configs.POMODORO_PAUSE_BTN_ID):
            self.dpg.remove_alias(configs.POMODORO_PAUSE_BTN_ID)

        if self.dpg.does_alias_exist(configs.POMODORO_STOP_BTN_ID):
            self.dpg.remove_alias(configs.POMODORO_STOP_BTN_ID)

        if self.dpg.does_alias_exist(configs.POMODORO_RESTART_BTN_ID):
            self.dpg.remove_alias(configs.POMODORO_RESTART_BTN_ID)

        if self.dpg.does_alias_exist(configs.POMODORO_RESUME_BTN_ID):
            self.dpg.remove_alias(configs.POMODORO_RESUME_BTN_ID)

        # finished window
        if self.dpg.does_alias_exist(configs.POMODORO_FINISHED_WINDOW_ID):
            self.dpg.remove_alias(configs.POMODORO_FINISHED_WINDOW_ID)

        if self.dpg.does_alias_exist(configs.POMODORO_FOCUS_BTN_ID):
            self.dpg.remove_alias(configs.POMODORO_FOCUS_BTN_ID)

        if self.dpg.does_alias_exist(configs.POMODORO_SMALL_BREAK_BTN_ID):
            self.dpg.remove_alias(configs.POMODORO_SMALL_BREAK_BTN_ID)

        if self.dpg.does_alias_exist(configs.POMODORO_LONG_BREAK_BTN_ID):
            self.dpg.remove_alias(configs.POMODORO_LONG_BREAK_BTN_ID)

    def update_pomodoro_counters(self):
        pomodoro_counter = int(self.dpg.get_value(configs.POMODORO_COUNTER_FIELD_ID)) + 1
        self.local_pomodoro_counter = pomodoro_counter
        self.dpg.set_value(configs.POMODORO_COUNTER_FIELD_ID, str(pomodoro_counter))

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
        with self.dpg.window(tag=configs.POMODORO_FINISHED_WINDOW_ID,
                             on_close=self.focus_callback,
                             width=configs.POMODORO_FINISHED_WINDOW_DIMENSIONS[0],
                             height=configs.POMODORO_FINISHED_WINDOW_DIMENSIONS[1],
                             pos=configs.POMODORO_FINISHED_WINDOW_POS,
                             modal=True,
                             show=True):
            # finished image
            with self.dpg.group(horizontal=True):
                self.dpg.add_spacer(width=configs.POMODORO_FINISHED_IMG_SPACER[0])
                Tools.add_and_load_image(self.dpg, configs.FINISHED_IMAGE_PATH)

            self.create_buttons_for_finished_session()

    def create_buttons_for_finished_session(self):
        with self.dpg.group(parent=configs.POMODORO_FINISHED_WINDOW_ID,
                            horizontal=True):
            self.dpg.add_button(label=configs.POMODORO_FOCUS_BTN_LABEL,
                                tag=configs.POMODORO_FOCUS_BTN_ID,
                                callback=self.focus_callback)
            self.dpg.add_button(label=configs.POMODORO_SMALL_BREAK_BTN_LABEL,
                                tag=configs.POMODORO_SMALL_BREAK_BTN_ID,
                                callback=self.smallbreak_callback)
            self.dpg.add_button(label=configs.POMODORO_LONG_BREAK_BTN_LABEL,
                                tag=configs.POMODORO_LONG_BREAK_BTN_ID,
                                callback=self.longbreak_callback)

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
        self.dpg.hide_item(configs.POMODORO_PAUSE_BTN_ID)
        self.dpg.show_item(configs.POMODORO_RESUME_BTN_ID)
        self.timer.pause_timer()

    def resume_callback(self):
        # replaces replaces button with pause button
        self.dpg.show_item(configs.POMODORO_PAUSE_BTN_ID)
        self.dpg.hide_item(configs.POMODORO_RESUME_BTN_ID)
        self.timer.resume_timer()

    # returns user to the settings
    def stop_callback(self):
        # stop the timer and gui thread
        self.timer.stop_timer()

        # show the settings gui again
        self.dpg.show_item(configs.SETTINGS_WINDOW_ID)

    def restart_callback(self):
        # resets the timer (in the Timer Class)
        self.timer.restart_timer()

        # resets the counter for the pomodoro cycle (in the GUI Class)
        self.local_pomodoro_counter = 0
