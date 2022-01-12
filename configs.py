# desc: contains all of the ids and values user in the program for efficient updates

# IDS-----------------------------------------------------------------

# fonts
DEFAULT_FONT_ID = "default"
TIMER_FONT_ID = "timer font"

# themes
DEFAULT_THEME_ID = "default theme"
POPUP_THEME_ID = "popup theme"

# settings window
SETTINGS_WINDOW_ID = "Settings GUI"
SETTINGS_FOCUS_COMBO_ID = "Focus Timer Combo"
SETTINGS_SMALL_BREAK_COMBO_ID = "Small Break Combo"
SETTINGS_LONG_BREAK_COMBO_ID = "Long Break Combo"
SETTINGS_START_BUTTON_ID = "Start"

# settings data window
SETTINGS_DATA_BTN_ID = "Data Button"
SETTINGS_DATA_WINDOW_ID = "Data Window"
SETTINGS_DATA_WINDOW_MINS_FIELD_ID = "Data Total Mins"
SETTINGS_DATA_WINDOW_POMODOROS_FIELD_ID = "Data Total Pomodoro"
SETTINGS_DATA_WINDOW_CLOSE_BTN_ID = "Close Button"

# pomodoro timer window
POMODORO_WINDOW_ID = "Pomodoro Timer"
POMODORO_FINISHED_WINDOW_ID = "Finished Window"
POMODORO_COUNTER_FIELD_ID = "Pomodoro Counter"
POMODORO_MIN_FIELD_ID = "Min"
POMODORO_SEC_FIELD_ID = "Second"
POMODORO_PAUSE_BTN_ID = "Pause"
POMODORO_STOP_BTN_ID = "Stop"
POMODORO_RESTART_BTN_ID = "Restart"
POMODORO_RESUME_BTN_ID = "Resume"
POMODORO_FOCUS_BTN_ID = "Focus btn"
POMODORO_SMALL_BREAK_BTN_ID = "Small Break"
POMODORO_LONG_BREAK_BTN_ID = "Long Break"

# VALUES--------------------------------------------------------------
# path files
DEFAULT_FONT_PATH = "resources/fonts/Simpleton-Gothic.ttf"
TIMER_FONT_PATH = "resources/fonts/Simpleton-Gothic.ttf"
BANNER_IMG_PATH = "resources/images/tomato-banner.png"
SOUND_PATH = "resources/sounds/bell.mp3"
STUDYING_IMAGE_PATH = "resources/images/studying.png"
FINISHED_IMAGE_PATH = "resources/images/finished.png"
RELAXING_IMAGE_PATH = "resources/images/relaxing.png"
ICON_PATH = "resources/images/tomato.ico"

# user data
USERDATA_FILEPATH = "user_data.json"
USERDATA_FOCUS_MINS = "focus_time"
USERDATA_SMALLBREAK_MINS = "small_break"
USERDATA_LONGBREAK_MINS = "long_break"
USERDATA_TOTAL_FOCUS_MINS = "total_mins"
USERDATA_TOTAL_POMODOROS = "total_poms"
USERDATA_DATE = 'date'

# main
VIEWPORT_HEIGHT = 700
VIEWPORT_WIDTH = 1000
DPG_FONT_SCALE = 1.25
VIEWPORT_TITLE = "Nikko's Pomodoro Timer"

# toast notification
TOAST_ERROR_MSG = "Notifications work for win 10 only"
TOAST_TITLE = "Pomodoro Timer"
TOAST_FOCUS_DONE_MSG = "Pomodoro Session Completed!"
TOAST_BREAK_DONE_MSG = "Break Completed"
TOAST_DURATION = 5

# settings window
SETTINGS_START_BUTTON_LABEL = "Start Pomodoro"
SETTINGS_FOCUS_COMBO_TOOLTIP = "Number of mins to stay focused"
SETTINGS_SMALL_BREAK_COMBO_TOOLTIP = "Number of mins for a small break"
SETTINGS_LONG_BREAK_COMBO_TOOLTIP = "Number of mins for a long break"
SETTINGS_START_BTN_TOOLTIP = "Start Pomodoro Session"
SETTINGS_COMBO_WIDTH = 400
SETTINGS_COMBO_HEIGHT_PADDING = 15
SETTINGS_FOCUS_COMBO_DEFAULT_VALUE = 25
SETTINGS_SMALL_BREAK_COMBO_DEFAULT_VALUE = 2
SETTINGS_LONG_BREAK_COMBO_DEFAULT_VALUE = 15
SETTINGS_BANNER_HEIGHT_SPACER = 20
SETTINGS_BANNER_WIDTH_SPACER = 30
SETTINGS_COMBOS_HEIGHT_SPACER = 25
SETTINGS_COMBOS_WIDTH_SPACER = 275
SETTINGS_START_BTN_WIDTH_SPACER = 100
SETTINGS_START_BUTTON_HEIGHT = 100
SETTINGS_START_BUTTON_WIDTH = 200
SETTINGS_CONFIG_WINDOW_DIMENSIONS = [800, 300]

# settings data window
SETTINGS_DATA_BTN_LABEL = "Check User Data"
SETTINGS_DATA_WINDOW_LABEL = "User Data"
SETTINGS_DATA_WINDOW_MINS_FIELD_LABEL = "Total Focus Mins"
SETTINGS_DATA_WINDOW_POMODOROS_FIELD_LABEL = "Total Pomodoros Done"
SETTINGS_DATA_WINDOW_CLOSE_BTN_LABEL = "Close"
SETTINGS_DATA_BTN_SPACER = [450, 0]
SETTINGS_DATA_WINDOW_DIMENSIONS = [VIEWPORT_WIDTH / 2, VIEWPORT_HEIGHT / 2]
SETTINGS_DATA_WINDOW_POS = [VIEWPORT_WIDTH / 2 - SETTINGS_DATA_WINDOW_DIMENSIONS[0] / 2,
                            VIEWPORT_HEIGHT / 2 - SETTINGS_DATA_WINDOW_DIMENSIONS[1] / 2]
SETTINGS_DATA_WINDOW_MINS_FIELD_SPACER = [SETTINGS_DATA_WINDOW_DIMENSIONS[0] / 7, 25]
SETTINGS_DATA_WINDOW_POMODOROS_FIELD_SPACER = [SETTINGS_DATA_WINDOW_DIMENSIONS[0] / 7, 50]
SETTINGS_DATA_WINDOW_CLOSE_BTN_SPACER = [SETTINGS_DATA_WINDOW_DIMENSIONS[0] / 2.6, 50]

# pomodoro timer window
POMODORO_MIN_FIELD_LABEL = "min"
POMODORO_SEC_FIELD_LABEL = "sec"
POMODORO_COUNTER_FIELD_LABEL = "Pomodoros"
POMODORO_FOCUS_BTN_LABEL = "Focus Time"
POMODORO_SMALL_BREAK_BTN_LABEL = "Small Break"
POMODORO_LONG_BREAK_BTN_LABEL = "Long Break"
POMODORO_STOP_BTN_LABEL = "Stop"
POMODORO_RESTART_BTN_LABEL = "Restart"
POMODORO_PAUSE_BTN_LABEL = "Pause"
POMODORO_RESUME_BTN_LABEL = "Resume"
POMODORO_STUDY_IMG_SPACER = [295, 0]  # WIDTH, HEIGHT (them same for the rest)
POMODORO_DISPLAYS_SPACER = [0, 25]
POMODORO_MIN_DISPLAY_SPACER = [125, 10]
POMODORO_SEC_DISPLAY_SPACER = [35, 0]
POMODORO_BUTTONS_SPACER = [0, 25]
POMODORO_COUNTER_FIELD_SPACER = [125, 75]
POMODORO_BTN_SPACER = [300, 0]
POMODORO_FINISHED_IMG_SPACER = [80, 0]
POMODORO_FINISHED_WINDOW_DIMENSIONS = [VIEWPORT_WIDTH / 2, VIEWPORT_HEIGHT / 2.5]
POMODORO_DISPLAY_TEXT_DIMENSION = [200, 200]
POMODORO_FINISHED_WINDOW_POS = [VIEWPORT_WIDTH/2 - POMODORO_FINISHED_WINDOW_DIMENSIONS[0] / 2,
                                VIEWPORT_HEIGHT/2 - POMODORO_FINISHED_WINDOW_DIMENSIONS[1] / 2]
POMODORO_COUNTER_FIELD_WIDTH = 550
