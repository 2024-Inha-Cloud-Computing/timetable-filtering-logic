def find_professor(course_df):
    professor_dict = {}
    for _, course_series in course_df.iterrows():
        if course_series["course_name"] in professor_dict:
            professor_dict[course_series["course_name"]].add(course_series["professor"])
        else:
            professor_dict[course_series["course_name"]] = {course_series["professor"]}

    return professor_dict
