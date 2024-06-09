# 입력받은 학수번호들로 시간표를 만들 수 있는지 확인하는 모듈

import numpy as np


def is_valid_timetable(timetable_df):
    # cur_course_df의 time_classroom column을 전부 bitwise AND 연산하여 모든 요소가 0인지 확인
    temp = 0
    for time_classroom in timetable_df["time_classroom"]:
        if np.bitwise_and(temp, time_classroom).any():
            return False

        temp = np.bitwise_or(temp, time_classroom)

    return True


def is_valid_course(course_series, timetable_df):
    timetable_or = np.bitwise_or.reduce(timetable_df["time_classroom"].tolist())

    # 시간이 겹치는지 확인
    time_conflict = not np.bitwise_and(
        timetable_or, course_series["time_classroom"]
    ).any()

    # 같은 과목인지 확인
    course_conflict = (
        not timetable_df["course_id"].isin([course_series["course_id"]]).any()
    )

    return time_conflict and course_conflict
