# 각 학과가 들어야하는 강의를 교양, 전공으로 분류한 csv 파일 생성 모듈

import pandas as pd


# 커리큘럼에 있는 학과를 토대로 DataFrame을 생성
# input: department_id_to_name_for_curriculum, department_name_to_id_for_curriculum
# output: 커리큘럼에 있는 학과를 토대로 2개씩 생성된 빈 DataFrame 2차원 list
def create_empty_department_possible_df(department_id_to_name_for_curriculum):
    # 학과별 빈 DataFrame tuple list 생성
    empty_department_possible_df_list = [
        [pd.DataFrame(), pd.DataFrame()]
        for _ in range(len(department_id_to_name_for_curriculum))
    ]

    return empty_department_possible_df_list


# 학과 이름이 df_course_list에 있으면, 해당 강의를 DataFrame에 추가
# input: df_course_list, department_possible_df_list, department_id_to_name_for_curriculum, department_name_to_id_for_course
# output: 학과별로 강의가 추가된 DataFrame 2차원 list (전공, 교양)
def add_course_to_department_possible_df(
    df_course_list,
    department_possible_df_list,
    department_id_to_name_for_curriculum,
    department_name_to_id_for_course,
):
    for department_id, department_name in enumerate(
        department_id_to_name_for_curriculum
    ):
        if department_name in department_name_to_id_for_course:
            department_possible_df_list[department_id][0] = pd.concat(
                [
                    department_possible_df_list[department_id][0],
                    df_course_list[department_name_to_id_for_course[department_name]],
                ]
            )

    return department_possible_df_list
