# 검색어를 입력받으면 해당 검색어를 포함하는 강의를 찾아주는 모듈


# 검색어를 입력받으면 해당 검색어를 포함하는 강의를 찾아주는 함수
# input: 검색어, 강의 DataFrame
# output: 검색어를 포함하는 강의 DataFrame
def search_course(search_word, course_df):
    # 학수번호, 강의명, 학과명, 교수명 중에서 검색어를 포함하는 강의를 찾아줌
    search_columns = ["course_id", "course_name", "professor"]

    search_result = course_df[
        course_df[search_columns]
        .apply(lambda x: x.str.contains(search_word, case=False))
        .any(axis=1)
    ]

    return search_result
