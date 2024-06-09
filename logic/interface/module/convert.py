# 프론트 백 데이터 변환 모듈

from constant_variable import *

import pandas as pd


# 시간표에서 사용할 강의 데이터를 프론트에서 사용할 수 있는 형태로 변환
def convert_timetable_element_to_front(course_series):
    course_time_classroom = course_series["time_classroom"]
    course_list = []
    day_list = ["월", "화", "수", "목", "금", "토", "셀"]

    for day_index, course_time_classroom_element in enumerate(course_time_classroom):
        time_head = None
        duration = 0
        for time_index in range(TIME_NUM):
            if course_time_classroom_element & (1 << time_index):
                if time_head is None:
                    time_head = 8.5 + time_index * 0.5
                    duration += 0.5
                else:
                    duration += 0.5
            else:
                if time_head is not None:
                    course_list.append(
                        {
                            "day": day_list[day_index],
                            "time": time_head,
                            "duration": duration,
                            "subject": course_series["course_name"],
                            "room": course_series["classroom"][day_list[day_index]],
                            "professor": course_series["professor"],
                            "course_class_id": course_series["course_class_id"],
                        }
                    )
                    time_head = None
                    duration = 0

    return course_list

def convert_timetable_element_to_back(course_series):
    pass

# 시간표 데이터를 프론트에서 사용할 수 있는 형태로 변환
def convert_timetable_to_front(timetable_df):
    timetable_list = []

    for _, course_series in timetable_df.iterrows():
        timetable_list += convert_timetable_element_to_front(course_series)

    return timetable_list

def convert_timetable_to_back(timetable_df):
    pass

# 강의 데이터를 프론트에서 사용할 수 있는 형태로 변환
def convert_course_to_front(course_df):
    # 학수번호가 중복된 row 제거
    course_df = course_df.drop_duplicates(subset="course_id", keep="first")

    course_list = []
    print("asdf")

    for _, course_series in course_df.iterrows():
        department_name = course_series["department"]
        if department_name.startswith("기타"):
            department_name = department_name.split("-")[1]
        else:
            department_name = department_name.split("-")[0]

        course_list.append(f"{department_name}, {course_series["course_name"]}, {course_series["course_id"]}")


    return course_list

def convert_course_to_back(entire_course_bit_df, course_list):
    course_df = pd.DataFrame()

    for department, course_name, course_id in course_list:
        course_df = course_df.append(
            entire_course_bit_df[
                entire_course_bit_df["course_id"] == course_id
            ]
        )

    return course_df


def convert_professor_to_front(professor_dict):
    pass

def convert_professor_to_back(entire_course_bit_df, professor_dict):
    professor_course_df = pd.DataFrame()

    for course, professor in professor_dict.items():
        course_id = course.split(", ")[2]
        # course_id와 professor가 일치하는 row를 찾아서 추가
        professor_course_df = professor_course_df.append(
            entire_course_bit_df[
                (entire_course_bit_df["course_id"] == course_id) and (entire_course_bit_df["professor"] == professor)
            ]
        )

    return professor_course_df


def convert_avoid_time_to_front(avoid_time_bit):
    pass

def convert_avoid_time_to_back(avoid_time_list):
    # 예시
    # "월요일 3시 30분 ~ 5시 30분"
    # "금요일 5시 ~ 7시"
    pass


def convert_with_front(mode, object_type, unknown_object):
    if mode == TO_FRONT:
        if object_type == TIMETABLE:
            return convert_timetable_to_front(unknown_object)
        elif object_type == COURSE:
            return convert_course_to_front(unknown_object)
        elif object_type == PROFESSOR:
            return convert_professor_to_front(unknown_object)
        elif object_type == AVOID_TIME:
            return convert_avoid_time_to_front(unknown_object)
        else:
            raise ValueError("object_type이 잘못되었습니다.")
    elif mode == TO_BACK:
        if object_type == TIMETABLE:
            return convert_timetable_to_back(unknown_object)
        elif object_type == COURSE:
            return convert_course_to_back(unknown_object)
        elif object_type == PROFESSOR:
            return convert_professor_to_back(unknown_object)
        elif object_type == AVOID_TIME:
            return convert_avoid_time_to_back(unknown_object)
        else:
            raise ValueError("object_type이 잘못되었습니다.")
    else:
        raise ValueError("mode가 잘못되었습니다.")
