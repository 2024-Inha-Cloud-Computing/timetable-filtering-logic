# 파일 저장 경로
RESOURCE_PATH = "resource"
PROCESSED_PATH = f"{RESOURCE_PATH}/processed"
PROCESSED_DEPARTMENT_INDEX_PATH = f"{PROCESSED_PATH}/department_index"
PROCESSED_IMPORT_PATH = f"{PROCESSED_PATH}/import_csv"
PROCESSED_ENTIRE_COURSE_PATH = f"{PROCESSED_PATH}/entire_course"
PROCESSED_TIME_STR_TO_BIT_PATH = f"{PROCESSED_PATH}/time_str_to_bit"
PROCESSED_COURSE_BY_TIME_PATH = f"{PROCESSED_PATH}/course_by_time"
PROCESSED_COURSE_BY_DEPARTMENT_PATH = f"{PROCESSED_PATH}/course_by_department"

# 요일, 교시
DAY_NUM = 7
TIME_NUM = 31

# user taste
AM = 0
PM = 1
SPACE_ON = 0
SPACE_OFF = 1

# convert mode
TO_FRONT = 0
TO_BACK = 1

# opject type
TIMETABLE = 0
COURSE = 1
PROFESSOR = 2

# auto_fill mode
MAJOR_MODE = 0
LIBERAL_REQUIRED_MODE = 1
ELECTIVE_MODE = 2
