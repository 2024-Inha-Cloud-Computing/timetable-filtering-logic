# 학과 강의 및 커리큘럼 csv 파일 생성 모듈


import os
import unicodedata
import pandas as pd


# 현재 저장된 csv 파일명에 따라 [학부과-전공명 <-> id] 간의 변환이 가능한 dict, list를 만드는 함수
# input: csv 파일(raw data)의 경로
# output: 학부과-전공명 -> id dict, id -> 학부과-전공명 list
def get_department_dict(csv_path):
    # csv 파일의 파일명을 읽어옴
    csv_files = os.listdir(csv_path)

    # 파일명을 NFC로 normalize
    csv_files = [unicodedata.normalize("NFC", x) for x in csv_files]

    # "학과"로 시작하는 파일명을 "기타"로 시작하는 파일명보다 앞서게 정렬
    csv_files.sort(key=sort_csv_file)

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


# 읽어온 csv 파일(raw data)을 DataFrame의 list로 반환하는 함수
# input: csv 파일(raw data)의 경로
# output: DataFrame list
def import_csv(csv_path):
    # csv 파일의 파일명을 읽어옴
    csv_files = os.listdir(csv_path)

    # 파일명을 NFC로 normalize
    csv_files = [unicodedata.normalize("NFC", x) for x in csv_files]

    # "학과"로 시작하는 파일명을 "기타"로 시작하는 파일명보다 앞서게 정렬
    csv_files.sort(key=sort_csv_file)

    df_list = []
    for file in csv_files:
        FILE_PATH = f"{csv_path}/{file}"
        df = pd.read_csv(FILE_PATH)
        df_list.append(df)

    return df_list


# csv 파일 이름 정렬 key 함수
# input: csv 파일명
# output: 정렬 기준
def sort_csv_file(file):
    file_remove_extension = file.split(".")[0]
    file_split = file_remove_extension.split("_")
    if file_split[0] == "기타":
        return (1, file)
    else:
        return (0, file)
