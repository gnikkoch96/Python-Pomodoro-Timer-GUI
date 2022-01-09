import threading
import time


# Description: handles the thread for updating timer values (which gets grabbed from the timer GUI)
class Timer:
    def __init__(self, mins):
        self.mins = mins
        self.sec = 0

        # used to restore min value to original (restart action)
        self.mins_copy = mins

        self.timer_pause = False
        self.timer_stop = False
        self.timer_restart = False

        # initially the timer will be set to focus
        self.isFocus = True
        self.isOnSmallBreak = False
        self.isOnLongBreak = False

        self.timer_event = threading.Event()
        self.timer_thread = threading.Thread(target=self.start_timer, daemon=True)
        self.timer_thread.start()

    def start_timer(self):
        # continue the timer until user stops, pauses, or restarts the timer
        # and when the timer has not finished
        while not self.timer_stop and (self.mins > 0 or self.sec > 0):
            if self.mins <= 0 and self.sec <= 0:
                break

            if self.timer_pause:
                self.timer_event.wait()
                self.timer_event.clear()
            else:
                if self.timer_restart:
                    self.mins = self.mins_copy
                    self.sec = 0
                    self.timer_restart = False
                else:
                    if self.sec <= 0:
                        if self.mins - 1 >= 0:
                            self.mins -= 1
                            self.sec = 60
                    else:
                        self.sec -= 1
                        time.sleep(1)

    def restart_timer(self):
        self.timer_restart = True

    def stop_timer(self):
        # ends the timer thread
        self.timer_stop = True

    def pause_timer(self):
        # pauses the timer thread
        self.timer_pause = True

    def resume_timer(self):
        # continues the timer thread (if pause was initiated)
        self.timer_pause = False
        self.timer_event.set()

    def get_min_value(self):
        return self.mins

    def get_sec_value(self):
        return self.sec
