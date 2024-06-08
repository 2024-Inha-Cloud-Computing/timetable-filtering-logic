# DataFrame 내부의 string 형태의 시간을 bit ndarray로 변환하는 모듈

import numpy as np


# string 형태의 시간을 bit ndarray로 변환하는 함수
# input: string 형태의 시간
# output: bit ndarray 형태의 시간
def convert_time(time_str):
    # 요일을 int로 변환하기 위한 dict
    day_to_int = {"월": 0, "화": 1, "수": 2, "목": 3, "금": 4, "토": 5, "셀": 6}

    time_bit_ndarray = np.zeros(shape=len(day_to_int), dtype=np.uint32)

    # 예시 시간:
    # 화9
    # 셀0(웹강의)
    # 월16,17,18,수16,17,18(하-222)
    # 화9,10,11,12(하-120) /수13,14,15,16(하-322)

    # "/"로 split
    split_by_slash = time_str.split("/")

    for split_by_slash_element in split_by_slash:
        # ","로 split
        split_by_comma = split_by_slash_element.split(",")

        # 맨 뒤 원소의 괄호 삭제
        split_by_comma[-1] = split_by_comma[-1].split("(")[0]

        # 요일과 시간으로 split
        # 예시: 화9, 10, 11, 수9, 10, 11 -> [("화", [9, 10, 11]), ("수", [9, 10, 11])]
        split_by_day = []
        current_day, current_time = "", []
        for element in split_by_comma:
            if not element.isdigit():
                if current_day:
                    split_by_day.append((current_day, current_time))
                current_day = element[0]
                current_time.append(element[1:])
            else:
                current_time.append(element)
        split_by_day.append((current_day, current_time))

        # 요일과 시간을 bit로 변환
        for day, times in split_by_day:
            # 시간 list와 요일을 int로 변환
            day = day_to_int[day]
            times = list(map(lambda x: int(x), times))

            # 시간을 bit로 추가
            for time in times:
                time_bit_ndarray[day] |= 1 << time

    return time_bit_ndarray


# DataFrame 내부의 string 형태의 시간 column으로 강의실 dict를 만드는 함수
# input: string 형태의 시간
# output: 강의실 dict
def convert_classroom_dict(time_str):
    time_dict = {}

    # "/"로 split
    split_by_slash = time_str.split("/")

    for split_by_slash_element in split_by_slash:
        cur_day = []

        for split_by_slash_element_char in split_by_slash_element:
            if split_by_slash_element_char == "(":
                for cur_day_i in cur_day:
                    time_dict[cur_day_i] = split_by_slash_element.split("(")[1].split(
                        ")"
                    )[0]
            elif (
                not split_by_slash_element_char.isdigit()
                and split_by_slash_element_char != ","
            ):
                cur_day.append(split_by_slash_element_char)

    return time_dict


# DataFrame 내부의 string 형태의 시간 column 전체를 bit로 변환하는 함수
# input: 변환 전 DataFrame, column 이름
# output: 변환 후 DataFrame
def convert_time_classroom_df(df, time_classroom):
    df_copy = df.copy()
    df_copy["classroom"] = df_copy[time_classroom].apply(convert_classroom_dict)
    df_copy[time_classroom] = df_copy[time_classroom].apply(convert_time)

    return df_copy
