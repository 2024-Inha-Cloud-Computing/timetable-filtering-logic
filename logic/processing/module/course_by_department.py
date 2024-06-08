# 각 학과가 들어야하는 강의를 교양, 전공으로 분류한 DataFrame 생성 모듈

import pandas as pd


# 커리큘럼에 있는 학과를 토대로 DataFrame을 생성
# input: 커리큘럼에 있는 학과의 id -> 학과이름 변환 list
# output: 커리큘럼에 있는 학과를 토대로 2개씩 생성된 빈 DataFrame 2차원 list (전공, 교양필수)
def create_empty_department_possible_df(department_id_to_name_for_curriculum):
    # 학과별 빈 DataFrame 2차원 list 생성
    empty_department_possible_df_list = [
        [pd.DataFrame(), pd.DataFrame()]
        for _ in range(len(department_id_to_name_for_curriculum))
    ]

    return empty_department_possible_df_list


# 학과 이름이 df_course_list에 있으면, 해당 강의를 전공과 교양필수로 나누어 DataFrame에 추가
# input: 학과별 강의 DataFrame list
#        전체 강의 DataFrame (시간이 bit ndarray로 변환된 DataFrame)
#        커리큘럼에 있는 학과의 id -> 학과이름 변환 list
#        강의시간표에 있는 학과의 학과이름 -> id 변환 dict
# output: 학과별로 강의가 추가된 DataFrame 2차원 list (전공, 교양필수)
def add_include_course_to_department_possible_df(
    df_course_list,
    entire_course_bit_df,
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

            # 필터링 된 과목을 course_class_id로 entire_course_df에서 찾아 스위칭
            df_major = entire_course_bit_df[
                entire_course_bit_df["course_class_id"].isin(
                    df_major["course_class_id"]
                )
            ]
            df_liberal_required = entire_course_bit_df[
                entire_course_bit_df["course_class_id"].isin(
                    df_liberal_required["course_class_id"]
                )
            ]

            # department_possible_df_list에 추가
            department_possible_df_list[department_id][0] = df_major
            department_possible_df_list[department_id][1] = df_liberal_required

    return department_possible_df_list


# 학과별 대학교교양필수(GEB) 과목을 교양필수 DataFrame에 추가
# input: 전체 강의 DataFrame (시간이 bit ndarray로 변환된 DataFrame)
#        학과별 커리큘럼 DataFrame list
#        학과별 강의가 추가된 DataFrame 2차원 list (전공, 교양필수)
#        커리큘럼에 있는 학과의 id -> 학과이름 변환 list
# output: 학과별로 강의가 추가된 DataFrame 2차원 list (전공, 교양필수)
def add_geb_to_department_possible_df(
    entire_course_bit_df,
    df_curriculum_list,
    department_possible_df_list,
    department_id_to_name_for_curriculum,
):
    for department_id, department_name in enumerate(
        department_id_to_name_for_curriculum
    ):
        # 현재 학과의 커리큘럼 DataFrame
        df_curriculum_cur = df_curriculum_list[department_id]

        # 커리큘럼에 있는 대학교교양필수(GEB) 과목을 필터링
        df_geb = df_curriculum_cur[
            df_curriculum_cur["학수번호"].str.contains("GEB", na=False)
        ]

        # 필터링 된 과목을 entire_course_df에서 찾아 교양필수 DataFrame에 추가
        df_geb = entire_course_bit_df[
            entire_course_bit_df["course_id"].isin(df_geb["학수번호"])
        ]

        # department_possible_df_list에 추가
        department_possible_df_list[department_id][1] = pd.concat(
            [department_possible_df_list[department_id][1], df_geb]
        )

    return department_possible_df_list


# 학과별 핵심교양(GED) 과목을 교양필수 DataFrame에 추가
# input: 전체 강의 DataFrame (시간이 bit ndarray로 변환된 DataFrame)
#        학과별 커리큘럼 DataFrame list
#        학과별 강의가 추가된 DataFrame 2차원 list (전공, 교양필수)
#        커리큘럼에 있는 학과의 id -> 학과이름 변환 list
# output: 학과별로 강의가 추가된 DataFrame 2차원 list (전공, 교양필수)
def add_ged_to_department_possible_df(
    entire_course_bit_df,
    df_curriculum_list,
    department_possible_df_list,
    department_id_to_name_for_curriculum,
):
    for department_id, department_name in enumerate(
        department_id_to_name_for_curriculum
    ):
        # 현재 학과의 커리큘럼 DataFrame
        df_curriculum_cur = df_curriculum_list[department_id]

        # 커리큘럼에 있는 핵심교양(GED) 과목을 필터링
        df_ged = df_curriculum_cur[
            df_curriculum_cur["교과목명"].str.contains("핵심교양-")
        ]

        # 핵심교양-{숫자} 문자열을 GED{숫자}로 변경
        df_ged.loc[:, "교과목명"] = df_ged["교과목명"].apply(
            lambda x: "GED" + x.split("-")[1][0]
        )

        # 필터링 된 과목을 entire_course_df에서 찾아 교양필수 DataFrame에 추가
        df_ged = entire_course_bit_df[
            entire_course_bit_df["course_id"].apply(
                lambda x: any(x.startswith(ged) for ged in df_ged["교과목명"])
            )
        ]

        # department_possible_df_list에 추가
        department_possible_df_list[department_id][1] = pd.concat(
            [department_possible_df_list[department_id][1], df_ged]
        )

    return department_possible_df_list
