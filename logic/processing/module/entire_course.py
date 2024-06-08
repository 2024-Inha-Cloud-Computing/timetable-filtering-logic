# 전체 & 교양선택 강의 csv 파일 생성 모듈

import pandas as pd


# 학과별 강의 전체를 하나의 DataFrame으로 만드는 함수
# input: 학과별 강의 DataFrame list
# output: 전체 강의 DataFrame
def get_entire_course_df(df_list_by_department, department_id_to_name_for_course):
    entire_course_df = pd.DataFrame()

    for department_id, department_name in enumerate(department_id_to_name_for_course):
        # 각 DataFrame에 학과 정보를 추가
        df_list_by_department[department_id]["department"] = department_name

    # 모든 DataFrame을 하나로 병합
    for df in df_list_by_department:
        entire_course_df = pd.concat([entire_course_df, df], ignore_index=True)

    # 학수번호를 기준으로 정렬
    entire_course_df = entire_course_df.sort_values(
        by="course_class_id", ignore_index=True
    )

    # 중복된 학수번호를 가진 행을 제거
    entire_course_df = entire_course_df.drop_duplicates(
        subset="course_class_id", ignore_index=True
    )

    return entire_course_df


# 전체 강의 DataFrame 중 교양선택 강의를 추출하는 함수
# input: 전체 강의 DataFrame
# output: 교양선택 강의 DataFrame
def get_elective_course_df(entire_course_df):
    # course_classification이 교양선택, 일반선택인 행만 추출
    elective_course_df = entire_course_df[
        entire_course_df["course_classification"].str.contains("교양선택|일반선택")
    ]

    return elective_course_df
