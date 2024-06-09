from constant_variable import *
from module.is_valid_timetable import *


# 백트래킹을 이용한 시간표 자동 채우기
def auto_fill(timetable_df, pool_df, fill_grade):
    def backtracking(timetable_df, pool_df, fill_grade, cur_grade):
        if cur_grade == fill_grade:
            timetable_df_list.append(timetable_df.copy())
            return

        for _, course_series in pool_df.iterrows():
            if is_valid_course(course_series, timetable_df):
                timetable_df = timetable_df.append(course_series)
                backtracking(
                    timetable_df,
                    pool_df,
                    fill_grade,
                    cur_grade + course_series["grade"],
                )
                timetable_df = timetable_df.iloc[:-1]

    timetable_df = timetable_df.copy()
    timetable_df_list = []
    backtracking(timetable_df, pool_df, fill_grade, 0)

    return timetable_df_list
