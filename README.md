# timetable-filtering-logic
시간표 만들기 &amp; 필터링 알고리즘

## Logic

### 1. Filtering
열심히 만드는 중...

### 2. Making
열심히 만드는 중...

### 3. Processing
#### import_csv
- 모듈 설명
  - 각 학과 별 csv 파일 생성 모듈

<details>
  <summary>함수 구성</summary>
  
  ##### get_department_dict

  - 현재 저장된 csv 파일명에 따라 [학부과-전공명 <-> id] 간의 변환이 가능한 dict, list를 만드는 함수
  - **input** csv 파일(raw data)의 경로
  - **output** 학부과-전공명 -> id dict, id -> 학부과-전공명 list

  ##### import_csv
  - 읽어온 csv 파일(raw data)을 DataFrame의 list로 반환하는 함수
  - **input** csv 파일(raw data)의 경로
  - **output** DataFrame list

</details>

#### entire_course
- 모듈 설명
  - 모든 강의 csv 파일 생성 모듈

<details>
  <summary>함수 구성</summary>
  
  ##### get_entire_course_df
  - 학과 별 강의 데이터를 모두 합쳐서 하나의 DataFrame으로 만드는 함수
  - **input** DataFrame list
  - **output** DataFrame

</details>

#### time_str_to_bit
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

#### get_course_by_time
- 모듈 설명
  - 특정 시간 강의들의 DataFrame을 반환하는 모듈

<details>
  <summary>함수 구성</summary>
  
  ##### course_by_time
  - 시간을 입력받으면 해당 시간과 겹치는 강의 목록을 반환하는 함수
  - **input** DataFrame, bit ndarray로 변환된 시간
  - **output** DataFrame

  ##### get_course_by_all_time
  - 각각의 시간 단위와 겹치는 강의들의 DataFrame list를 반환하는 함수
  - **input** DataFrame
  - **output** DataFrame list

</details>