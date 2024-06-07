# 학과 별 csv 파일을 메인 로직에서 사용하기 편하게 가공하는 모듈

import pandas as pd

from import_csv import *
from entire_course import *
from time_str_to_bit import *
from course_by_time import *
from course_by_department import *

RESOURCE_PATH = "resource"
RAW_PATH = f"{RESOURCE_PATH}/raw"
PROCESSED_PATH = f"{RESOURCE_PATH}/processed"
PROCESSED_DEPARTMENT_INDEX_PATH = f"{PROCESSED_PATH}/department_index"
PROCESSED_IMPORT_PATH = f"{PROCESSED_PATH}/import_csv"
PROCESSED_ENTIRE_COURSE_PATH = f"{PROCESSED_PATH}/entire_course"
PROCESSED_TIME_STR_TO_BIT_PATH = f"{PROCESSED_PATH}/time_str_to_bit"
PROCESSED_COURSE_BY_TIME_PATH = f"{PROCESSED_PATH}/course_by_time"
PROCESSED_COURSE_BY_DEPARTMENT_PATH = f"{PROCESSED_PATH}/course_by_department"


# [import_csv 모듈] 학과별 강의/커리큘럼 & 인덱싱 csv 파일 생성
# input: data_type (course 또는 curriculum)
# output: 학과 별 강의 or 커리큘럼이 담긴 DataFrame list
def import_csv_module(data_type):
    # 학과별 강의/커리큘럼 & 인덱싱을 위한 변수 초기화
    if data_type == "course":
        department_name_to_id, department_id_to_name, df_list = import_routine(
            f"{RAW_PATH}/{data_type}"
        )
    elif data_type == "curriculum":
        department_name_to_id, department_id_to_name, df_list = import_routine(
            f"{RAW_PATH}/{data_type}"
        )
    else:
        raise ValueError(
            "타입 입력이 잘못되었습니다. 'course' 또는 'curriculum'을 입력해주세요."
        )

    # csv로 변환하기 위한 DataFrame 생성
    department_name_to_id_df = pd.DataFrame.from_dict(
        department_name_to_id, orient="index", columns=["id"]
    )
    department_id_to_name_df = pd.DataFrame(
        department_id_to_name, columns=["department"]
    )

    # csv 파일로 저장
    department_name_to_id_df.to_csv(
        f"{PROCESSED_DEPARTMENT_INDEX_PATH}/department_name_to_id_for_{data_type}.csv"
    )
    department_id_to_name_df.to_csv(
        f"{PROCESSED_DEPARTMENT_INDEX_PATH}/department_id_to_name_for_{data_type}.csv"
    )

    for department_id, df in enumerate(df_list):
        department_name = department_id_to_name[department_id]
        df.to_csv(f"{PROCESSED_IMPORT_PATH}/{data_type}/{department_name}.csv")

    # 출력 테스트 코드
    print(department_name_to_id)
    print(department_id_to_name)
    print(df_list[department_name_to_id["컴퓨터공학과-컴퓨터공학"]])
    print("import_csv_module 출력 끝.")

    return department_name_to_id, department_id_to_name, df_list


# [entire_course 모듈] 학과별 csv 파일을 하나로 병합한 csv 파일 생성
# input: 학과 별 강의가 담긴 DataFrame list
# output: 모든 학과의 강의가 담긴 DataFrame
def entire_course_module(df_course_list):
    entire_course_df = get_entire_course_df(df_course_list)
    elective_course_df = get_elective_course_df(entire_course_df)

    entire_course_df.to_csv(f"{PROCESSED_ENTIRE_COURSE_PATH}/entire_course.csv")
    elective_course_df.to_csv(f"{PROCESSED_ENTIRE_COURSE_PATH}/elective_course.csv")

    # 출력 테스트 코드
    print(entire_course_df)
    print(elective_course_df)
    print("entire_course_module 출력 끝.")

    return entire_course_df, elective_course_df


# [time_str_to_bit 모듈] 시간 문자열을 bit로 변환한 csv 파일 생성
# input: 모든 학과의 강의가 담긴 DataFrame
# output: 시간 문자열을 bit로 변환한 DataFrame
def time_str_to_bit_module(entire_course_df, elective_course_df, column_name):
    entire_course_bit_df = time_str_to_bit_df(entire_course_df, column_name)
    elective_course_bit_df = time_str_to_bit_df(elective_course_df, column_name)

    entire_course_bit_df.to_csv(
        f"{PROCESSED_TIME_STR_TO_BIT_PATH}/entire_course_bit.csv"
    )
    elective_course_bit_df.to_csv(
        f"{PROCESSED_TIME_STR_TO_BIT_PATH}/elective_course_bit.csv"
    )

    # 출력 테스트 코드
    print(entire_course_bit_df)
    print(elective_course_bit_df)
    print("time_str_to_bit_module 출력 끝.")

    return entire_course_bit_df, elective_course_bit_df


# [course_by_time 모듈] 특정 시간 강의들의 csv 파일 생성
# input: 시간 문자열을 bit로 변환한 DataFrame
# output: None
def course_by_time_module(course_bit_df):
    course_by_all_time = get_course_by_all_time(course_bit_df)

    for day_index, day_df_list in enumerate(course_by_all_time):
        for time_index, time_df in enumerate(day_df_list):
            time_df.to_csv(
                f"{PROCESSED_COURSE_BY_TIME_PATH}/{day_index}_{time_index}.csv"
            )

    # 출력 테스트 코드
    print(course_by_all_time[3][10])
    print("course_by_time_module 출력 끝.")


# [course_by_department 모듈]각 학과가 들어야하는 강의를 교양, 전공으로 분류한 csv 파일 생성
# input: df_course_list, department_possible_df_list, department_id_to_name_for_curriculum, department_name_to_id_for_course
# output: 학과별로 강의가 추가된 DataFrame 2차원 list (전공, 교양필수, 교양선택)
def course_by_department_module(
    df_course_list,
    entire_course_bit_df,
    department_id_to_name_for_curriculum,
    department_name_to_id_for_course,
):
    # 커리큘럼에 있는 학과를 토대로 DataFrame을 생성
    department_possible_df_list = create_empty_department_possible_df(
        department_id_to_name_for_curriculum
    )
    # 학과 이름이 df_course_list에 있으면, 해당 강의를 전공과 교양필수로 나누어 DataFrame에 추가
    department_possible_df_list = add_include_course_to_department_possible_df(
        df_course_list,
        entire_course_bit_df,
        department_possible_df_list,
        department_id_to_name_for_curriculum,
        department_name_to_id_for_course,
    )

    add_geb_to_department_possible_df(
        entire_course_bit_df,
        df_curriculum_list,
        department_possible_df_list,
        department_id_to_name_for_curriculum,
    )

    add_ged_to_department_possible_df(
        entire_course_bit_df,
        df_curriculum_list,
        department_possible_df_list,
        department_id_to_name_for_curriculum,
    )

    # csv 파일로 저장
    for department_id, department_name in enumerate(
        department_id_to_name_for_curriculum
    ):
        department_possible_df_list[department_id][0].to_csv(
            f"{PROCESSED_COURSE_BY_DEPARTMENT_PATH}/{department_name}_major.csv"
        )
        department_possible_df_list[department_id][1].to_csv(
            f"{PROCESSED_COURSE_BY_DEPARTMENT_PATH}/{department_name}_liberal_required.csv"
        )

    # 출력 테스트 코드
    print(
        department_possible_df_list[
            department_name_to_id_for_curriculum["컴퓨터공학과-컴퓨터공학"]
        ]
    )
    print("course_by_department_module 출력 끝.")


# main 함수
if __name__ == "__main__":
    df_course_list = None
    df_curriculum_list = None
    department_name_to_id_for_course = None
    department_name_to_id_for_curriculum = None
    department_id_to_name_for_course = None
    department_id_to_name_for_curriculum = None

    # csv 파일을 불러와 여러 변수로 저장
    for data_type in ["course", "curriculum"]:
        department_name_to_id, department_id_to_name, df_list = import_csv_module(
            data_type
        )

        if data_type == "course":
            df_course_list = df_list
            department_name_to_id_for_course = department_name_to_id
            department_id_to_name_for_course = department_id_to_name
        elif data_type == "curriculum":
            df_curriculum_list = df_list
            department_name_to_id_for_curriculum = department_name_to_id
            department_id_to_name_for_curriculum = department_id_to_name

    # 모듈 실행
    entire_course_df, elective_course_df = entire_course_module(df_course_list)
    entire_course_bit_df, elective_course_bit_df = time_str_to_bit_module(
        entire_course_df, elective_course_df, "time_classroom"
    )
    course_by_time_module(entire_course_bit_df)

    department_possible_df_list = course_by_department_module(
        df_course_list,
        entire_course_bit_df,
        department_id_to_name_for_curriculum,
        department_name_to_id_for_course,
    )
