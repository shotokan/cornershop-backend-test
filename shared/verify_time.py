from datetime import datetime

from django.utils import timezone

import pytz

from shared.constants import TIME_OVER


class TimeVerifier:
    """
    A class used to verify that current time is less than the a end time selected
    ...
    Attributes
    ---------
    time_over: represents the time against which the current date and time will be compared
    """

    def __init__(self, time_over=TIME_OVER):
        self.time_over = time_over

    def is_before_end_time(self):
        """Validates that current time is less than the end_time

        Returns:
            boolean: a boolean representing if the time is less than end_time
        """
        chile = pytz.timezone("America/Santiago")
        timezone.activate(chile)
        current_date = chile.localize(datetime.utcnow())
        end_time = timezone.datetime(
            current_date.year,
            current_date.month,
            current_date.day,
            hour=self.time_over,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=chile,
        ).astimezone(pytz.utc)
        print(end_time)
        if current_date.hour < end_time.hour:
            return True
        return False
