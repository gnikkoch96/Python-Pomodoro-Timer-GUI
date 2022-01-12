import threading
import configs
from timer import Timer
from playsound import playsound
from tools import Tools


# desc: loads the timer gui
class PomodoroTimer:
    def __init__(self, dpg, settings, user_data):
        self.dpg = dpg
        self.user_data = user_data
        self.settings = settings

        # todo cleanup used to change img indicator of the current activity (focus or small break)
        self.study_img = None
        self.relax_img = None

        # bool flags to tell what the current activity is
        self.isFocus = True
        self.isOnSmallBreak = False
        self.isOnLongBreak = False

        # retrieves the current day's num of pomodoros
        try:
            self.local_pomodoro_counter = self.user_data[configs.USERDATA_DATE][Tools.get_current_day()]
        except KeyError:
            self.user_data[configs.USERDATA_DATE][Tools.get_current_day()] = 0
            self.local_pomodoro_counter = self.user_data[configs.USERDATA_DATE][Tools.get_current_day()]

        # update json file
        Tools.update_user_data(self.user_data)

        # starts the timer.py thread
        self.timer = Timer(self.settings.get_focus_time())

        self.create_pomodoro_timer_gui_window()

        # threading and events
        self.event = threading.Event()

        # starts the timer gui thread
        self.pomodoro_timer_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.pomodoro_timer_thread.start()

    def create_pomodoro_timer_gui_window(self):
        with self.dpg.window(tag=configs.POMODORO_WINDOW_ID,
                             height=self.dpg.get_viewport_height(),
                             width=self.dpg.get_viewport_width()) as timer_window:
            self.dpg.bind_item_theme(timer_window, configs.DEFAULT_THEME_ID)
            self.dpg.set_primary_window(timer_window, True)
            self.create_pomodoro_timer_gui_items()

    def create_pomodoro_timer_gui_items(self):
        # student studying image
        with self.dpg.group(horizontal=True) as self.study_img:
            self.dpg.add_spacer(width=configs.POMODORO_STUDY_IMG_SPACER[0])
            Tools.add_and_load_image(self.dpg, configs.STUDYING_IMAGE_PATH, self.study_img)

        # person relaxing image
        with self.dpg.group(horizontal=True) as self.relax_img:
            self.dpg.add_spacer(width=configs.POMODORO_STUDY_IMG_SPACER[0])
            Tools.add_and_load_image(self.dpg, configs.RELAXING_IMAGE_PATH, self.relax_img)

        # hidden in the beginning and only appears when user is on a small/long break
        self.dpg.hide_item(self.relax_img)

        # load min, sec, and pomodoro displays
        self.dpg.add_spacer(height=configs.POMODORO_DISPLAYS_SPACER[1])
        self.create_displays()

        # load the timer buttons
        self.dpg.add_spacer(height=configs.POMODORO_BUTTONS_SPACER[1])
        self.create_buttons()

        # binds fonts to timer
        self.dpg.bind_item_font(configs.POMODORO_MIN_FIELD_ID, configs.TIMER_FONT_ID)
        self.dpg.bind_item_font(configs.POMODORO_SEC_FIELD_ID, configs.TIMER_FONT_ID)

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
                                    default_value=self.local_pomodoro_counter)
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

            # resume appears only when pause is pressed
            self.dpg.hide_item(configs.POMODORO_RESUME_BTN_ID)

    def update_gui(self):
        self.update_min_and_sec()

        # timer is finished
        if self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0:
            # only update counter if it was a focus session
            if self.isFocus:
                self.update_pomodoro_counters()

                # update user data
                self.update_data_file()

            # change the sound here (block allows the program to continue w/o waiting for sound to finish)
            playsound(configs.SOUND_PATH, block=False)

            self.create_finished_dialog()

            # display toast
            if self.isFocus:
                message = configs.TOAST_FOCUS_DONE_MSG
            else:
                message = configs.TOAST_BREAK_DONE_MSG
            threading.Thread(target=Tools.display_win10_notif, daemon=True, args=(configs.TOAST_TITLE,
                                                                                  message,
                                                                                  configs.TOAST_DURATION)).start()

            # pomodoro_timer gui waits for user to press a button or close dialog
            self.event.wait()
            self.event.clear()
            self.dpg.delete_item(configs.POMODORO_FINISHED_WINDOW_ID)

            self.cleanup_finished_win_aliases()
            self.restart_threads()

    def cleanup_finished_win_aliases(self):
        if self.dpg.does_alias_exist(configs.POMODORO_FINISHED_WINDOW_ID):
            self.dpg.remove_alias(configs.POMODORO_FINISHED_WINDOW_ID)

        if self.dpg.does_alias_exist(configs.POMODORO_FOCUS_BTN_ID):
            self.dpg.remove_alias(configs.POMODORO_FOCUS_BTN_ID)

        if self.dpg.does_alias_exist(configs.POMODORO_SMALL_BREAK_BTN_ID):
            self.dpg.remove_alias(configs.POMODORO_SMALL_BREAK_BTN_ID)

        if self.dpg.does_alias_exist(configs.POMODORO_LONG_BREAK_BTN_ID):
            self.dpg.remove_alias(configs.POMODORO_LONG_BREAK_BTN_ID)

    def update_min_and_sec(self):
        while not self.timer.timer_stop:
            # prevents thread from continuing
            if not self.dpg.is_dearpygui_running():
                break

            self.dpg.set_value(configs.POMODORO_MIN_FIELD_ID, self.timer.get_min_value())
            self.dpg.set_value(configs.POMODORO_SEC_FIELD_ID, self.timer.get_sec_value())

            # todo quick fix as the gui is behind timer by one second
            if self.timer.get_min_value() <= 0 and self.timer.get_sec_value() <= 0:
                self.dpg.set_value(configs.POMODORO_SEC_FIELD_ID, 0)
                break

        # waits for values to be set before deleting window (to prevent updating errors)
        if self.timer.timer_stop:
            self.dpg.delete_item(configs.POMODORO_WINDOW_ID)
            self.cleanup_pomodoro_win_aliases()

    def update_data_file(self):
        # update the values
        self.user_data[configs.USERDATA_TOTAL_FOCUS_MINS] += self.settings.get_focus_time()
        self.user_data[configs.USERDATA_TOTAL_POMODOROS] += 1

        # update json file
        Tools.update_user_data(self.user_data)

    def cleanup_pomodoro_win_aliases(self):
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
        # increment pomodoro counter
        pomodoro_counter = int(self.dpg.get_value(configs.POMODORO_COUNTER_FIELD_ID)) + 1
        self.local_pomodoro_counter = pomodoro_counter

        # update json
        self.user_data[configs.USERDATA_DATE][Tools.get_current_day()] = self.local_pomodoro_counter
        Tools.update_user_data(self.user_data)

        # update the pomodoro field display
        self.dpg.set_value(configs.POMODORO_COUNTER_FIELD_ID, str(pomodoro_counter))

    # restarts the timer and the gui threads
    def restart_threads(self):
        if self.isFocus:
            mins = self.settings.get_focus_time()
        elif self.isOnSmallBreak:
            mins = self.settings.get_small_break()
        else:
            mins = self.settings.get_long_break()

        self.timer = Timer(mins)
        self.pomodoro_timer_thread = threading.Thread(target=self.update_gui, daemon=True)
        self.pomodoro_timer_thread.start()

    def create_finished_dialog(self):
        with self.dpg.window(tag=configs.POMODORO_FINISHED_WINDOW_ID,
                             width=configs.POMODORO_FINISHED_WINDOW_DIMENSIONS[0],
                             height=configs.POMODORO_FINISHED_WINDOW_DIMENSIONS[1],
                             pos=configs.POMODORO_FINISHED_WINDOW_POS,
                             no_title_bar=True,
                             no_move=True,
                             modal=True,
                             show=True):
            self.dpg.bind_item_theme(configs.POMODORO_FINISHED_WINDOW_ID, configs.POPUP_THEME_ID)

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
        self.update_img_indicator(True)

        self.isOnLongBreak = False
        self.isFocus = True
        self.isOnSmallBreak = False

    def smallbreak_callback(self):
        self.event.set()
        self.update_img_indicator(False)

        self.isOnLongBreak = False
        self.isFocus = False
        self.isOnSmallBreak = True

    def longbreak_callback(self):
        self.event.set()
        self.update_img_indicator(False)

        self.isOnLongBreak = True
        self.isFocus = False
        self.isOnSmallBreak = False

    # updates the main img to indicate focus or break time
    def update_img_indicator(self, is_focus):
        if is_focus:
            self.dpg.show_item(self.study_img)
            self.dpg.hide_item(self.relax_img)
        else:
            self.dpg.hide_item(self.study_img)
            self.dpg.show_item(self.relax_img)

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
