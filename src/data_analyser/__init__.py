from . import file_reader as fr

def main() -> None:
    print("Hello from data-analyser!")
    file_reader = fr.FileReader()
    file_reader.get_file_path()