# 특정 시간의 강의들의 집합을 반환하는 모듈

import pandas as pd
import numpy as np


# 시간을 입력받으면 해당 시간에 열리는 강의들의 집합을 반환하는 함수
# input: DataFrame, bit로 변환된 시간
# output: DataFrame
def course_by_time(df, time):
    # time에 존재하는 강의 DataFrame
    course_by_time = pd.DataFrame(columns=df.columns)

    # time에 존재하는 강의들을 course_by_time에 추가
    for index, row in df.iterrows():
        if np.bitwise_and(row["time_classroom"], time).tolist() == time:
            course_by_time = pd.concat([course_by_time, row.to_frame().T])

    return course_by_time


# 모든 시간에 대해 열리는 강의들의 집합을 반환하는 함수
# input: DataFrame
# output: DataFrame list
def course_by_all_time(df):
    DAY_CNT = 7
    TIME_CNT = 31
    # 모든 시간에 대해 열리는 강의들을 저장할 list
    course_by_all_time = [[] for _ in range(DAY_CNT)]

    # 모든 시간에 대해 열리는 강의들을 course_by_all_time에 추가
    for day in range(DAY_CNT):
        for time in range(TIME_CNT):
            time_argument = [0] * DAY_CNT
            time_argument[day] = 1 << time
            course_by_all_time[day].append(course_by_time(df, time_argument))

    return course_by_all_time


# 테스트 코드
# import import_csv
# import entire_course
# import time_str_to_bit

# RAW_PATH = "resource/raw"

# imported_data = import_csv.import_csv(RAW_PATH)
# merged_data = entire_course.merge_all_data(imported_data)
# merged_data_time_bit = time_str_to_bit.time_str_to_bit_df(
#     merged_data.copy(), "time_classroom"
# )
# course_by_all_time = course_by_all_time(merged_data_time_bit)

# print(course_by_all_time)
