# 과 별로 이루어진 강의 시간표를 메인 로직에서 사용하기 편하게 가공하는 모듈

import import_csv

# import_csv 모듈 테스트 코드
RAW_PATH = "resource/raw"

department_name_to_id, id_to_department_name = import_csv.get_department_dict(RAW_PATH)
imported_data = import_csv.import_csv(RAW_PATH)

print(imported_data[department_name_to_id["컴퓨터공학과-컴퓨터공학"]])