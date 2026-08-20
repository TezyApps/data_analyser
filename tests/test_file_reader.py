import sys

import pandas as pd
import pytest

from data_analyser.file_reader import FileReader


def test_get_data_reads_csv_path_from_argv(tmp_path, monkeypatch):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("a,b\n1,x\n2,y\n")

    monkeypatch.setattr(sys, "argv", ["dca", str(csv_path)])

    reader = FileReader()
    data = reader.get_data()

    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == ["a", "b"]
    assert len(data) == 2


def test_get_data_strips_trailing_newline_from_path(tmp_path, monkeypatch):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("a,b\n1,x\n")

    monkeypatch.setattr(sys, "argv", ["dca", f"{csv_path}\n"])

    reader = FileReader()
    data = reader.get_data()

    assert len(data) == 1


def test_get_data_exits_when_no_path_is_provided(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["dca"])

    reader = FileReader()
    with pytest.raises(SystemExit):
        reader.get_data()


def test_get_data_raises_for_missing_file(tmp_path, monkeypatch):
    missing_path = tmp_path / "does-not-exist.csv"
    monkeypatch.setattr(sys, "argv", ["dca", str(missing_path)])

    reader = FileReader()
    with pytest.raises(FileNotFoundError):
        reader.get_data()
