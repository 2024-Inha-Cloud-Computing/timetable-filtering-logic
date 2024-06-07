# 모든 & 교양선택 강의 csv 파일 생성 모듈

import pandas as pd


# 학과 별 강의 데이터를 모두 합쳐서 하나의 DataFrame으로 만드는 함수
# input: 학과별 강의가 담긴 DataFrame list
# output: 모든 학과의 강의가 담긴 DataFrame
def get_entire_course_df(df_list_by_department):
    entire_course_df = pd.DataFrame()

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


# 전체 강의 DataFrame을 받아서 교양선택 강의만 추출하는 함수
# input: entire_course_df
# output: 교양선택 강의만 추출한 DataFrame
def get_elective_course_df(entire_course_df):
    # course_classification이 교양선택, 일반선택인 행만 추출
    elective_course_df = entire_course_df[
        entire_course_df["course_classification"].str.contains("교양선택|일반선택")
    ]

    return elective_course_df
