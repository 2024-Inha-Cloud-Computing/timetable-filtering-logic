from constant_variable import *
from module.is_valid_timetable import *
from module.sort_timetable import *

import pandas as pd


# 백트래킹을 이용한 시간표 자동 채우기
def auto_fill(timetable_df, pool_df, fill_credit):
    def backtracking(timetable_df, pool_df, fill_credit, cur_credit):
        print(cur_credit, fill_credit, len(timetable_df_list))

        if cur_credit == fill_credit:
            timetable_df_list.append(timetable_df.copy())
            return

        for index, course_series in pool_df.iterrows():
            if not is_valid_course(course_series, timetable_df):
                continue

            next_credit = cur_credit + course_series["credits"]
            if next_credit > fill_credit:
                continue

            timetable_df = pd.concat([timetable_df, course_series.to_frame().T])
            pool_df = pool_df.drop(index)
            backtracking(
                timetable_df,
                pool_df,
                fill_credit,
                next_credit,
            )
            timetable_df = timetable_df.iloc[:-1]
            pool_df = pd.concat([pool_df, course_series.to_frame().T])

    timetable_df = timetable_df.copy()
    timetable_df_list = []
    backtracking(timetable_df, pool_df, fill_credit, 0)

    sort_timetable(SQAURE_AREA, timetable_df_list)

    return timetable_df_list
