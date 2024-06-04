# 과 별로 이루어진 강의 시간표를 메인 로직에서 사용하기 편하게 가공하는 모듈

import import_csv
import entire_course
import time_str_to_bit

# import_csv 모듈 테스트 코드
RAW_PATH = "resource/raw"

department_name_to_id, id_to_department_name = import_csv.get_department_dict(RAW_PATH)
imported_data = import_csv.import_csv(RAW_PATH)

for department_name, data in zip(id_to_department_name, imported_data):
    data.to_csv(f"export/import_csv/{department_name}.csv", index=False)
print(imported_data[department_name_to_id["컴퓨터공학과-컴퓨터공학"]])


# entire_course 모듈 테스트 코드
RAW_PATH = "resource/raw"

imported_data = import_csv.import_csv(RAW_PATH)
merged_data = entire_course.merge_all_data(imported_data)

merged_data.to_csv("export/entire_course/merged_data.csv", index=False)
print(merged_data)

# time_str_to_bit 모듈 테스트 코드
RAW_PATH = "resource/raw"

imported_data = import_csv.import_csv(RAW_PATH)
merged_data = entire_course.merge_all_data(imported_data)
merged_data_time_bit = time_str_to_bit.time_str_to_bit_df(merged_data, "time_classroom")

merged_data_time_bit.to_csv(
    "export/time_str_to_bit/merged_data_time_bit.csv", index=False
)
print(merged_data_time_bit)
