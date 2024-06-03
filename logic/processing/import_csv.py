# csv로 저장된 raw data를 읽어오는 모듈

import os
import pandas as pd

# 현재 저장된 csv 파일명에 따라 학부과-전공명 <-> id dict, list를 만드는 함수
# input: 저장된 csv 파일의 경로
# output: 학부과-전공명 -> id dict, id -> 학부과-전공명 list
def get_department_dict(csv_path):
    department_name_to_id = {}
    id_to_department_name = []

    # csv 파일의 파일명을 읽어옴
    csv_files = os.listdir(csv_path)
    csv_files.sort()

    # csv 파일명을 통해 학부과-전공명을 추출
    for file in enumerate(csv_files):
        file_split = file[1].split("_")
        department_name = file_split[0] + "-" + file_split[3]

        department_name_to_id[department_name] = file[0]
        id_to_department_name.append(department_name)

    return department_name_to_id, id_to_department_name


# csv 파일들을 DataFrame으로 읽어와서 list로 반환하는 함수
# input: csv 파일의 경로
# output: DataFrame list
def import_csv(csv_path):
    csv_files = os.listdir(csv_path)
    csv_files.sort()

    data_list = []
    for file in csv_files:
        data = pd.read_csv(csv_path + "/" + file)
        data_list.append(data)

    return data_list


# 테스트 코드
RAW_PATH = "resource/raw"

department_name_to_id, id_to_department_name = get_department_dict(RAW_PATH)
imported_data = import_csv(RAW_PATH)

print(imported_data[department_name_to_id["컴퓨터공학과-컴퓨터공학"]])
