import time

''' A timer class to measure the passage of time in the game
    start - starts the timer
    stop - stops the timer
    get_timer - returns the difference in seconds between start time and stop time, rounded to 3 decimal digits
    added exception to check for timer bugs'''


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self):
        self.start_time = None

    def start(self):
        """Start a new timer"""
        if self.start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self.start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self.start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")
        self.start_time = None

    def get_timer(self):
        return round(time.perf_counter() - self.start_time, 3)


if __name__ == '__main__':
    timer = Timer()
    timer.start()
    time.sleep(2)
    print(timer.get_timer())
    timer.stop()

