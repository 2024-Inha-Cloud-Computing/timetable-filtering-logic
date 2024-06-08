# 특정 시간 강의의 DataFrame을 반환하는 모듈

from constant_variable import *

import pandas as pd
import numpy as np


# 시간을 입력받으면 해당 시간에 열리는 강의 DataFrame을 반환하는 함수
# input: 강의 DataFrame, bit ndarray 형태의 시간
# output: 입력된 시간에 열리는 강의 DataFrame
def get_course_by_time(df, time):
    course_by_time = pd.DataFrame(columns=df.columns)

    for index, row in df.iterrows():
        if np.bitwise_and(row["time_classroom"], time).any():
            course_by_time = pd.concat([course_by_time, row.to_frame().T])

    return course_by_time


# 개별 교시에 열리는 강의들의 DataFrame list를 반환하는 함수
# input: 강의 DataFrame
# output: 개별 교시에 열리는 강의 DataFrame list
def get_course_by_all_time(df):
    # 개별 교시에 열리는 강의를 저장할 list
    course_by_all_time = [[] for _ in range(DAY_CNT)]

    # 개별 교시에 열리는 강의를 course_by_all_time에 추가
    for day in range(DAY_CNT):
        for time in range(TIME_CNT):
            time_argument = np.zeros(shape=DAY_CNT, dtype=np.uint32)
            time_argument[day] |= 1 << time
            course_by_all_time[day].append(get_course_by_time(df, time_argument))

    return course_by_all_time
