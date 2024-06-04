# 학과 별 csv 파일을 메인 로직에서 사용하기 편하게 가공하는 모듈

import import_csv
import entire_course
import time_str_to_bit
import course_by_time

RAW_PATH = "resource/raw"
PROCESSED_PATH = "resource/processed"

# [import_csv 모듈] 학과별 csv 파일 생성
department_name_to_id, department_id_to_name = import_csv.get_department_dict(RAW_PATH)
df_list_by_departement = import_csv.import_csv(RAW_PATH)

for department_id, df in enumerate(df_list_by_departement):
    department_name = department_id_to_name[department_id]
    df.to_csv(f"{PROCESSED_PATH}/import_csv/{department_name}.csv")

# 출력 테스트 코드
print(df_list_by_departement[department_name_to_id["컴퓨터공학과-컴퓨터공학"]])


# # entire_course 모듈 테스트 코드
# RAW_PATH = "resource/raw"

# df_list_by_departement = import_csv.import_csv(RAW_PATH)
# merged_data = entire_course.merge_all_data(df_list_by_departement)

# merged_data.to_csv("export/entire_course/merged_data.csv", index=False)
# print(merged_data)

# # time_str_to_bit 모듈 테스트 코드
# RAW_PATH = "resource/raw"

# df_list_by_departement = import_csv.import_csv(RAW_PATH)
# merged_data = entire_course.merge_all_data(df_list_by_departement)
# merged_data_time_bit = time_str_to_bit.time_str_to_bit_df(
#     merged_data.copy(), "time_classroom"
# )

# merged_data_time_bit.to_csv(
#     "export/time_str_to_bit/merged_data_time_bit.csv", index=False
# )
# print(merged_data_time_bit)


# # course_by_time 모듈 테스트 코드
# RAW_PATH = "resource/raw"

# df_list_by_departement = import_csv.import_csv(RAW_PATH)
# merged_data = entire_course.merge_all_data(df_list_by_departement)
# merged_data_time_bit = time_str_to_bit.time_str_to_bit_df(
#     merged_data.copy(), "time_classroom"
# )
# course_by_all_time = course_by_time.course_by_all_time(merged_data_time_bit)

# for day_index, day in enumerate(course_by_all_time):
#     for time_index, time in enumerate(day):
#         time.to_csv(f"export/course_by_time/{day_index}_{time_index}.csv", index=False)
# print(course_by_all_time)
