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
        self.mins = self.focus_mins
        self.sec = 0

        # boolean logic to control timer thread
        self.timer_pause = False
        self.timer_stop = False
        self.timer_restart = False
        self.isFocus = True
        self.isOnSmallBreak = False # it is a small break if it isn't a long break
        self.isOnLongBreak = False # it is a long break if the # of pomodoros % 4 == 0

        # threading related
        self.timer_event = threading.Event()
        self.timer_thread = threading.Thread(target=self.start_timer, daemon=True)
        self.timer_thread.start()

    def start_timer(self):
        print("[State: Start] - timer thread starts")

        # continue the timer until user stops, pauses, or restarts the timer
        # and when the timer has not finished
        while not self.timer_stop and (self.mins >= 0 and self.sec >= 0):
            if self.timer_pause:
                self.timer_event.wait()
                self.timer_event.clear()
            else:
                if self.timer_restart:
                    # checks to see which timer to restart to
                    if self.isFocus:
                        self.mins = self.focus_mins
                    elif self.isOnLongBreak:
                        self.mins = self.long_break_mins
                    else:
                        self.mins = self.small_break_mins

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

                # todo: breaking from the program is not good practice, so think of another solution
                if self.mins <= 0 and self.sec <= 0:
                    break

                print(self.mins, " min\n", self.sec, " sec")
        print("[State: Finished] timer thread ends")

    def restart_timer(self):
        # 1. resets the timer (in the Timer Class)
        self.timer_restart = True
        # 2. resets the counter for the pomodoro cycle (in the GUI Class)
        print("[State: Restart] - timer thread continues")

    def stop_timer(self):
        # ends the timer thread
        self.timer_stop = True
        print("[State: Stop] - timer thread ends")

    def pause_timer(self):
        # pauses the timer thread
        # 1. pauses the timer
        self.timer_pause = True
        print("[State: Pause] - timer thread paused")

    def resume_timer(self):
        # continues the timer thread (if pause was initiated)
        self.timer_pause = False
        self.timer_event.set()  # triggers the timer to continue again
        print("[State: Resume] - timer thread resumes")

    def get_min_value(self):
        return self.mins

    def get_sec_value(self):
        return self.sec
