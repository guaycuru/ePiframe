from datetime import datetime, timedelta
from itertools import cycle, islice
from typing import List


class TimerManager:

    __DATE_MASK = "%H:%M"
    __NO_TIME_MARK = "-"
    __DELIMITER = ","

    def __init__(self, start_times: List[str], end_times: List[str]):
        self.__start_times = start_times
        self.__end_times = end_times

    def should_i_work_now(self) -> bool:
        now = datetime.now()

        day_of_week = now.weekday()
        yesterday = (datetime.now() - timedelta(1)).weekday() - 1

        return_value = False

        startTab = self.__start_times[day_of_week].strip()
        endTab = self.__end_times[day_of_week].strip()

        if startTab == self.__NO_TIME_MARK:
            return_value = False
        elif (
            now.time() < self.get_time_from_string(startTab).time()
            and self.__end_times[yesterday].strip() == self.__NO_TIME_MARK
        ):
            return_value = True
        elif (
            now.time() > self.get_time_from_string(startTab).time()
            and not self.__end_times[day_of_week].strip() == self.__NO_TIME_MARK
        ):
            return_value = (
                self.get_time_from_string(startTab).time()
                < now.time()
                < self.get_time_from_string(endTab).time()
            )
        elif (
            now.time() > self.get_time_from_string(startTab).time()
            and self.__end_times[day_of_week].strip() == self.__NO_TIME_MARK
        ):
            return_value = True

        return return_value

    def when_i_work_next(self) -> datetime:
        now = datetime.now()
        day_of_week = now.weekday()

        return_value = datetime.now(datetime.now().astimezone().tzinfo)
        now_tab = islice(cycle(self.__start_times), day_of_week, None)

        if (
            self.__end_times[day_of_week].strip() == self.__NO_TIME_MARK
            or now.time()
            > self.get_time_from_string(self.__end_times[day_of_week].strip()).time()
        ):
            return_value += timedelta(1)

        while True:
            value = next(now_tab)
            if value == self.__NO_TIME_MARK:
                return_value += timedelta(1)
            else:
                return_value = return_value.replace(
                    hour=self.get_time_from_string(value).hour,
                    minute=self.get_time_from_string(value).minute,
                    second=0,
                )
                break

        return return_value

    @classmethod
    def get_time_from_string(cls, time: str) -> datetime:
        return datetime.strptime(time, cls.__DATE_MASK)

    @classmethod
    def verify(cls, times: List[str]):
        times1 = times[0].split(cls.__DELIMITER)
        times2 = times[1].split(cls.__DELIMITER)

        for index in range(len(times1)):
            if not times1[index].strip() == cls.__NO_TIME_MARK:
                cls.get_time_from_string(times1[index].strip())
            if not times2[index].strip() == cls.__NO_TIME_MARK:
                cls.get_time_from_string(times2[index].strip())

            if (
                not times2[index].strip() == cls.__NO_TIME_MARK
                and not times1[index].strip() == cls.__NO_TIME_MARK
            ):
                if cls.get_time_from_string(
                    times1[index].strip()
                ) > cls.get_time_from_string(times2[index].strip()):
                    raise Exception(
                        "Configuration start_times times are older than stop_times!"
                    )
