# timetable-filtering-logic
시간표 만들기 & 필터링 알고리즘

## Logic

### 1. Filtering
#### Filtering Class
- 클래스 설명
  - 필터링 인터페이스

<details>
  <summary>클래스 구성</summary>
  
  ##### Filtering
  - private 변수
    - __department_name_to_id: dict
    - __department_id_to_name: list[str]
    - __department_course_df_list: list[DataFrame]
    - __entire_course_df: DataFrame
    - __entire_course_bit_df: DataFrame
    - __course_by_all_time: list[list[DataFrame]]
  - private 함수
    - __import_processed_data

  - public 함수
    - search_course_routine

</details>

### 2. Making
열심히 만드는 중...

### 3. Processing
#### ✅ import_csv
- 모듈 설명
  - 학과 강의 및 커리큘럼 csv 파일 생성 모듈

<details>
  <summary>함수 구성</summary>

  ##### import_routine
  - csv 파일로부터 변환에 필요한 list & dict와 DataFrame list로 반환하는 함수
  - **input** csv 파일(raw data)의 경로
  - **output** 학과별 [id <-> 학과명] list & dict, DataFrame list
  
  ##### get_department_dict
  - csv 파일명에 따라 [id <-> 학과명] 간의 변환에 필요한 dict, list를 만드는 함수
  - **input** csv 파일명 list
  - **output** [id <-> 학과명] 간의 변환에 필요한 dict, list

  ##### import_csv
  - 읽어온 csv 파일(raw data)을 DataFrame의 list로 변환하는 함수
  - **input** csv 파일(raw data)의 경로, csv 파일명 list
  - **output** DataFrame list

  ##### sort_csv_file
  - csv 파일 이름 정렬 key 함수
  - **input** csv 파일명
  - **output** 정렬 기준에 따른 우선순위 튜플

</details>

#### ✅ entire_course
- 모듈 설명
  - 전체 & 교양선택 강의 csv 파일 생성 모듈

<details>
  <summary>함수 구성</summary>
  
  ##### get_entire_course_df
  - 학과별 강의 전체를 하나의 DataFrame으로 만드는 함수
  - **input** 학과별 강의 DataFrame list
  - **output** 전체 강의 DataFrame

  ##### get_elective_course_df
  - 전체 강의 DataFrame 중 교양선택 강의를 추출하는 함수
  - **input** 전체 강의 DataFrame
  - **output** 교양선택 강의 DataFrame

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
  - 특정 시간 강의의 DataFrame을 반환하는 모듈

<details>
  <summary>함수 구성</summary>
  
  ##### course_by_time
  - 시간을 입력받으면 해당 시간에 열리는 강의 DataFrame을 반환하는 함수
  - **input** 강의 DataFrame, bit ndarray 형태의 시간
  - **output** 입력된 시간에 열리는 강의 DataFrame

  ##### get_course_by_all_time
  - 개별 교시에 열리는 강의들의 DataFrame list를 반환하는 함수
  - **input** 강의 DataFrame
  - **output** 개별 교시에 열리는 강의 DataFrame list

</details>

#### ✅ course_by_department
- 모듈 설명
  - 각 학과가 들어야하는 강의를 교양, 전공으로 분류한 DataFrame 생성 모듈

<details>
  <summary>함수 구성</summary>
  
  ##### create_empty_department_possible_df
  - 커리큘럼에 있는 학과를 토대로 DataFrame을 생성
  - **input** 커리큘럼에 있는 학과의 id -> 학과이름 변환 list
  - **output** 커리큘럼에 있는 학과를 토대로 2개씩 생성된 빈 DataFrame 2차원 list (전공, 교양필수)

  ##### add_include_course_to_department_possible_df
  - 학과 이름이 df_course_list에 있으면, 해당 강의를 전공과 교양필수로 나누어 DataFrame에 추가
  - **input**
    - 학과별 강의 DataFrame list
    - 전체 강의 DataFrame (시간이 bit ndarray로 변환된 DataFrame)
    - 커리큘럼에 있는 학과의 id -> 학과이름 변환 list
    - 강의시간표에 있는 학과의 학과이름 -> id 변환 dict
  - **output** 학과별로 강의가 추가된 DataFrame 2차원 list (전공, 교양필수)

  ##### add_geb_to_department_possible_df
  - 학과별 대학교교양필수(GEB) 과목을 교양필수 DataFrame에 추가
  - **input**
    - 전체 강의 DataFrame (시간이 bit ndarray로 변환된 DataFrame)
    - 학과별 커리큘럼 DataFrame list
    - 학과별 강의가 추가된 DataFrame 2차원 list (전공, 교양필수)
    - 커리큘럼에 있는 학과의 id -> 학과이름 변환 list
  - **output** 학과별로 강의가 추가된 DataFrame 2차원 list (전공, 교양필수)

  ##### add_ged_to_department_possible_df
  - 학과별 핵심교양(GED) 과목을 교양필수 DataFrame에 추가
  - **input**
    - 전체 강의 DataFrame (시간이 bit ndarray로 변환된 DataFrame)
    - 학과별 커리큘럼 DataFrame list
    - 학과별 강의가 추가된 DataFrame 2차원 list (전공, 교양필수)
    - 커리큘럼에 있는 학과의 id -> 학과이름 변환 list
  - **output** 학과별로 강의가 추가된 DataFrame 2차원 list (전공, 교양필수)

</detalis>