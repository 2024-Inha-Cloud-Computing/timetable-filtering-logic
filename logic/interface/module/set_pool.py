from constant_variable import *
from module.is_valid_timetable import *

import numpy as np
import pandas as pd


def set_pool_by_timetable(entire_course_bit_df, timetable_df):
    pool = entire_course_bit_df.copy()

    timetable_df_course_id_set = set(timetable_df["course_id"].tolist())
    timetable_df_grade_set = set(timetable_df["grade"].tolist())

    for index, course_series in pool.iterrows():
        if not is_valid_course(course_series, timetable_df):
            pool = pool.drop(index, errors="ignore")

        if course_series["course_id"] in timetable_df_course_id_set:
            pool = pool.drop(index, errors="ignore")

        # if course_series["grade"] not in timetable_df_grade_set:
        #     pool = pool.drop(index, errors="ignore")

    return pool


def set_pool_by_mode(
    auto_fill_mode,
    department_possible_df_list,
    elective_course_bit_df,
    department_id_by_curriculum,
):
    if auto_fill_mode == MAJOR_MODE:
        pool = department_possible_df_list[department_id_by_curriculum][0]
    elif auto_fill_mode == LIBERAL_REQUIRED_MODE:
        pool = department_possible_df_list[department_id_by_curriculum][1]
    elif auto_fill_mode == ELECTIVE_MODE:
        pool = elective_course_bit_df

    return pool


def set_pool_by_filter(filter_data, pool_df):
    avoid_time_bit = filter_data[AVOID_TIME]
    prefer_professor_dict = filter_data[PREFER_PROFESSOR]
    avoid_professor_dict = filter_data[AVOID_PROFESSOR]

    for index, course_series in pool_df.iterrows():
        if np.bitwise_and(avoid_time_bit, course_series["time_classroom"]).any():
            pool_df = pool_df.drop(index, errors="ignore")

        for course_id, professor in prefer_professor_dict.items():
            if (
                course_series["course_id"] == course_id
                and course_series["professor"] != professor
            ):
                pool_df = pool_df.drop(index, errors="ignore")

        for course_id, professor in avoid_professor_dict.items():
            if (
                course_series["course_id"] == course_id
                and course_series["professor"] == professor
            ):
                pool_df = pool_df.drop(index, errors="ignore")

    return pool_df
