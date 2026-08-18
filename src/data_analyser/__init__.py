from . import file_reader as fr

def main() -> None:
    print("Hello from data-analyser!")
    file_reader = fr.FileReader()
    csv_data = file_reader.get_data()
    print(csv_data.describe())