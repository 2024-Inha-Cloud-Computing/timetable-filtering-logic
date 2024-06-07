# timetable-filtering-logic
시간표 만들기 & 필터링 알고리즘

## Logic

### 1. Filtering
열심히 만드는 중...

### 2. Making
열심히 만드는 중...

### 3. Processing
#### ✅ import_csv
- 모듈 설명
  - 학과 강의 및 커리큘럼 csv 파일 생성 모듈

<details>
  <summary>함수 구성</summary>

  ##### import_routine
  - csv 파일을 읽어와서 인덱스와 DataFrame list로 반환하는 함수
  - **input** csv 파일(raw data)의 경로
  - **output** 학과별 id <-> 학과명 dict, DataFrame list
  
  ##### get_department_dict
  - 현재 저장된 csv 파일명에 따라 [학부과-전공명 <-> id] 간의 변환이 가능한 dict, list를 만드는 함수
  - **input** csv 파일명 list
  - **output** 학부과-전공명 -> id dict, id -> 학부과-전공명 list

  ##### import_csv
  - 읽어온 csv 파일(raw data)을 DataFrame의 list로 반환하는 함수
  - **input** csv 파일(raw data)의 경로, csv 파일명 list
  - **output** DataFrame list

  ##### sort_csv_file
  - csv 파일 이름 정렬 key 함수
  - **input** csv 파일명
  - **output** 정렬 기준

</details>

#### ✅ entire_course
- 모듈 설명
  - 모든 강의 csv 파일 생성 모듈

<details>
  <summary>함수 구성</summary>
  
  ##### get_entire_course_df
  - 학과 별 강의 데이터를 모두 합쳐서 하나의 DataFrame으로 만드는 함수
  - **input** 학과별 강의가 담긴 DataFrame list
  - **output** 모든 학과의 강의가 담긴 DataFrame

</details>

#### ✅ time_str_to_bit
- 모듈 설명
  - DataFrame 내부의 string 형태의 시간을 bit ndarray로 변환하는 모듈
  
<details>
  <summary>함수 구성</summary>
  
  ##### time_str_to_bit
  - string 형태의 시간을 bit ndarray로 변환하는 함수
  - **input** string 형태의 시간
  - **output** bit ndarray 형태의 시간
  - 
  ##### time_str_to_bit_df
  - DataFrame 내부의 string 형태의 시간 column 전체를 bit로 변환하는 함수
  - **input** 변환 전 DataFrame, column 이름
  - **output** 변환 후 DataFrame
  
</details>

#### ✅ course_by_time
- 모듈 설명
  - 특정 시간 강의들의 DataFrame을 반환하는 모듈

<details>
  <summary>함수 구성</summary>
  
  ##### course_by_time
  - 시간을 입력받으면 해당 시간과 겹치는 강의 목록을 반환하는 함수
  - **input** 강의가 담긴 DataFrame, ndarray 형태의 시간
  - **output** 입력된 시간의 강의가 담긴 DataFrame

  ##### get_course_by_all_time
  - 각각의 시간 단위와 겹치는 강의들의 DataFrame list를 반환하는 함수
  - **input** 강의가 담긴 DataFrame
  - **output** 최소 시간 단위에 있는 강의들의 DataFrame list

</details>

#### ✅ course_by_department
- 모듈 설명
  - 각 학과가 들어야하는 강의를 교양, 전공으로 분류한 csv 파일 생성 모듈

<details>
  <summary>함수 구성</summary>
  
  ##### create_empty_department_possible_df
  - 커리큘럼에 있는 학과를 토대로 DataFrame을 생성
  - **input** department_id_to_name_for_curriculum, department_name_to_id_for_curriculum
  - **output** 커리큘럼에 있는 학과를 토대로 2개씩 생성된 빈 DataFrame 2차원 list (전공, 교양필수)

  ##### add_include_course_to_department_possible_df
  - 학과 이름이 df_course_list에 있으면, 해당 강의를 전공과 교양필수로 나누어 DataFrame에 추가
  - **input** df_course_list, entire_course_bit_df department_possible_df_list, department_id_to_name_for_curriculum, department_name_to_id_for_course
  - **output** 학과별로 강의가 추가된 DataFrame 2차원 list (전공, 교양필수)

  ##### add_geb_to_department_possible_df
  - 학과별 대학교교양필수(GEB) 과목을 교양필수 DataFrame에 추가
  - **input** entire_course_df, df_curriculum_list, department_possible_df_list, department_id_to_name_for_curriculum
  - **output** 학과별로 강의가 추가된 DataFrame 2차원 list (전공, 교양필수)

  ##### add_ged_to_department_possible_df
  - 학과별 핵심교양(GED) 과목을 교양필수 DataFrame에 추가
  - **input** entire_course_df, df_curriculum_list, department_possible_df_list, department_id_to_name_for_curriculum
  - **output** 학과별로 강의가 추가된 DataFrame 2차원 list (전공, 교양필수)

</detalis>