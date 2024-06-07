# 학과 강의 및 커리큘럼 csv 파일 생성 모듈

import os
import unicodedata
import pandas as pd


# csv 파일로부터 변환에 필요한 list & dict와 DataFrame list로 반환하는 함수
# input: csv 파일(raw data)의 경로
# output: 학과별 [id <-> 학과명] list & dict, DataFrame list
def import_routine(csv_path):
    # csv 파일명 추출
    csv_files = os.listdir(csv_path)

    # 파일명을 같은 유니코드 인코딩(자소통합)으로 normalize
    csv_files = [unicodedata.normalize("NFC", x) for x in csv_files]

    # "학과"로 시작하는 파일명을 "기타"로 시작하는 파일명보다 앞서게 정렬
    csv_files.sort(key=sort_csv_file)

    return *get_department_dict(csv_files), import_csv(csv_path, csv_files)


# csv 파일명에 따라 [id <-> 학과명] 간의 변환에 필요한 dict, list를 만드는 함수
# input: csv 파일명 list
# output: [id <-> 학과명] 간의 변환에 필요한 dict, list
def get_department_dict(csv_files):
    department_name_to_id = {}
    department_id_to_name = []

    # csv 파일명을 통해 학부과-전공명을 추출
    for file in enumerate(csv_files):
        # 확장자 제거 및 "_"로 split
        file_remove_extension = file[1].split(".")[0]
        file_split = file_remove_extension.split("_")
        if file_split[0] == "기타":
            DEPARTMENT_NAME = "기타-" + file_split[1]

            department_name_to_id[DEPARTMENT_NAME] = file[0]
            department_id_to_name.append(DEPARTMENT_NAME)
        else:
            DEPARTMENT_NAME = file_split[1] + "-" + file_split[2]

            department_name_to_id[DEPARTMENT_NAME] = file[0]
            department_id_to_name.append(DEPARTMENT_NAME)

    return department_name_to_id, department_id_to_name


# 읽어온 csv 파일(raw data)을 DataFrame의 list로 변환하는 함수
# input: csv 파일(raw data)의 경로, csv 파일명 list
# output: DataFrame list
def import_csv(csv_path, csv_files):
    df_list = []
    for file in csv_files:
        FILE_PATH = f"{csv_path}/{file}"
        df = pd.read_csv(FILE_PATH)
        df_list.append(df)

    return df_list


# csv 파일 이름 정렬 key 함수
# input: csv 파일명
# output: 정렬 기준에 따른 우선순위 튜플
def sort_csv_file(file):
    file_remove_extension = file.split(".")[0]
    file_split = file_remove_extension.split("_")
    if file_split[0] == "기타":
        return (1, file)
    else:
        return (0, file)
