# 프론트 백 데이터 변환 모듈

from constant_variable import *

import pandas as pd


# 시간표에서 사용할 강의 데이터를 프론트에서 사용할 수 있는 형태로 변환
def convert_timetable_element_to_front(course_series):
    course_time_classroom = course_series.time_classroom
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
                    try:
                        course_list.append(
                            {
                                "day": day_list[day_index],
                                "time": time_head,
                                "duration": duration,
                                "subject": course_series.course_name,
                                "room": course_series.classroom[day_list[day_index]],
                                "professor": course_series.professor,
                                "course_class_id": course_series.course_class_id,
                            }
                        )
                    except:
                        raise KeyError(f"KeyError: {course_series.classroom}")
                    time_head = None
                    duration = 0

    return course_list


def convert_timetable_element_to_back(course_series):
    pass


# 시간표 데이터를 프론트에서 사용할 수 있는 형태로 변환
def convert_timetable_to_front(timetable_df):
    timetable_list = []

    for course_series in timetable_df.itertuples():
        timetable_list += convert_timetable_element_to_front(course_series)

    return timetable_list


def convert_timetable_to_back(entire_course_bit_df, timetable_list):
    course_class_id_set = set()

    for timetable_element in timetable_list:
        course_class_id_set.add(timetable_element["course_class_id"])

    timetable_df = pd.DataFrame(columns=entire_course_bit_df.columns)

    for course_class_id in course_class_id_set:
        timetable_df = pd.concat(
            [
                timetable_df,
                entire_course_bit_df[
                    entire_course_bit_df["course_class_id"] == course_class_id
                ],
            ]
        )

    return timetable_df


# 강의 데이터를 프론트에서 사용할 수 있는 형태로 변환
def convert_course_to_front(course_df):
    # 학수번호가 중복된 row 제거
    course_df = course_df.drop_duplicates(subset="course_id", keep="first")

    course_list = []

    for course_series in course_df.itertuples():
        department_name = course_series.department
        if department_name.startswith("기타"):
            department_name = department_name.split("-")[1]
        else:
            department_name = department_name.split("-")[0]

        course_list.append(
            f"{department_name}, {course_series.course_name}, {course_series.course_id}"
        )

    return course_list


def convert_course_to_back(entire_course_bit_df, course_list):
    course_df = pd.DataFrame()

    for course_list_element in course_list:
        department, course_name, course_id = course_list_element.split(", ")
        course_df = pd.concat(
            [
                course_df,
                entire_course_bit_df[entire_course_bit_df["course_id"] == course_id],
            ]
        )

    return course_df


def convert_professor_to_front(professor_dict):
    return professor_dict


def convert_professor_to_back(entire_course_bit_df, professor_dict):
    professor_course_df = pd.DataFrame()

    for course, professor in professor_dict.items():
        course_id = course.split(", ")[2]
        # course_id와 professor가 일치하는 row를 찾아서 추가
        professor_course_df = professor_course_df.append(
            entire_course_bit_df[
                (entire_course_bit_df["course_id"] == course_id)
                and (entire_course_bit_df["professor"] == professor)
            ]
        )

    return professor_course_df


def convert_filter_to_front(avoid_time_bit):
    pass


def convert_filter_to_back(filter_data):
    # 1. 필터에서 피해야 할 시간을 bit로 변환
    # 예시
    # "월요일 15시 30분 ~ 17시 30분"
    # "금요일 17시 ~ 19시"
    avoid_time_list = filter_data[AVOID_TIME]
    avoid_time_bit = [0] * DAY_NUM

    for avoid_time in avoid_time_list:
        # 요일, 시간 추출
        day, time = avoid_time.split("요일 ")
        # 시작 시간 추출
        start_time = time.split("~")[0]
        start_hour = start_time.split("시")[0]
        if "분" in start_time:
            start_minute = start_time.split("시")[1].split("분")[0]
        else:
            start_minute = "0"
        # 종료 시간 추출
        end_time = time.split("~")[1]
        end_hour = end_time.split("시")[0]
        if "분" in end_time:
            end_minute = end_time.split("시")[1].split("분")[0]
        else:
            end_minute = "0"

        # 요일 bit 설정
        day_index = ["월", "화", "수", "목", "금", "토"].index(day)
        # 시간 bit 설정
        for time_index in range(
            (int(start_hour) - 9) * 2 + int(start_minute) // 30 + 1,
            (int(end_hour) - 9) * 2 + int(end_minute) // 30 + 1,
        ):
            avoid_time_bit[day_index] |= 1 << time_index

    filter_data[AVOID_TIME] = avoid_time_bit

    # 2. 필터에서 선호하는 교수를 dict로 변환
    # 예시
    # {"컴퓨터공학과, 컴파일러, CES4312" : "김지응", "컴퓨터공학과, 프로그래밍언어 이론, CES4232" : "김지응"}
    prefer_professor_front_dict = filter_data[PREFER_PROFESSOR]
    prefer_professor_back_dict = {}
    for course, professor in prefer_professor_front_dict.items():
        department, course_name, course_id = course.split(", ")
        prefer_professor_back_dict[course_id] = professor

    filter_data[PREFER_PROFESSOR] = prefer_professor_back_dict

    # 3. 필터에서 피해야 할 교수를 dict로 변환
    # 예시
    # {"컴퓨터공학과, 컴파일러, CES4312" : "김지응", "컴퓨터공학과, 프로그래밍언어 이론, CES4232" : "김지응"}
    avoid_professor_front_dict = filter_data[AVOID_PROFESSOR]
    avoid_professor_back_dict = {}
    for course, professor in avoid_professor_front_dict.items():
        department, course_name, course_id = course.split(", ")
        avoid_professor_back_dict[course_id] = professor

    filter_data[AVOID_PROFESSOR] = avoid_professor_back_dict

    return filter_data


def convert_with_front(mode, object_type, unknown_object, entire_course_bit_df=None):
    if mode == TO_FRONT:
        if object_type == TIMETABLE:
            return convert_timetable_to_front(unknown_object)
        elif object_type == COURSE:
            return convert_course_to_front(unknown_object)
        elif object_type == PROFESSOR:
            return convert_professor_to_front(unknown_object)
        elif object_type == FILTER:
            return convert_filter_to_front(unknown_object)
        else:
            raise ValueError(f"유효하지 않은 object_type: {object_type}")
    elif mode == TO_BACK:
        if object_type == TIMETABLE:
            return convert_timetable_to_back(entire_course_bit_df, unknown_object)
        elif object_type == COURSE:
            return convert_course_to_back(entire_course_bit_df, unknown_object)
        elif object_type == PROFESSOR:
            return convert_professor_to_back(entire_course_bit_df, unknown_object)
        elif object_type == FILTER:
            return convert_filter_to_back(unknown_object)
        else:
            raise ValueError(f"유효하지 않은 object_type: {object_type}")
    else:
        raise ValueError(f"유효하지 않은 mode: {mode}")
