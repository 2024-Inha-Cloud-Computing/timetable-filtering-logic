from constant_variable import *
from module.is_valid_timetable import *

import numpy as np
import pandas as pd


def set_pool_by_timetable(entire_course_bit_df, timetable_df):
    pool = entire_course_bit_df.copy()

    timetable_df_course_id_set = set(timetable_df["course_id"].tolist())

    for index, course_series in timetable_df.iterrows():
        if not is_valid_course(course_series, timetable_df):
            pool = pool.drop(index)

        if course_series["course_id"] in timetable_df_course_id_set:
            pool = pool.drop(index)

    return pool


def set_pool_by_mode(
    auto_fill_mode, department_possible_df_list, elective_course_bit_df, department_id
):
    if auto_fill_mode == MAJOR_MODE:
        pool = department_possible_df_list[department_id][0]
    elif auto_fill_mode == LIBERAL_REQUIRED_MODE:
        pool = department_possible_df_list[department_id][1]
    elif auto_fill_mode == ELECTIVE_MODE:
        pool = elective_course_bit_df

    return pool
