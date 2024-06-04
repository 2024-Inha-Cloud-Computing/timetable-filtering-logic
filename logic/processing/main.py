# 학과 별 csv 파일을 메인 로직에서 사용하기 편하게 가공하는 모듈

import pandas as pd

import import_csv
import entire_course
import time_str_to_bit
import course_by_time

RAW_PATH = "resource/raw"
PROCESSED_PATH = "resource/processed"

# [import_csv 모듈] 학과별 강의 & 인덱싱 csv 파일 생성
department_name_to_id, department_id_to_name = import_csv.get_department_dict(RAW_PATH)
df_list_by_departement = import_csv.import_csv(RAW_PATH)

# department_name_to_id, department_id_to_name csv 파일 생성
department_name_to_id_df = pd.DataFrame.from_dict(
    department_name_to_id, orient="index", columns=["id"]
)
department_id_to_name_df = pd.DataFrame(department_id_to_name, columns=["department"])

department_name_to_id_df.to_csv(
    f"{PROCESSED_PATH}/department_index/department_name_to_id.csv"
)
department_id_to_name_df.to_csv(
    f"{PROCESSED_PATH}/department_index/department_id_to_name.csv"
)

# 학과별 csv 파일 생성
for department_id, df in enumerate(df_list_by_departement):
    department_name = department_id_to_name[department_id]
    df.to_csv(f"{PROCESSED_PATH}/import_csv/{department_name}.csv")

# 출력 테스트 코드
print(df_list_by_departement[department_name_to_id["컴퓨터공학과-컴퓨터공학"]])


# [entire_course 모듈] 학과별 csv 파일을 하나로 병합한 csv 파일 생성
df_list_by_departement = import_csv.import_csv(RAW_PATH)
entire_course_df = entire_course.get_entire_course_df(df_list_by_departement)

entire_course_df.to_csv(f"{PROCESSED_PATH}/entire_course/entire_course.csv")

# 출력 테스트 코드
print(entire_course_df)

# [time_str_to_bit 모듈] 시간 문자열을 bit로 변환한 csv 파일 생성
print(time_str_to_bit.time_str_to_bit("화9"))

entire_course_bit_df = time_str_to_bit.time_str_to_bit_df(
    entire_course_df, "time_classroom"
)

entire_course_bit_df.to_csv(f"{PROCESSED_PATH}/time_str_to_bit/entire_course_bit.csv")
print(entire_course_bit_df)


# [course_by_time 모듈] 특정 시간 강의들의 csv 파일 생성
course_by_all_time = course_by_time.get_course_by_all_time(entire_course_bit_df)

for day_index, day_df_list in enumerate(course_by_all_time):
    for time_index, time_df in enumerate(day_df_list):
        time_df.to_csv(f"{PROCESSED_PATH}/course_by_time/{day_index}_{time_index}.csv")

# 출력 테스트 코드
print(course_by_all_time)
