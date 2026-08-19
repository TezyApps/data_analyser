import pandas as pd
from . import file_reader as fr, cleanser as cl
from .utils import print_header as ph, print_footer as pf

def main() -> None:
    ph("🕵️‍♂️ Data Quality Analyser")

    print(" 👓 Reading the input file…")
    file_reader = fr.FileReader()
    csv_data = file_reader.get_data()

    cleaner = cl.Cleaner(csv_data)

    print(f" 🔎 Checking for Data quality issues...")
    columns = cleaner.find_missing_data()
    print(" 🧹 Data Quality Analysis Complete!")

    if columns is not None:
        new_data = cleaner.replace_missing_data(columns)
        print(" 🪄 Found few missing values and replaced with defaults...\n")
        ph("🗒️ Summary of the changes")
        print(cleaner.summary)
        pf()
        ph("📊 Some Interesting facts about your data")
        print(f"\n{new_data.describe()}\n")
        pf()
    else:
        print("\n ✨ Nothing to clean. No missing values across columns.")
        pf()

    
    # ph('NEW - Data')
    # print(cleansed_data)
    # pf()
    
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