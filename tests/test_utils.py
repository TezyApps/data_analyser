from data_analyser.utils import print_header, print_footer


def test_print_header_wraps_title_with_separator_of_same_char(capsys):
    print_header("Title", sep="=")
    out = capsys.readouterr().out

    lines = out.strip("\n").split("\n")
    assert lines[1] == "Title"
    assert lines[0] == lines[2]
    assert set(lines[0]) == {"="}


def test_print_header_clamps_short_titles_to_min_length(capsys):
    # separator length must never be shorter than the min_len default (30)
    print_header("Hi")
    lines = capsys.readouterr().out.strip("\n").split("\n")
    assert len(lines[0]) >= 30


def test_print_header_clamps_long_titles_to_max_length(capsys):
    print_header("x" * 200)
    lines = capsys.readouterr().out.strip("\n").split("\n")
    assert len(lines[0]) <= 60


def test_print_footer_without_text_only_prints_separator(capsys):
    print_footer(sep="-", length=10)
    out = capsys.readouterr().out
    assert out.strip("\n") == "-" * 30  # clamped to min_len default (30)


def test_print_footer_with_text_prints_text_then_separator(capsys):
    print_footer("done", sep="-", length=10)
    out = capsys.readouterr().out
    lines = out.strip("\n").split("\n")
    assert lines[0] == "done"
    assert set(lines[1]) == {"-"}


def test_print_footer_ignores_blank_text(capsys):
    print_footer("   ", sep="-", length=10)
    out = capsys.readouterr().out
    lines = out.strip("\n").split("\n")
    assert len(lines) == 1
