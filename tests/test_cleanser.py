import numpy as np
import pandas as pd
import pytest

from data_analyser.cleanser import Cleaner


def make_dataframe():
    return pd.DataFrame(
        {
            "name": ["Alice", None, "Bob", "Carol"],
            "age": [30.0, 25.0, np.nan, 40.0],
            "score": [1, 2, 3, 4],
        }
    )


class TestFindMissingData:
    def test_returns_columns_with_missing_values(self):
        cleaner = Cleaner(make_dataframe())
        columns = cleaner.find_missing_data()
        assert set(columns) == {"name", "age"}

    def test_returns_none_when_no_missing_values(self):
        data = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
        cleaner = Cleaner(data)
        assert cleaner.find_missing_data() is None

    def test_does_not_mutate_original_data(self):
        data = make_dataframe()
        cleaner = Cleaner(data)
        cleaner.find_missing_data()
        assert data["name"].isna().sum() == 1


class TestReplaceMissingData:
    def test_fills_string_column_with_undefined_default(self):
        data = make_dataframe()
        cleaner = Cleaner(data)
        columns = cleaner.find_missing_data()
        result = cleaner.replace_missing_data(columns)

        assert result["name"].isna().sum() == 0
        assert result.loc[1, "name"] == "undefined"

    def test_fills_numeric_column_with_zero_default(self):
        data = make_dataframe()
        cleaner = Cleaner(data)
        columns = cleaner.find_missing_data()
        result = cleaner.replace_missing_data(columns)

        assert result["age"].isna().sum() == 0
        assert result.loc[2, "age"] == 0

    def test_leaves_columns_without_missing_values_untouched(self):
        data = make_dataframe()
        cleaner = Cleaner(data)
        columns = cleaner.find_missing_data()
        result = cleaner.replace_missing_data(columns)

        assert list(result["score"]) == [1, 2, 3, 4]

    def test_does_not_mutate_the_original_dataframe(self):
        data = make_dataframe()
        cleaner = Cleaner(data)
        columns = cleaner.find_missing_data()
        cleaner.replace_missing_data(columns)

        # original reference passed into the constructor stays untouched
        assert data["name"].isna().sum() == 1
        assert data["age"].isna().sum() == 1


class TestSummary:
    def test_reports_before_and_after_missing_counts_per_column(self):
        data = make_dataframe()
        cleaner = Cleaner(data)
        columns = cleaner.find_missing_data()
        cleaner.replace_missing_data(columns)

        summary = cleaner.summary
        name_row = summary[summary["columns"] == "name"].iloc[0]
        assert name_row["missing_entries"] == 1
        assert name_row["after"] == 0
        assert name_row["replacing_strategy"] == "undefined"

    def test_reports_dash_strategy_for_untouched_columns(self):
        data = make_dataframe()
        cleaner = Cleaner(data)
        columns = cleaner.find_missing_data()
        cleaner.replace_missing_data(columns)

        summary = cleaner.summary
        score_row = summary[summary["columns"] == "score"].iloc[0]
        assert score_row["replacing_strategy"] == "-"

    def test_summary_before_replace_shows_no_strategy_applied(self):
        data = make_dataframe()
        cleaner = Cleaner(data)
        cleaner.find_missing_data()

        summary = cleaner.summary
        assert (summary["replacing_strategy"] == "-").all()
