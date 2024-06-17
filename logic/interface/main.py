# 앱의 진행에 따라 필요한 기능을 수행하는 모듈

from constant_variable import *
from module.import_processed_data import *
from module.convert import *
from module.search_course import *
from module.require_course_timetable import *
from module.find_professor import *
from module.filter_timetable import *
from module.is_valid_timetable import *
from module.auto_fill import *
from module.set_pool import *

import pandas as pd


class TimetableInterface:
    """
    프론트의 요청에 따라 백엔드의 기능을 수행하는 클래스
    input: 사용자의 취향 list [오전/오후 수업, 1교시 수업 수, 우주 공강 여부]
    output: 없음
    """

    def __init__(self, user_taste):
        self.__user_taste = (
            user_taste  # [오전/오후 수업, 1교시 수업 수, 우주 공강 여부]
        )
        self.__user_timetable_df_list = []
        self.__require_course_timetable_df_list = (
            None  # require_course_timetable 함수에서 사용하는 변수
        )

        # 강의 데이터 불러오기
        (
            # 학과 변환 데이터
            self.__department_name_to_id_by_course,
            self.__department_id_to_name_by_course,
            self.__department_name_to_id_by_curriculum,
            self.__department_id_to_name_by_curriculum,
            self.__df_course_list,
            self.__df_curriculum_list,
            self.__entire_course_df,  # 전체 강의 DataFrame
            self.__elective_course_df,  # 교양선택 DataFrame
            self.__entire_course_bit_df,  # 전체 강의 DataFrame (시간 bit ndarray)
            self.__elective_course_bit_df,  # 교양선택 DataFrame
            self.__course_by_all_time,  # 특정 시간 강의 DataFrame
            self.__department_possible_df_list,  # 학과별 전공, 교양필수 DataFrame
        ) = import_processed_data()

    def search_course_routine(self, search_word=""):
        """
        검색어를 받아 검색 결과를 반환하는 함수
        input: 검색어 string
        output: 검색 결과 list
        """

        search_course_back_opject = search_course(
            search_word, self.__entire_course_bit_df
        )
        search_course_front_object = convert_with_front(
            TO_FRONT, COURSE, search_course_back_opject
        )

        return search_course_front_object

    def require_course_timetable_routine(self, course_list):
        """
        강의 리스트를 받아 이 강의로만 이루어진 시간표를 반환하는 함수
        input: 강의 list
        output: 시간표 list
        """
        course_list_front_object = course_list
        course_df_back_object = convert_with_front(
            TO_BACK, COURSE, course_list_front_object, self.__entire_course_bit_df
        )

        timetable_df_list_back_object = require_course_timetable(course_df_back_object)
        self.__require_course_timetable_df_list = timetable_df_list_back_object  # timetable_filter_routine 함수에서 사용하기 위해 저장

        # 취향 순으로 정렬 후 상위 10개만 반환
        timetable_df_list_back_object = sort_timetable_by_taste(
            timetable_df_list_back_object, self.__user_taste
        )[:10]

        timetable_df_list_front_object = [
            convert_with_front(TO_FRONT, TIMETABLE, timetable_df_back_object)
            for timetable_df_back_object in timetable_df_list_back_object
        ]

        return timetable_df_list_front_object

    def find_professor_routine(self, course_list):
        """
        강의 리스트를 받아 이 강의들의 교수님을 반환하는 함수
        input: 강의 list
        output: 강의-교수님 dict {강의 이름: 교수님 이름}
        """
        course_list_front_object = course_list
        course_df_back_object = convert_with_front(
            TO_BACK, COURSE, course_list_front_object, self.__entire_course_bit_df
        )

        find_professor_back_object = find_professor(course_df_back_object)
        find_professor_front_object = convert_with_front(
            TO_FRONT, PROFESSOR, find_professor_back_object
        )

        return find_professor_front_object

    def timetable_filter_routine(self, filter_data_front_object, filter_priority):
        """
        필터링 조건을 받아 필터링된 시간표 리스트를 반환하는 함수
        input: 필터링 조건 list [avoid_time: list, prefer_professor: dict, avoid_professor: dict], 필터링 우선순위 list ["time", "good", "bad"] <- 순서대로 필터링 조건을 적용
        output: 필터링된 시간표 list
        """
        if self.__require_course_timetable_df_list is None:
            raise ValueError(
                "시간표 필터링을 하기 전에 require_course_timetable 함수를 실행해야 합니다."
            )
        filter_back_object = convert_with_front(
            TO_BACK, FILTER, filter_data_front_object
        )

        timetable_df_list_back_object = filter_timetable(
            self.__require_course_timetable_df_list, filter_back_object, filter_priority
        )

        is_filter_pop = False

        while timetable_df_list_back_object[0].empty and filter_priority:
            # 필터링 조건을 뒤에서부터 하나씩 제거하며 시간표를 찾음
            filter_priority.pop()
            is_filter_pop = True

            timetable_df_list_back_object = filter_timetable(
                self.__require_course_timetable_df_list,
                filter_back_object,
                filter_priority,
            )

            print("필터링 조건을 줄여 시간표를 찾는 중...")

        # 취향 순으로 정렬 후 상위 10개만 반환
        timetable_df_list_back_object = sort_timetable_by_taste(
            timetable_df_list_back_object, self.__user_taste
        )[:10]

        timetable_list_front_object = [
            convert_with_front(TO_FRONT, TIMETABLE, timetable_df_back_object)
            for timetable_df_back_object in timetable_df_list_back_object
        ]

        return timetable_list_front_object, is_filter_pop

    def auto_fill_routine(
        self, filter_data_front_object, timetable_front_object, mode_list_front_object
    ):
        """
        시간표를 자동으로 채워주는 함수
        input: 필터링 조건, 시간표, 모드 list
        output: 채워진 시간표 list
        """

        # front 형식의 데이터를 back 형식으로 변환
        filter_data_back_object = convert_with_front(
            TO_BACK, FILTER, filter_data_front_object
        )
        timetable_back_object = convert_with_front(
            TO_BACK, TIMETABLE, timetable_front_object, self.__entire_course_bit_df
        )
        mode_list_back_object = []
        for mode_list_front_object_element in mode_list_front_object:
            mode_list_back_object_element = mode_list_front_object_element.copy()
            if len(mode_list_back_object_element) == 3:
                mode_list_back_object_element[1] = [
                    value
                    for key, value in self.__department_name_to_id_by_curriculum.items()
                    if key.startswith(mode_list_back_object_element[1])
                ][0]
            mode_list_back_object.append(mode_list_back_object_element)

        # mode와 filter_data에 따라 강의 pool 설정
        print("강의 pool 설정 중...")
        # 1. 시간표에 따른 강의 pool 설정
        pool_by_timetable = set_pool_by_timetable(
            self.__entire_course_bit_df, timetable_back_object
        )

        # 2. filter_data에 따른 강의 pool 설정
        pool_by_filter = set_pool_by_filter(
            self.__entire_course_bit_df, filter_data_back_object
        )

        # 3. 1, 2의 교집합 설정
        pool_by_timetable_and_filter = pd.merge(
            pool_by_timetable,
            pool_by_filter,
            on="course_class_id",
            suffixes=("", "_to_drop"),
        )
        pool_by_timetable_and_filter = pool_by_timetable_and_filter.drop(
            columns=[
                col for col in pool_by_timetable_and_filter.columns if "to_drop" in col
            ]
        )

        # 4. mode에 따른 강의 pool 설정
        pool_by_mode_list = [
            set_pool_by_mode(
                (
                    mode_list_back_object_element[2]
                    if len(mode_list_back_object_element) == 3
                    else mode_list_back_object_element[1]
                ),
                self.__department_possible_df_list,
                self.__elective_course_bit_df,
                (
                    mode_list_back_object_element[1]
                    if len(mode_list_back_object_element) == 3
                    else None
                ),
            )
            for mode_list_back_object_element in mode_list_back_object
        ]

        # 4. 통합된 강의 pool 설정
        pool_list = []
        for pool_by_mode in pool_by_mode_list:
            pool = pd.merge(
                pool_by_timetable_and_filter,
                pool_by_mode,
                on="course_class_id",
                suffixes=("", "_to_drop"),
            )
            pool = pool.drop(columns=[col for col in pool.columns if "to_drop" in col])

            pool_list.append(pool)

        print("강의 pool 설정 완료!")

        # 5. auto_fill 실행
        print("시간표 자동 채우기 중...")
        auto_fill_timetable_list = [timetable_back_object]

        for pool, mode in zip(pool_list, mode_list_front_object):
            print(f"{mode} 모드로 시간표 자동 채우기 중...")
            auto_fill_timetable_list_next = []
            for auto_fill_timetable in auto_fill_timetable_list:
                auto_fill_timetable_list = auto_fill(
                    auto_fill_timetable,
                    pool,
                    mode[0],
                )
                auto_fill_timetable_list_next.extend(auto_fill_timetable_list)

            auto_fill_timetable_list = sort_timetable_by_taste(
                auto_fill_timetable_list_next, self.__user_taste
            )[:10]

            print(f"\n{mode} 모드로 시간표 자동 채우기 완료!")
            print(f"총 {len(auto_fill_timetable_list_next)}개의 시간표 생성됨")

        print("시간표 자동 채우기 완료!")
        print(f"총 {len(auto_fill_timetable_list_next)}개의 시간표 생성됨")

        # back 형식의 데이터를 front 형식으로 변환
        timetable_front_object = [
            convert_with_front(TO_FRONT, TIMETABLE, timetable_back_object)
            for timetable_back_object in auto_fill_timetable_list
        ]

        return timetable_front_object


# 테스트 코드
user_taste = [False, 2, False]
user = TimetableInterface(user_taste)
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

user.require_course_timetable_routine([])
print(
    user.timetable_filter_routine(
        [
            ["월요일 15시 ~ 16시 30분", "수요일 15시 ~ 16시 30분"],
            {},
            {"컴퓨터공학과, 컴파일러, CSE4312": "박준석"},
        ],
        ["time", "good", "bad"],
    )
)

auto_fill_result = user.auto_fill_routine(
    [
        ["월요일 15시 ~ 16시 30분", "수요일 15시 ~ 16시 30분"],
        {
            "컴퓨터공학과, 컴파일러, CSE4312": "김지응",
            "컴퓨터공학과, 프로그래밍언어 이론, CSE4232": "김지응",
        },
        {"컴퓨터공학과, 컴파일러, CSE4312": "박준석"},
    ],
    [],
    [
        [6, "컴퓨터공학과", "전공선택"],
        [3, "컴퓨터공학과", "교양필수"],
        [3, "핵심교양 1"],
    ],
)

print(auto_fill_result[0])
