from constant_variable import *

import pandas as pd


def import_processed_data(self):
    for data_type in ["course", "curriculum"]:
        department_name_to_id = pd.read_csv(
            f"{PROCESSED_DEPARTMENT_INDEX_PATH}/department_name_to_id_for_{data_type}.csv",
            index_col=0,
        ).to_dict()["id"]
        department_id_to_name = [
            element[0]
            for element in pd.read_csv(
                f"{PROCESSED_DEPARTMENT_INDEX_PATH}/department_id_to_name_for_{data_type}.csv",
                index_col=0,
            ).values.tolist()
        ]
        df_list = [
            pd.read_csv(f"{PROCESSED_IMPORT_PATH}/{data_type}/{department_name}.csv")
            for department_name in department_id_to_name
        ]

        if data_type == "course":
            department_name_to_id_for_course = department_name_to_id
            department_id_to_name_for_course = department_id_to_name
            df_course_list = df_list
        elif data_type == "curriculum":
            department_name_to_id_for_curriculum = department_name_to_id
            department_id_to_name_for_curriculum = department_id_to_name
            df_curriculum_list = df_list

    entire_course_df = pd.read_csv(f"{PROCESSED_ENTIRE_COURSE_PATH}/entire_course.csv")

    entire_course_bit_df = pd.read_csv(
        f"{PROCESSED_TIME_STR_TO_BIT_PATH}/entire_course_bit.csv"
    )
    elective_course_bit_df = pd.read_csv(
        f"{PROCESSED_ENTIRE_COURSE_PATH}/elective_course.csv"
    )

    course_by_all_time = [
        [
            pd.read_csv(f"{PROCESSED_COURSE_BY_TIME_PATH}/{day}_{time}.csv")
            for time in range(TIME_NUM)
        ]
        for day in range(DAY_NUM)
    ]

    department_possible_df_list = [
        [
            pd.read_csv(
                f"{PROCESSED_COURSE_BY_DEPARTMENT_PATH}/{department_name}_major.csv"
            ),
            pd.read_csv(
                f"{PROCESSED_COURSE_BY_DEPARTMENT_PATH}/{department_name}_liberal_required.csv"
            ),
        ]
        for department_name in department_id_to_name_for_curriculum
    ]

    return (
        department_name_to_id_for_course,
        department_id_to_name_for_course,
        department_name_to_id_for_curriculum,
        department_id_to_name_for_curriculum,
        df_course_list,
        df_curriculum_list,
        entire_course_df,
        entire_course_bit_df,
        elective_course_bit_df,
        course_by_all_time,
        department_possible_df_list,
    )
