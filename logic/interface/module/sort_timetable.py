from constant_variable import *

import sys


def sort_timetable(mode, timetable_df_list):
    if mode == SQAURE_AREA:
        return sort_timetable_by_square_area(timetable_df_list)


def sort_timetable_by_square_area(timetable_df_list):
    for index, timetable_df in enumerate(timetable_df_list):
        timetable_df_list[index] = (timetable_df, get_square_area(timetable_df))

    timetable_df_list.sort(key=lambda x: x[1])

    for index, (timetable_df, _) in enumerate(timetable_df_list):
        timetable_df_list[index] = timetable_df

    return timetable_df_list


def get_square_area(timetable_df):
    day_head = sys.maxsize
    day_tail = 0
    time_head = sys.maxsize
    time_tail = 0

    for _, course_series in timetable_df.iterrows():
        course_time_classroom = course_series["time_classroom"]

        for day_index, course_time_classroom_element in enumerate(
            course_time_classroom
        ):
            for time_index in range(TIME_NUM):
                if course_time_classroom_element & (1 << time_index):
                    day_head = min(day_head, day_index)
                    day_tail = max(day_tail, day_index)
                    time_head = min(time_head, time_index)
                    time_tail = max(time_tail, time_index)

    return (day_tail - day_head + 1) * (time_tail - time_head + 1)
