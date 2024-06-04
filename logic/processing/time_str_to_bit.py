# DataFrame 내부의 string 형태의 시간을 bit로 변환하는 모듈


# string 형태의 시간을 bit로 변환하는 함수
# input: string 형태의 시간
# output: bit로 변환된 시간
def time_str_to_bit(time_str):
    # 요일을 int로 변환하기 위한 dict
    day_to_int = {"월": 0, "화": 1, "수": 2, "목": 3, "금": 4, "토": 5, "셀": 6}

    bit_time = [0] * 7

    # 예시 시간: "화9,10,11,12(하-120) /수13,14,15,16(하-322)"
    # 예시 시간: "월16,17,18,수16,17,18(하-222)"
    # 예시 시간: "셀0(웹강의)"
    # 예시 시간: "화9"

    # "/"로 split
    split_by_slash = time_str.split("/")

    for split_by_slash_element in split_by_slash:
        # ","로 split
        split_by_comma = split_by_slash_element.split(",")

        # 맨 뒤 원소의 괄호 삭제
        split_by_comma[-1] = split_by_comma[-1].split("(")[0]

        # 요일이 들어있는 원소를 기준으로 분리
        separate_index = []
        for index, split_by_comma_element in enumerate(split_by_comma):
            if not split_by_comma_element.isdigit():
                separate_index.append(index)
        split_by_day, day = [], []
        for separate_index_element in separate_index[::-1]:
            day.append(split_by_comma[separate_index_element][0])
            split_by_comma[separate_index_element] = split_by_comma[
                separate_index_element
            ][1:]
            split_by_day.append(split_by_comma[separate_index_element:])
            split_by_comma = split_by_comma[:separate_index_element]

        # 요일과 시간을 bit로 변환
        for split_by_day_element, day_element in zip(split_by_day, day):
            # 요일을 int로 변환
            day_element = day_to_int[day_element]

            # 시간 list를 int로 변환
            split_by_day_element = list(map(lambda x: int(x), split_by_day_element))

            # 시간을 bit로 추가
            for time in split_by_day_element:
                bit_time[day_element] |= 1 << time

    return bit_time


# DataFrame 내부의 string 형태의 시간 column 전체를 bit로 변환하는 함수
# input: 변환 전 DataFrame, column 이름
# output: 변환 후 DataFrame
def time_str_to_bit_df(df, column_name):
    df[column_name] = df[column_name].apply(time_str_to_bit)

    return df


# 테스트 코드
# import import_csv
# import entire_course

# RAW_PATH = "resource/raw"

# imported_data = import_csv.import_csv(RAW_PATH)
# merged_data = entire_course.merge_all_data(imported_data)
# merged_data_time_bit = time_str_to_bit.time_str_to_bit_df(merged_data, "time_classroom")

# print(merged_data_time_bit)
