
import pandas as pd

from ..utils import print_header as ph, print_footer as pf

class Cleanser():

    def __init__(self, data: pd.DataFrame) -> None:
        self.__data = data

    def clean(self) -> pd.DataFrame:
        return self.__find_and_replace_nulls()

    #region - Private Methods

    def __find_and_replace_nulls(self) -> pd.DataFrame:
        ph("Finding null records… across columns")
        data = self.__data

        null_columns = data.columns[data.isna().sum() > 0]
        print(f" # of null columns: {len(null_columns)}")

        print("\n Preparing for clean up… \n")

        for col in null_columns:
            ph(f" Column: {col}")
            if pd.api.types.is_string_dtype(data[col]):
                current_unique_values = data[col].unique()
                print(f"\n {data[col].isna().sum()} null entries | Current Unique Values: { ", ".join(map(str, current_unique_values))}")
                fill_na_value = input(f"\n Enter a default value for {col}, if skipped will marked as 'undefined'\t=> ")
                if str(fill_na_value).strip(' ') != "":
                    data[col] = data[col].fillna(str(fill_na_value))
                else:
                    data[col] = data[col].fillna("undefined")
            elif pd.api.types.is_numeric_dtype(data[col]):
                print(f"\n {data[col].isna().sum()} null entries | Values Range : Range({data[col].min()}, {data[col].max()})")
                print(f"\n How would you like to handle missing data for {col}:")
                print("\t1. mean")
                print("\t2. median")
                print("\t3. Enter a custom number")
                option = input(f"\n Enter your option => ").strip('.,').lower()
                if option == "1" or option == "mean":
                    data[col] = data[col].fillna(data[col].mean())
                elif option == "2" or option == "median":
                    data[col] = data[col].fillna(data[col].median())
                elif option == "3" or option in "custom":
                    fill_na_value = input(f" Enter a default value for {col}, if unrecognized will marked as '-1'\t=> ")
                    try:
                        num_value = pd.to_numeric(fill_na_value)
                    except Exception as e:
                        print(f"Unrecognized {fill_na_value}. Defaulting to -1")
                        num_value = -1
                    data[col] = data[col].fillna(num_value)
                else:
                    print(f"Unrecognized option : {option} for {col}: Defaulting to -1")
                    data[col] = data[col].fillna(-1)

                pf()

        print(f" Data cleanup is complete!")
        null_entries = data.columns[data.isna().sum() > 0]
        print(f" Null Entries after cleanup : {len(null_entries)}")
        pf()
        return data

    #endregion