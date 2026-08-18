
import pandas as pd
from pandas import isna

from ..utils import print_header as ph, print_footer as pf

class Cleanser():

    def __init__(self, data: pd.DataFrame) -> None:
        self.__data = data

    def find_nulls(self):
        ph("Finding null records… across columns")
        data = self.__data
        null_columns = data.columns[data.isna().sum() > 0]
        print(f" # of null columns: {len(null_columns)}")
        for col in null_columns:
            print(f" {col} : {data[col].isna().sum()}")
            print(" Preparing for clean up… ")
            if data[col].dtype == "str":
                before = data[col].unique()
                fill_na_value = input(f" Enter a default value for {col}, if skipped will marked as 'undefined'\t=> ")
                if str(fill_na_value).strip(' ') != "":
                    data[col] = data[col].fillna(str(fill_na_value))
                after = data[col].unique()

                pf()
                df_before_after = pd.DataFrame({'Before': before, 'After': after})
                print()
                print(df_before_after)
                print()
                pf()

        print(f" Data cleanup is complete!")
        null_entries = data.columns[data.isna().sum() > 0]
        print(f" Null Entries after cleanup : {len(null_entries)}")
        pf()