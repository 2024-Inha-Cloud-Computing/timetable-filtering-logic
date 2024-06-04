# 모든 강의 csv 파일 생성 모듈

import pandas as pd


# 학과 별 강의 데이터를 모두 합쳐서 하나의 DataFrame으로 만드는 함수
# input: DataFrame list
# output: DataFrame
def merge_all_data(df_list_by_department):
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
