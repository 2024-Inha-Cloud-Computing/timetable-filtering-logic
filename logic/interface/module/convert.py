# 프론트 백 데이터 변환 모듈

from constant_variable import *


# 시간표에서 사용할 강의 데이터를 프론트에서 사용할 수 있는 형태로 변환
def convert_timetable_course_to_front(course_series):
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
                            "room": None,
                            "professor": course_series["professor"],
                            "course_class_id": course_series["course_class_id"],
                        }
                    )
                    time_head = None
                    duration = 0

    return course_list

# 시간표 데이터를 프론트에서 사용할 수 있는 형태로 변환
def convert_timetable_to_front(timetable_df):
    timetable_list = []

    for _, course_series in timetable_df.iterrows():
        timetable_list += convert_timetable_course_to_front(course_series)

    return timetable_list

# 강의 데이터를 프론트에서 사용할 수 있는 형태로 변환
def convert_course_to_front(course_df):
    course_list = []

    for _, course_series in course_df.iterrows():
        department_name = course_series["department"]
        if department_name.startswith("기타"):
            department_name = department_name.split("-")[1]
        else:
            department_name = department_name.split("-")[0]

        course_list.append(f"{department_name}, {course_series["course_name"]}, {course_series["course_id"]}")

    return course_list
