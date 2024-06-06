# 학과 별 csv 파일을 메인 로직에서 사용하기 편하게 가공하는 모듈

import pandas as pd

from import_csv import *
from entire_course import *
from time_str_to_bit import *
from course_by_time import *

RESOURCE_PATH = "resource"

RAW_PATH = f"{RESOURCE_PATH}/raw"

PROCESSED_PATH = f"{RESOURCE_PATH}/processed"

PROCESSED_DEPARTMENT_INDEX_PATH = f"{PROCESSED_PATH}/department_index"

PROCESSED_IMPORT_PATH = f"{PROCESSED_PATH}/import_csv"


# [import_csv 모듈] 학과별 강의/커리큘럼 & 인덱싱 csv 파일 생성
# input: type (str) - "course" or "curriculum"
# output: None
def import_csv_module(data_type):
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

    department_name_to_id_df = pd.DataFrame.from_dict(
        department_name_to_id, orient="index", columns=["id"]
    )
    department_id_to_name_df = pd.DataFrame(
        department_id_to_name, columns=["department"]
    )

    department_name_to_id_df.to_csv(
        f"{PROCESSED_DEPARTMENT_INDEX_PATH}/department_name_to_id_for_{data_type}.csv"
    )
    department_id_to_name_df.to_csv(
        f"{PROCESSED_DEPARTMENT_INDEX_PATH}/department_id_to_name_for_{data_type}.csv"
    )

    for department_id, df in enumerate(df_list):
        department_name = department_id_to_name[department_id]
        df.to_csv(f"{PROCESSED_IMPORT_PATH}/{data_type}/{department_name}.csv")

    print(department_name_to_id)
    print(department_id_to_name)
    print(df_list[department_name_to_id["컴퓨터공학과-컴퓨터공학"]])


for data_type in ["course", "curriculum"]:
    import_csv_module(data_type)
exit()

# [entire_course 모듈] 학과별 csv 파일을 하나로 병합한 csv 파일 생성
entire_course_df = get_entire_course_df(df_course_list)

entire_course_df.to_csv(f"{PROCESSED_PATH}/entire_course/entire_course.csv")

# 출력 테스트 코드
print(entire_course_df)

# [time_str_to_bit 모듈] 시간 문자열을 bit로 변환한 csv 파일 생성
print(time_str_to_bit("화9"))

entire_course_bit_df = time_str_to_bit_df(entire_course_df, "time_classroom")

entire_course_bit_df.to_csv(f"{PROCESSED_PATH}/time_str_to_bit/entire_course_bit.csv")
print(entire_course_bit_df)


# [course_by_time 모듈] 특정 시간 강의들의 csv 파일 생성
course_by_all_time = get_course_by_all_time(entire_course_bit_df)

for day_index, day_df_list in enumerate(course_by_all_time):
    for time_index, time_df in enumerate(day_df_list):
        time_df.to_csv(f"{PROCESSED_PATH}/course_by_time/{day_index}_{time_index}.csv")

# 출력 테스트 코드
print(course_by_all_time)
