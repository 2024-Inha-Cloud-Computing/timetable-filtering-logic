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
  - csv 파일을 읽어와서 DataFrame으로 변환하는 모듈

<details>
  <summary>함수 구성</summary>
  
  ##### get_department_dict

  - 현재 저장된 csv 파일명에 따라 학부과-전공명 <-> id dict, list를 만드는 함수
  - **input** 저장된 csv 파일의 경로
  - **output** 학부과-전공명 -> id dict, id -> 학부과-전공명 list

  ##### import_csv
  - csv 파일들을 DataFrame으로 읽어와서 list로 반환하는 함수
  - **input** csv 파일의 경로
  - **output** DataFrame list

</details>

#### entire_course
- 모듈 설명
  - 모든 강좌 데이터가 들어있는 DataFrame을 만드는 모듈

<details>
  <summary>함수 구성</summary>
  
  ##### get_entire_course
  - 과 별 강의 데이터를 모두 합쳐서 하나의 DataFrame으로 만드는 함수
  - **input** DataFrame list
  - **output** DataFrame

</details>

#### time_str_to_bit
- 모듈 설명
  - DataFrame 내부의 string 형태의 시간을 bit로 변환하는 모듈
  
<details>
  <summary>함수 구성</summary>
  
  ##### time_str_to_bit
  - string 형태의 시간을 bit로 변환하는 함수
  - **input** string 형태의 시간
  - **output** bit로 변환된 시간

  ##### time_str_to_bit_df
  - DataFrame 내부의 string 형태의 시간 column 전체를 bit로 변환하는 함수
  - **input** 변환 전 DataFrame, column 이름
  - **output** 변환 후 DataFrame
  
</details>