
def __clamped(len: int, min_len: int = 20, max_len: int = 40) -> int:
    return max(min_len, min(len, max_len))

def print_header(title: str, sep: str = "="):
    separator = sep * __clamped(len(title))
    header = "\n".join([separator, title, separator])
    print(f"\n{header}")

def print_footer(text: str | None = None, sep: str = '-', length: int = 30):
    footer_list = []
    if text is not None and text.strip(' ') != "":
        footer_list.append(text)

    separator = sep * __clamped(length)
    footer_list.append(separator)
    footer = "\n".join(footer_list)
    print(f"{footer}\n")