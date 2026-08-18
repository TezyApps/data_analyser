
import sys

class FileReader():
    """
    FileReader class is responsible for the below:
        1. Takes a file path from user as an input
        2. validates the file path, and accepts only .csv format.
        3. Returns a panda DataFrame object.
    """

    def __init__(self):
        self.__file_path = None

    def get_file_path(self):
        if len(sys.argv) < 2:
            print(f"""
            Please input a file name.
                Usage: dca /root/path/my_file.csv
                Note:
                    - Only a single .csv file is supported at the moment as input.
            """)
            sys.exit(1)

        file_path = sys.argv[1]
        self.__file_path = file_path
        print(f"Loaded the file successfully : {self.__file_path}")