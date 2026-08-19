import sys
import pandas as pd
from . import file_reader as fr, cleanser as cl
from .utils import print_header as ph, print_footer as pf

def __next_steps() -> int:
    print("\n")
    ph(" Options")
    print(" 1. Show first 5 rows")
    print(" 2. Show Columns' data types")
    print(" 3. Data info")
    print(" 4. Summary of the data")
    print(" 5. Exit")
    pf()
    
    option = input("Enter an option : 1 to 4\t=> ")
    return int(option)

def __execute_options(data: pd.DataFrame):

    __option = 0
    while __option < 5:
        __option = __next_steps()

        if __option == 1:
            ph("Displaying first 5 rows…")
            print(data.head())
            pf()
        elif __option == 2:
            ph("Displaying column data types…")
            print(data.columns)
            pf()
        elif __option == 3:
            ph("Displaying data info…")
            print(data.info())
            pf()
        elif __option == 4:
            ph("Summary of the data")
            print(data.describe())
            pf()
    else:
        ph("Thank you for using the tool…")
        print("Exiting the program… Bye!")
        pf()
        sys.exit(1)



def main() -> None:
    ph("Data Cleanser & Analyser:")

    print("Reading the input file…")
    file_reader = fr.FileReader()

    print("\nData is ready for analysis…")
    csv_data = file_reader.get_data()

    # __execute_options(csv_data)

    clo = cl.Cleanser(csv_data)
    cleansed_data = clo.clean()

    ph('NEW - Data')
    print(cleansed_data)
    
    # Next steps:

    # 1. Describe the data ✅
    #   ✅ a. columns -> data types, nulls count, sum of unique values, 
    #   ✅ b. Action Required -> for handling missing data
    
    # [MVP - 2] 2. Get a config file for data cleaning:
    #   a. If None, then go with default mapping based on dtypes
    #   b. If provided, then use the config for respective columns.

    # 3. Describe the data (after cleaning > follow step 1) ✅
    #   ✅ a. columns -> data types, sum of unique values, 
    #   ✅ b. Action Required -> for handling missing data
    #   ✅ c. what's changed and it's columns

    # 4. Visualization?