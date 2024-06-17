from constant_variable import *
from module.is_valid_timetable import *

import numpy as np
import pandas as pd


def set_pool_by_timetable(entire_course_bit_df, timetable_df):
    pool = entire_course_bit_df.copy()

    # timetable_df_course_id_set = set(timetable_df["course_id"].tolist())
    # timetable_df_grade_set = set(timetable_df["grade"].tolist())

    for course_series in pool.itertuples():
        if not is_valid_course(course_series, timetable_df):
            pool = pool.drop(course_series.Index)
            continue

        # if course_series.grade not in timetable_df_grade_set:
        #     pool = pool.drop(course_series.Index)

    return pool


def set_pool_by_mode(
    auto_fill_mode,
    department_possible_df_list,
    elective_course_bit_df,
    department_id_by_curriculum,
):
    if auto_fill_mode == "전공필수":
        major_pool = department_possible_df_list[department_id_by_curriculum][0]
        major_required_pool = major_pool[
            major_pool["course_classification"] == "전공필수"
        ]
        return major_required_pool
    elif auto_fill_mode == "전공선택":
        major_pool = department_possible_df_list[department_id_by_curriculum][0]
        major_elective_pool = major_pool[
            major_pool["course_classification"] == "전공선택"
        ]
        return major_elective_pool
    elif auto_fill_mode == "교양필수":
        liberal_required_pool = department_possible_df_list[
            department_id_by_curriculum
        ][1]
        return liberal_required_pool
    elif auto_fill_mode == "교양영어":
        english_pool = elective_course_bit_df[
            elective_course_bit_df["department"] == "기타-교양영어"
        ]
        return english_pool
    elif auto_fill_mode.startswith("핵심교양"):
        ged_num = auto_fill_mode[-1]
        ged_pool = elective_course_bit_df[
            elective_course_bit_df["course_id"].str.startswith(f"GED{ged_num}")
        ]
        return ged_pool
    elif auto_fill_mode == "일반교양":
        elective_pool = elective_course_bit_df[
            elective_course_bit_df["department"] == "기타-일반교양"
        ]
        return elective_pool
    else:
        raise ValueError(f"유효하지 않은 auto_fill_mode: {auto_fill_mode}")


def set_pool_by_filter(entire_course_bit_df, filter_data):
    avoid_time_bit = filter_data[AVOID_TIME]
    prefer_professor_dict = filter_data[PREFER_PROFESSOR]
    avoid_professor_dict = filter_data[AVOID_PROFESSOR]

    pool_df = entire_course_bit_df.copy()

    for course_series in entire_course_bit_df.itertuples():
        if np.bitwise_and(avoid_time_bit, course_series.time_classroom).any():
            pool_df = pool_df.drop(course_series.Index)
            continue

        course_id_cur, professor_cur = (
            course_series.course_id,
            course_series.professor,
        )

        if course_id_cur in prefer_professor_dict:
            if professor_cur != prefer_professor_dict[course_id_cur]:
                pool_df = pool_df.drop(course_series.Index)
                continue

        if course_id_cur in avoid_professor_dict:
            if professor_cur == avoid_professor_dict[course_id_cur]:
                pool_df = pool_df.drop(course_series.Index)
                continue

    return pool_df
