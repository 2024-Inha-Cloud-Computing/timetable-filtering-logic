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
            TO_FRONT, "course", search_course_back_opject
        )

        return search_course_front_object

    def find_professor_routine(self, course_list):
        course_list_front_object = course_list
        course_list_back_object = convert_with_front(
            TO_BACK, "course", course_list_front_object
        )

        find_professor_back_object = find_professor(course_list_back_object)
        find_professor_front_object = convert_with_front(
            TO_FRONT, "course", find_professor_back_object
        )

        return find_professor_front_object

    def auto_fill_routine(self, mode, timetable_df, fill_grade, department=None):
        pool_by_timetable = set_pool_by_timetable(
            self.__entire_course_bit_df, timetable_df
        )
        pool_by_mode = set_pool_by_mode(
            mode,
            self.__department_possible_df_list,
            self.__elective_course_bit_df,
            department,
        )

        # 두 pool의 교집합
        pool = pd.merge(pool_by_timetable, pool_by_mode)

        timetable_df_list_back_object = auto_fill(timetable_df, pool, fill_grade)
        timetable_df_list_front_object = convert_with_front(
            TO_FRONT, "timetable", timetable_df_list_back_object
        )

        return timetable_df_list_front_object


# 테스트 코드
user_data = {
    "학과": "컴퓨터공학과-컴퓨터공학",
}
user = TimetableInterface(user_data)
search_word = "김지응"
