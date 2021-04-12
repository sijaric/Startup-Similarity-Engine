import os
import sys
import time

class progress_bar:

    data_size = 0.0
    data_processed_so_far = 0.0
    start_time_ms = 0.0

    def __init__(self, total_data_size):
        self.data_size = total_data_size
        self.start_time_ms = self.__current_time_ms()

    def __current_time_ms(self):
        return round(time.time() * 1000)

    def make_progress(self, data_processed):
        self.data_processed_so_far += data_processed
        self.__print_progress()

    def __time_run_so_far_ms(self):
        return self.__current_time_ms() - self.start_time_ms

    def __ms_to_timer(self, millis):
        seconds=(millis/1000)%60
        seconds = int(seconds)
        minutes=(millis/(1000*60))%60
        minutes = int(minutes)
        hours=(millis/(1000*60*60))%24
        return seconds, minutes, hours

    def __print_progress(self):
        if self.data_processed_so_far <= 0:
            millis = 0.0
        else:
            millis = ((self.__time_run_so_far_ms()) / self.data_processed_so_far) * (self.data_size - self.data_processed_so_far)
        seconds, minutes, hours = self.__ms_to_timer(millis)
        time_left = ("%d:%d:%d" % (hours, minutes, seconds))
        seconds, minutes, hours = self.__ms_to_timer(self.__time_run_so_far_ms())
        time_elapsed = ("%d:%d:%d" % (hours, minutes, seconds))

        bar_len = 60
        filled_len = int(round(bar_len * self.data_processed_so_far / float(self.data_size)))

        percents = round(100.0 * self.data_processed_so_far / float(self.data_size), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', 'Time Elapsed: [' + time_elapsed + "] | Time Left: [" + time_left + ']'))
        sys.stdout.flush()
