from module.is_valid_timetable import *

import pandas as pd
import itertools


def require_course_timetable(course_df):
    course_id_set = set(course_df["course_id"].tolist())

    course_id_df_list = [
        course_df[course_df["course_id"] == course_id] for course_id in course_id_set
    ]

    row_product = list(
        itertools.product(*[course_id_df.index for course_id_df in course_id_df_list])
    )

    timetable_df_list = [
        pd.concat(
            [course_id_df_list[i].loc[row] for i, row in enumerate(row)], axis=1
        ).T
        for row in row_product
    ]

    valid_timetable_df_list = [
        timetable_df
        for timetable_df in timetable_df_list
        if is_valid_timetable(timetable_df)
    ]

    return valid_timetable_df_list
