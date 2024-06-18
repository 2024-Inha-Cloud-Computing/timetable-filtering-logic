from constant_variable import *
from module.is_valid_timetable import *
from module.sort_timetable import *

import pandas as pd


# 백트래킹을 이용한 시간표 자동 채우기
def auto_fill(timetable_df, pool_df, fill_credit):
    def backtracking(timetable_df, pool_df, fill_credit, cur_credit, start_index):
        print(f"\r만들어진 시간표 수: {len(timetable_df_list)}\t", end="")

        if cur_credit == fill_credit:
            timetable_df_list.append(timetable_df.copy())
            return

        for i in range(start_index, len(pool_df)):
            course_series = pool_df.iloc[i]

            if not is_valid_course(course_series, timetable_df):
                continue

            next_credit = cur_credit + course_series.credits
            if next_credit > fill_credit:
                continue

            if timetable_df.empty:
                timetable_df = pd.DataFrame([course_series])
            else:
                timetable_df = pd.concat([timetable_df, pd.DataFrame([course_series])])

            backtracking(
                timetable_df,
                pool_df,
                fill_credit,
                next_credit,
                i + 1,
            )
            timetable_df = timetable_df.iloc[:-1]

    timetable_df = timetable_df.copy()
    timetable_df_list = []
    backtracking(timetable_df, pool_df, fill_credit, 0, 0)

    return timetable_df_list


def auto_fill_process(auto_fill_timetable_list_next, auto_fill_timetable, pool, mode):
    auto_fill_timetable_list_next += auto_fill(auto_fill_timetable, pool, mode[0])
