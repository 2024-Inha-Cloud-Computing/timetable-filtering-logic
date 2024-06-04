# 앱의 진행에 따라 필요한 필터링을 수행하는 모듈

import search_course

import pandas as pd

# csv 파일 경로
PROCESSED_PATH = "resource/processed"
DAY_NUM = 7
TIME_NUM = 31


class Filtering:
    def __init__(self, user_data):
        # json 데이터를 받아서 __user_data에 Series 형태로 저장
        self.__user_data = pd.Series(user_data)

        # 강의 데이터 불러오기
        (
            self.__department_name_to_id,
            self.__department_id_to_name,
            self.__department_course_df_list,
            self.__entire_course_df,
            self.__entire_course_bit_df,
            self.__course_by_all_time,
        ) = self.__import_processed_data()

    def __import_processed_data(self):
        department_name_to_id = pd.read_csv(
            f"{PROCESSED_PATH}/department_index/department_name_to_id.csv", index_col=0
        ).to_dict()["id"]
        department_id_to_name = [
            element[0]
            for element in pd.read_csv(
                f"{PROCESSED_PATH}/department_index/department_id_to_name.csv",
                index_col=0,
            ).values.tolist()
        ]
        department_course_df_list = [
            pd.read_csv(f"{PROCESSED_PATH}/import_csv/{department}.csv")
            for department in department_id_to_name
        ]
        entire_course_df = pd.read_csv(
            f"{PROCESSED_PATH}/entire_course/entire_course.csv"
        )
        entire_course_bit_df = pd.read_csv(
            f"{PROCESSED_PATH}/time_str_to_bit/entire_course_bit.csv"
        )
        course_by_all_time = [
            [
                pd.read_csv(f"{PROCESSED_PATH}/course_by_time/{day}_{time}.csv")
                for time in range(TIME_NUM)
            ]
            for day in range(DAY_NUM)
        ]

        return (
            department_name_to_id,
            department_id_to_name,
            department_course_df_list,
            entire_course_df,
            entire_course_bit_df,
            course_by_all_time,
        )

    def search_course_routine(self, search_word):
        # search_course 모듈의 search_course 함수 호출
        return search_course.search_course(search_word, self.__entire_course_df)


# 테스트 코드
user_data = {}
filtering_user_0 = Filtering(user_data)
search_word = "컴퓨터"

print(filtering_user_0.search_course_routine(search_word))
