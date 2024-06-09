# 앱의 진행에 따라 필요한 기능을 수행하는 모듈

from constant_variable import *
from module.import_processed_data import *
from module.search_course import *
from module.is_valid_timetable import *
from module.convert import *
from module.find_professor import *
from module.auto_fill import *
from module.set_pool import *

import pandas as pd


class TimetableInterface:
    def __init__(self, user_taste):
        self.__user_taste = {
            "am_pm": AM,
            "time1": 2,
            "space": SPACE_ON,
        }
        self.__user_timetable_df_list = []

        # 강의 데이터 불러오기
        (
            # 학과 변환 데이터
            self.__department_name_to_id_by_course,
            self.__department_id_to_name_by_course,
            self.__department_name_to_id_by_curriculum,
            self.__department_id_to_name_by_curriculum,
            self.__df_course_list,
            self.__df_curriculum_list,
            # 전체 강의 DataFrame
            self.__entire_course_df,
            # 교양선택 DataFrame
            self.__elective_course_df,
            # 전체 강의 DataFrame (시간 bit ndarray)
            self.__entire_course_bit_df,
            # 교양선택 DataFrame
            self.__elective_course_bit_df,
            # 특정 시간 강의 DataFrame
            self.__course_by_all_time,
            # 학과별 전공, 교양필수 DataFrame
            self.__department_possible_df_list,
        ) = import_processed_data()

    def search_course_routine(self, search_word=""):
        search_course_back_opject = search_course(
            search_word, self.__entire_course_bit_df
        )
        search_course_front_object = convert_with_front(
            TO_FRONT, COURSE, search_course_back_opject
        )

        return search_course_front_object

    def find_professor_routine(self, course_list):
        course_list_front_object = course_list
        course_df_back_object = convert_with_front(
            TO_BACK, COURSE, course_list_front_object, self.__entire_course_bit_df
        )

        find_professor_back_object = find_professor(course_df_back_object)
        find_professor_front_object = convert_with_front(
            TO_FRONT, PROFESSOR, find_professor_back_object
        )

        return find_professor_front_object

    def auto_fill_routine(
        self,
        mode,
        timetable_list_front_object,
        fill_credit,
        department_id_by_curriculum=None,
    ):
        timetable_df_back_object = convert_with_front(
            TO_BACK, TIMETABLE, timetable_list_front_object, self.__entire_course_bit_df
        )

        pool_by_timetable = set_pool_by_timetable(
            self.__entire_course_bit_df, timetable_df_back_object
        )
        pool_by_mode = set_pool_by_mode(
            mode,
            self.__department_possible_df_list,
            self.__elective_course_bit_df,
            department_id_by_curriculum,
        )

        # 두 pool의 교집합
        pool = pd.merge(
            pool_by_timetable,
            pool_by_mode,
            on="course_class_id",
            suffixes=("", "_to_drop"),
        )
        pool = pool.drop(
            columns=[col for col in pool.columns if col.endswith("_to_drop")]
        )

        # print(pool)
        # exit()

        timetable_df_list_back_object = auto_fill(
            timetable_df_back_object, pool, fill_credit
        )

        timetable_df_list_front_object = [
            convert_with_front(TO_FRONT, TIMETABLE, timetable_df_back_object)
            for timetable_df_back_object in timetable_df_list_back_object
        ]

        return timetable_df_list_front_object


# 테스트 코드
user_data = {
    "학과": "컴퓨터공학과-컴퓨터공학",
}
user = TimetableInterface(user_data)
search_word = "김지응"
search_result = [
    {
        "day": "목",
        "time": 12,
        "duration": 1.5,
        "subject": "프로그래밍언어 이론",
        "room": "하-222",
        "professor": "김지응",
        "course_class_id": "CSE4232-001",
    },
    {
        "day": "금",
        "time": 12,
        "duration": 1.5,
        "subject": "프로그래밍언어 이론",
        "room": "하-222",
        "professor": "김지응",
        "course_class_id": "CSE4232-001",
    },
    {
        "day": "목",
        "time": 15,
        "duration": 1.5,
        "subject": "컴파일러",
        "room": "하-222",
        "professor": "김지응",
        "course_class_id": "CSE4312-002",
    },
    {
        "day": "금",
        "time": 15,
        "duration": 1.5,
        "subject": "컴파일러",
        "room": "하-222",
        "professor": "김지응",
        "course_class_id": "CSE4312-002",
    },
]

auto_fill_result = user.auto_fill_routine(
    MAJOR_MODE,
    search_result,
    12,
    69,
)

print(auto_fill_result[0])
