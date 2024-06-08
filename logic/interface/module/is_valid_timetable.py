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
