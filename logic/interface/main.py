# 앱의 진행에 따라 필요한 기능을 수행하는 모듈

from constant_variable import *
from module.import_processed_data import *
from module.convert import *
from module.search_course import *
from module.require_course_timetable import *
from module.find_professor import *
from module.is_valid_timetable import *
from module.auto_fill import *
from module.set_pool import *

import pandas as pd


class TimetableInterface:
    def __init__(self, user_taste):
        self.__user_taste = (
            user_taste  # [오전/오후 수업, 1교시 수업 수, 우주 공강 여부]
        )
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

    def require_course_timetable_routine(self, course_list):
        course_list_front_object = course_list
        course_df_back_object = convert_with_front(
            TO_BACK, COURSE, course_list_front_object, self.__entire_course_bit_df
        )

        timetable_df_list_back_object = require_course_timetable(course_df_back_object)
        timetable_df_list_front_object = [
            convert_with_front(TO_FRONT, TIMETABLE, timetable_df_back_object)
            for timetable_df_back_object in timetable_df_list_back_object
        ]

        return timetable_df_list_front_object

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
        filter_data,
        mode,
        timetable_list_front_object,
        fill_credit,
        department_id_by_curriculum=None,
    ):
        # front 형식의 시간표를 back 형식으로 변환
        timetable_df_back_object = convert_with_front(
            TO_BACK, TIMETABLE, timetable_list_front_object, self.__entire_course_bit_df
        )

        # 시간표에 들어갈 수 있는 강의들의 pool 생성
        pool_by_timetable = set_pool_by_timetable(
            self.__entire_course_bit_df, timetable_df_back_object
        )
        # 현재 mode에 맞는 강의들의 pool 생성
        pool_by_mode = set_pool_by_mode(
            mode,
            self.__department_possible_df_list,
            self.__elective_course_bit_df,
            department_id_by_curriculum,
        )

        # 두 pool의 교집합
        pool_df = pd.merge(
            pool_by_timetable,
            pool_by_mode,
            on="course_class_id",
            suffixes=("", "_to_drop"),
        )
        pool_df = pool_df.drop(
            columns=[col for col in pool_df.columns if col.endswith("_to_drop")]
        )

        # pool에서 필터링
        filter_front_object = filter_data
        filter_back_object = convert_with_front(TO_BACK, FILTER, filter_front_object)
        pool_df = set_pool_by_filter(filter_back_object, pool_df)

        # pool에서 시간표 생성
        timetable_df_list_back_object = auto_fill(
            timetable_df_back_object, pool_df, fill_credit
        )

        # 시간표 정렬
        timetable_df_list_back_object = sort_timetable(
            TASTE, timetable_df_list_back_object, self.__user_taste
        )

        timetable_df_list_front_object = [
            convert_with_front(TO_FRONT, TIMETABLE, timetable_df_back_object)
            for timetable_df_back_object in timetable_df_list_back_object
        ]

        return timetable_df_list_front_object


# 테스트 코드
user_taste = [False, 2, False]
user = TimetableInterface(user_taste)
search_word = "박준석"
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
    [
        ["월요일 15시 ~ 16시 30분", "수요일 15시 ~ 16시 30분"],
        {
            "컴퓨터공학과, 컴파일러, CSE4312": "김지응",
            "컴퓨터공학과, 프로그래밍언어 이론, CSE4232": "김지응",
        },
        {"컴퓨터공학과, 컴파일러, CSE4312": "박준석"},
    ],
    MAJOR_MODE,
    search_result,
    9,
    69,
)

print(auto_fill_result[0])
