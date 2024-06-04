# 모든 강좌 데이터가 들어있는 DataFrame을 만드는 모듈

import pandas as pd

# 과 별 강의 데이터를 모두 합쳐서 하나의 DataFrame으로 만드는 함수
# input: DataFrame list
# output: DataFrame
def merge_all_data(data_list):
    merged_data = pd.DataFrame()

    # 모든 DataFrame을 하나로 병합
    for data in data_list:
        merged_data = pd.concat([merged_data, data])

    # 학수번호를 기준으로 정렬
    merged_data = merged_data.sort_values(by="course_class_id", ignore_index=True)

    # 중복된 학수번호를 출력하는 테스트 코드
    # duplicated = merged_data[merged_data.duplicated(subset="course_class_id", keep=False)]
    # print(duplicated)

    # 중복된 학수번호를 가진 행을 제거
    merged_data = merged_data.drop_duplicates(subset="course_class_id", keep="first", ignore_index=True)
    
    return merged_data

# 테스트 코드
# import import_csv

# RAW_PATH = "resource/raw"

# imported_data = import_csv.import_csv(RAW_PATH)
# merged_data = merge_all_data(imported_data)

# print(merged_data)