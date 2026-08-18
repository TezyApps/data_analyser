
import argparse
import pandas as pd

class FileReader():
    """
    FileReader class is responsible for the below:
        1. Takes a file path from user as an input
        2. validates the file path, and accepts only .csv format.
        3. Returns a panda DataFrame object.
    """

    #region - Public Methods

    def get_data(self) -> pd.DataFrame:
        csv_data_file = self.__argparse_get_file_path()
        data_frame = pd.read_csv(csv_data_file)
        return data_frame

    #endregion

    #region - Private Methods

    def __argparse_get_file_path(self) -> str:
          parser = argparse.ArgumentParser(description = "Input a .csv file path")
          parser.add_argument("file_name", help="The path to the .csv file")
          args = parser.parse_args()
          return args.file_name.strip("\n")

    #endregion
        