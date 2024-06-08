# 앱의 진행에 따라 필요한 필터링을 수행하는 모듈

import search_course

import pandas as pd

# 파일 저장 경로
RESOURCE_PATH = "resource"
PROCESSED_PATH = f"{RESOURCE_PATH}/processed"
PROCESSED_DEPARTMENT_INDEX_PATH = f"{PROCESSED_PATH}/department_index"
PROCESSED_IMPORT_PATH = f"{PROCESSED_PATH}/import_csv"
PROCESSED_ENTIRE_COURSE_PATH = f"{PROCESSED_PATH}/entire_course"
PROCESSED_TIME_STR_TO_BIT_PATH = f"{PROCESSED_PATH}/time_str_to_bit"
PROCESSED_COURSE_BY_TIME_PATH = f"{PROCESSED_PATH}/course_by_time"
PROCESSED_COURSE_BY_DEPARTMENT_PATH = f"{PROCESSED_PATH}/course_by_department"

# 요일, 교시
DAY_NUM = 7
TIME_NUM = 31


class Filtering:
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
        # return 값으로 사용할 변수 초기화
        department_name_to_id_for_course = {}
        department_id_to_name_for_course = []
        department_name_to_id_for_curriculum = {}
        department_id_to_name_for_curriculum = []
        department_course_df_list = []
        department_curriculum_df_list = []

        for data_type in ["course", "curriculum"]:
            department_name_to_id = pd.read_csv(
                f"{PROCESSED_DEPARTMENT_INDEX_PATH}/department_name_to_id_for_{data_type}.csv",
                index_col=0,
            ).to_dict()["id"]
            department_id_to_name = [
                element[0]
                for element in pd.read_csv(
                    f"{PROCESSED_DEPARTMENT_INDEX_PATH}/department_id_to_name_for_{data_type}.csv",
                    index_col=0,
                ).values.tolist()
            ]
            df_list = [
                pd.read_csv(
                    f"{PROCESSED_IMPORT_PATH}/{data_type}/{department_name}.csv"
                )
                for department_name in department_id_to_name
            ]

            if data_type == "course":
                department_name_to_id_for_course = department_name_to_id
                department_id_to_name_for_course = department_id_to_name
                df_course_list = df_list
            elif data_type == "curriculum":
                department_name_to_id_for_curriculum = department_name_to_id
                department_id_to_name_for_curriculum = department_id_to_name
                df_curriculum_list = df_list

        entire_course_df = pd.read_csv(
            f"{PROCESSED_ENTIRE_COURSE_PATH}/entire_course.csv"
        )

        entire_course_bit_df = pd.read_csv(
            f"{PROCESSED_TIME_STR_TO_BIT_PATH}/entire_course_bit.csv"
        )
        elective_course_bit_df = pd.read_csv(
            f"{PROCESSED_ENTIRE_COURSE_PATH}/elective_course.csv"
        )

        course_by_all_time = [
            [
                pd.read_csv(f"{PROCESSED_COURSE_BY_TIME_PATH}/{day}_{time}.csv")
                for time in range(TIME_NUM)
            ]
            for day in range(DAY_NUM)
        ]

        department_possible_df_list = [
            [
                pd.read_csv(
                    f"{PROCESSED_COURSE_BY_DEPARTMENT_PATH}/{department_name}_major.csv"
                ),
                pd.read_csv(
                    f"{PROCESSED_COURSE_BY_DEPARTMENT_PATH}/{department_name}_liberal_required.csv"
                ),
            ]
            for department_name in department_id_to_name_for_curriculum
        ]

        return (
            department_name_to_id_for_course,
            department_id_to_name_for_course,
            department_name_to_id_for_curriculum,
            department_id_to_name_for_curriculum,
            df_course_list,
            df_curriculum_list,
            entire_course_df,
            entire_course_bit_df,
            elective_course_bit_df,
            course_by_all_time,
            department_possible_df_list,
        )

    def search_course_routine(self, search_word):
        # search_course 모듈의 search_course 함수 호출
        return search_course.search_course(search_word, self.__entire_course_df)


# 테스트 코드
user_data = {
    "학과": "컴퓨터공학과-컴퓨터공학",
}
filtering_user_0 = Filtering(user_data)
search_word = "컴퓨터"

print(filtering_user_0.search_course_routine(search_word))
