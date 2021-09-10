import threading
import time


# Timer class used to handle the timer functionalities
class Timer:
    # initialize the timer with mins
    def __init__(self, focus_mins, small_break_mins, long_break_mins):
        # initialize values
        self.focus_mins = focus_mins
        self.small_break_mins = small_break_mins
        self.long_break_mins = long_break_mins
        self.sec = 0

        # boolean logic to control timer thread
        self.timer_pause = False
        self.timer_stop = False
        self.timer_restart = False

        # threading related
        self.timer_event = threading.Event()
        self.timer_thread = threading.Thread(target=self.start_timer, daemon=True)
        self.timer_thread.start()

    def start_timer(self):
        # continue the timer until user stops, pauses, or restarts the timer
        # and when the timer has not finished
        while not (self.timer_stop or self.timer_restart) and (self.focus_mins >= 0 and self.sec >= 0):
            if self.timer_pause:
                self.timer_event.wait()
                self.timer_event.clear()
            else:
                if self.sec <= 0:
                    if self.focus_mins - 1 >= 0:
                        self.focus_mins -= 1
                        self.sec = 60
                else:
                    self.sec -= 1
                    time.sleep(1)
                # print(self.mins, " min\n", self.sec, " sec")

    def restart_timer(self):
        # ends the timer thread
        # 1. resets the timer (in the Timer Class)
        # 2. resets the counter for the pomodoro cycle (in the GUI Class)
        self.timer_restart = True
        print("Timer Thread ended")

    def stop_timer(self):
        # ends the timer thread
        self.timer_stop = True
        print("Timer Thread ended")

    def pause_timer(self):
        # pauses the timer thread
        # 1. pauses the timer
        self.timer_pause = True
        print("Timer Thread paused")

    def resume_timer(self):
        # continues the timer thread (if pause was initiated)
        self.timer_pause = False
        self.timer_event.set()  # triggers the timer to continue again
        print("Timer Thread continues")

    def get_min_value(self):
        return self.focus_mins

    def get_sec_value(self):
        return self.sec
