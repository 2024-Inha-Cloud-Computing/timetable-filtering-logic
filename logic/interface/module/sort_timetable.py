from constant_variable import *

import sys
import numpy as np


def sort_timetable(mode, timetable_df_list, mode_data=None):
    if mode == SQAURE_AREA:
        return sort_timetable_by_square_area(timetable_df_list)
    elif mode == TASTE:
        return sort_timetable_by_taste(timetable_df_list, mode_data)
    else:
        raise ValueError("올바른 mode가 아닙니다.")


def sort_timetable_by_square_area(timetable_df_list):
    timetable_df_list_with_square_area = [
        (timetable_df, get_square_area(timetable_df))
        for timetable_df in timetable_df_list
    ]

    timetable_df_list_with_square_area.sort(key=lambda x: x[1])

    timetable_df_list_sorted = [
        timetable_df for timetable_df, square_area in timetable_df_list_with_square_area
    ]

    return timetable_df_list_sorted


def sort_timetable_by_taste(timetable_df_list, user_taste):
    timetable_df_list_with_taste_score = [
        (timetable_df, get_taste(timetable_df, user_taste))
        for timetable_df in timetable_df_list
    ]

    timetable_df_list_with_taste_score.sort(key=lambda x: x[1], reverse=True)

    timetable_df_list_sorted = [
        timetable_df for timetable_df, taste_score in timetable_df_list_with_taste_score
    ]

    return timetable_df_list_sorted


def get_square_area(timetable_df):
    day_head = sys.maxsize
    day_tail = 0
    time_head = sys.maxsize
    time_tail = 0

    for course_series in timetable_df.itertuples():
        course_time_classroom = course_series.time_classroom

        for day_index, course_time_classroom_element in enumerate(
            course_time_classroom
        ):
            for time_index in range(TIME_NUM):
                if course_time_classroom_element & (1 << time_index):
                    day_head = min(day_head, day_index)
                    day_tail = max(day_tail, day_index)
                    time_head = min(time_head, time_index)
                    time_tail = max(time_tail, time_index)

    return (day_tail - day_head + 1) * (time_tail - time_head + 1)


def get_taste(timetable_df, user_taste):
    # 1. 오전/오후 수업 점수
    # 오전/오후 시간 비트
    am_bit = np.array([0b1111110] * 6 + [0], dtype=np.uint32)
    pm_bit = np.array([(2**32 - 1) ^ am_bit[0]] * 6 + [0], dtype=np.uint32)

    # 각 수업의 오전/오후 점수 합산
    am_score = 0
    pm_score = 0

    for course_series in timetable_df.itertuples():
        course_time_classroom = course_series.time_classroom

        am_score_bitwise_and = np.bitwise_and(
            am_bit, course_time_classroom, dtype=np.uint32
        )
        am_score_cur = bit_count(am_score_bitwise_and).sum()
        am_score += am_score_cur

        pm_score_bitwise_and = np.bitwise_and(
            pm_bit, course_time_classroom, dtype=np.uint32
        )
        pm_score_cur = bit_count(pm_score_bitwise_and).sum()
        pm_score += pm_score_cur

    if user_taste[AMPM]:
        ampm_score = min(2, (am_score + 1) // (pm_score + 1))
    else:
        ampm_score = min(2, (pm_score + 1) // (am_score + 1))

    # 2. 1교시 점수
    # 1교시 비트
    time1_bit = np.array([0b10], dtype=np.uint32)

    # 각 수업의 1교시 점수 합산
    time1_score = 0

    for course_series in timetable_df.itertuples():
        course_time_classroom = course_series.time_classroom[:-1]

        time1_score_bitwise_and = np.bitwise_and(
            time1_bit, course_time_classroom, dtype=np.uint32
        )

        time1_score_cur = bit_count(time1_score_bitwise_and).sum()
        time1_score += time1_score_cur

    time1_score = min(0, user_taste[TIME1] - time1_score)

    # 3. 우주 공강 점수
    if user_taste[SPACE]:
        space_score = get_no_class_day(timetable_df)
    else:
        space_score = -get_height(timetable_df) // 3

    # 모든 점수 합산
    taste_score = ampm_score + time1_score + space_score

    return taste_score


def get_no_class_day(timetable_df):
    timetable_df_bitwise_or = np.bitwise_or.reduce(
        timetable_df["time_classroom"].tolist()[:-1], dtype=np.uint32
    )

    no_class_day = 0

    for day_index in range(DAY_NUM - 1):
        if not timetable_df_bitwise_or[day_index]:
            no_class_day += 1

    return no_class_day


def get_height(timetable_df):
    timetable_df_bitwise_or = np.bitwise_or.reduce(
        timetable_df["time_classroom"].tolist()[:-1], dtype=np.uint32
    )

    timetable_df_bitwise_or = np.bitwise_or.reduce(
        timetable_df_bitwise_or, dtype=np.uint32
    )

    top, bottom = 0, 0

    for time_index in range(TIME_NUM):
        if timetable_df_bitwise_or & (1 << time_index):
            top = time_index
            break

    for time_index in range(TIME_NUM)[::-1]:
        if timetable_df_bitwise_or & (1 << time_index):
            bottom = time_index
            break

    return bottom - top + 1


def bit_count(arr):
    # https://stackoverflow.com/questions/9829578/fast-way-of-counting-non-zero-bits-in-positive-integer
    # Make the values type-agnostic (as long as it's integers)
    t = arr.dtype.type
    mask = t(-1)
    s55 = t(0x5555555555555555 & mask)  # Add more digits for 128bit support
    s33 = t(0x3333333333333333 & mask)
    s0F = t(0x0F0F0F0F0F0F0F0F & mask)
    s01 = t(0x0101010101010101 & mask)

    arr = arr - ((arr >> 1) & s55)
    arr = (arr & s33) + ((arr >> 2) & s33)
    arr = (arr + (arr >> 4)) & s0F
    return (arr * s01) >> (8 * (arr.itemsize - 1))
