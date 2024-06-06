# 각 학과가 들어야하는 강의를 교양, 전공으로 분류한 csv 파일 생성 모듈

import pandas as pd


# 커리큘럼에 있는 학과를 토대로 DataFrame을 생성
# input: department_id_to_name_for_curriculum, department_name_to_id_for_curriculum
# output: 커리큘럼에 있는 학과를 토대로 3개씩 생성된 빈 DataFrame 2차원 list (전공, 교양필수, 교양선택)
def create_empty_department_possible_df(department_id_to_name_for_curriculum):
    # 학과별 빈 DataFrame 2차원 list 생성
    empty_department_possible_df_list = [
        [pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]
        for _ in range(len(department_id_to_name_for_curriculum))
    ]

    return empty_department_possible_df_list


# 학과 이름이 df_course_list에 있으면, 해당 강의를 전공과 교양필수로 나누어 DataFrame에 추가
# input: df_course_list, department_possible_df_list, department_id_to_name_for_curriculum, department_name_to_id_for_course
# output: 학과별로 강의가 추가된 DataFrame 2차원 list (전공, 교양필수, 교양선택)
def add_include_course_to_department_possible_df(
    df_course_list,
    department_possible_df_list,
    department_id_to_name_for_curriculum,
    department_name_to_id_for_course,
):
    for department_id, department_name in enumerate(
        department_id_to_name_for_curriculum
    ):
        if department_name in department_name_to_id_for_course:
            # 현재 학과의 course DataFrame
            df_course_cur = df_course_list[
                department_name_to_id_for_course[department_name]
            ]

            # course_classification이 교양필수가 아닌 경우 -> 전공으로 분류
            df_major = df_course_cur[
                df_course_cur["course_classification"] != "교양필수"
            ]

            # course_classification이 교양필수인 경우 -> 교양필수로 분류
            df_liberal_required = df_course_cur[
                df_course_cur["course_classification"] == "교양필수"
            ]

            # department_possible_df_list에 추가
            department_possible_df_list[department_id][0] = df_major
            department_possible_df_list[department_id][1] = df_liberal_required

    return department_possible_df_list
