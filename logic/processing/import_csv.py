# 각 학과 별 csv 파일 생성 모듈

import os
import pandas as pd


# 현재 저장된 csv 파일명에 따라 [학부과-전공명 <-> id] 간의 변환이 가능한 dict, list를 만드는 함수
# input: csv 파일(raw data)의 경로
# output: 학부과-전공명 -> id dict, id -> 학부과-전공명 list
def get_department_dict(csv_path):
    department_name_to_id = {}
    department_id_to_name = []

    # csv 파일의 파일명을 읽어옴
    csv_files = os.listdir(csv_path)
    csv_files.sort()

    # csv 파일명을 통해 학부과-전공명을 추출
    for file in enumerate(csv_files):
        # 확장자 제거 및 "_"로 split
        file_split = file[1].split(".")[0].split("_")
        if file_split[0] == "학과":
            department_name = file_split[1] + "-" + file_split[2]

            department_name_to_id[department_name] = file[0]
            department_id_to_name.append(department_name)
        elif file_split[0] == "기타":
            department_name = "기타-" + file_split[1]

            department_name_to_id[department_name] = file[0]
            department_id_to_name.append(department_name)

    return department_name_to_id, department_id_to_name


# 읽어온 csv 파일(raw data)을 DataFrame의 list로 반환하는 함수
# input: csv 파일(raw data)의 경로
# output: DataFrame list
def import_csv(csv_path):
    csv_files = os.listdir(csv_path)
    csv_files.sort()

    df_list = []
    for file in csv_files:
        file_path = os.path.join(csv_path, file)
        df = pd.read_csv(file_path)
        df_list.append(df)

    return df_list
