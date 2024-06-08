from constant_variable import *

import numpy as np


def reduce_pool_by_course(
    entire_course_bit_df, course_by_all_time, user_pool_set, course_df
):
    course_df_time_or = np.bitwise_or.reduce(course_df["time_classroom"].values)

    for i, day_time in enumerate(course_df_time_or):
        for j in range(TIME_NUM):
            if day_time & (1 << j):
                # course_by_all_time list 해당 시간에 해당하는 강의를 user_pool_set에서 제거
                user_pool_set.difference_update(
                    set(course_by_all_time[i][j]["course_class_id"].tolist())
                )

    # course_df의 학수번호와 같은 강의를 user_pool_set에서 제거
    user_pool_set.difference_update(
        set(
            entire_course_bit_df[
                entire_course_bit_df["course_id"].isin(course_df["course_id"])
            ]["course_class_id"].tolist()
        )
    )

    return user_pool_set
