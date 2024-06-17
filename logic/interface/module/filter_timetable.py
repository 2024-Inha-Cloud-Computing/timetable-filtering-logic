from constant_variable import *

import numpy as np


def filter_timetable(timetable_df_list, filter_data, filter_priority):
    avoid_time_bit = filter_data[AVOID_TIME]
    prefer_professor_dict = filter_data[PREFER_PROFESSOR]
    avoid_professor_dict = filter_data[AVOID_PROFESSOR]

    filter_timetable_df_list = []

    for timetable_df in timetable_df_list:
        is_valid_timetable = True

        for course_series in timetable_df.itertuples():
            if "time" in filter_priority:
                if np.bitwise_and(avoid_time_bit, course_series.time_classroom).any():
                    is_valid_timetable = False
                    break

            if "good" in filter_priority:
                for course_id, professor in prefer_professor_dict.items():
                    if (
                        course_series.course_id == course_id
                        and course_series.professor != professor
                    ):
                        is_valid_timetable = False
                        break

            if "bad" in filter_priority:
                for course_id, professor in avoid_professor_dict.items():
                    if (
                        course_series.course_id == course_id
                        and course_series.professor == professor
                    ):
                        is_valid_timetable = False
                        break

        if is_valid_timetable:
            filter_timetable_df_list.append(timetable_df)

    return filter_timetable_df_list
