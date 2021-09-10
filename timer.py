import threading
import time


# Timer class used to handle the timer functionalities
class Timer:
    # initialize the timer with mins
    def __init__(self, mins):
        # initialize values
        self.mins = int(mins)
        self.sec = 0
        self.continue_timer = True  # bool used to control the timer
        self.timer_event = threading.Event()
        self.timer_thread = threading.Thread(target=self.start_timer, daemon=True)
        self.timer_thread.start()  # starts the timer thread immediately

    def start_timer(self):
        # continue the timer until user stops, pauses, or restarts the timer
        # and when the min counter >= 0 and sec is greater than 0


        while self.continue_timer and (self.mins >= 0 and self.sec >= 0):
            if self.sec <= 0:
                self.mins -= 1
                self.sec = 60
            else:
                self.sec -= 1
                time.sleep(1)
            print(self.mins, " min\n", self.sec, " sec")

    def restart_timer(self):
        # 1. resets the timer back to focus time
        # 2. resets the counter for the pomodoro cycle
        self.continue_timer = False

    def stop_timer(self):
        # 1. resets the timer of focus
        self.continue_timer = False

    def pause_timer(self):
        # 1. pauses the timer
        self.continue_timer = False

    def get_min_value(self):
        return self.mins

    def get_sec_value(self):
        return self.sec
