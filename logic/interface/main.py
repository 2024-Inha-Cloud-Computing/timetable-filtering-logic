# 앱의 진행에 따라 필요한 필터링을 수행하는 모듈

from constant_variable import *
from module.import_processed_data import *
from module.search_course import *
from module.is_valid_timetable import *
from module.convert import *

import pandas as pd


class TimetableInterface:
    def __init__(self, user_data):
        # json 데이터를 받아서 __user_data에 Series 형태로 저장
        self.__user_data = pd.Series(user_data)

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
        ) = self.__import_processed_data()

    def __import_processed_data(self):
        return import_processed_data()

    def __make_timetable(self):
        pass

    def __convert_to_front(self, mode, back_object):
        if mode == "timetable":
            return convert_timetable_to_front(back_object)
        elif mode == "course":
            return convert_course_to_front(back_object)

    def search_course_routine(self, search_word=""):
        # search_course 모듈의 search_course 함수 호출
        return search_course(search_word, self.__entire_course_bit_df)


# 테스트 코드
user_data = {
    "학과": "컴퓨터공학과-컴퓨터공학",
}
user_0 = TimetableInterface(user_data)
search_word = "김지응"

print(user_0.search_course_routine(search_word))
