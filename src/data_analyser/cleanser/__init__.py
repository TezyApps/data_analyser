
import pandas as pd

class Cleaner():

    def __init__(self, data: pd.DataFrame) -> None:
        self.__data = data.copy()
        self.__original_data = data
        self.__changes = dict()

    #region - Public APIs

    @property
    def summary(self) -> pd.DataFrame:
        original, modified = self.__original_data, self.__data
        before = original.isna().sum()
        after = modified.isna().sum()
        result = pd.concat(
            [before, after],
            axis=1,
            keys=["missing_entries", "after"]
        ).reset_index()
        result.columns = ["columns", "missing_entries", "after"]
        result["replacing_strategy"] = result['columns'].map(self.__changes).fillna("-")
        return result

    def find_missing_data(self) -> pd.Index | None:
        """
        Returns a list of columns with missing values or data quality
        """
        return self.__columns_containing_missing_values(self.__data)

    def replace_missing_data(self, columns: pd.Index) -> pd.DataFrame:
        changes = self.__handle_missing_columns(columns)
        self.__changes = changes if changes is not None else dict()
        return self.__data

    #endregion

    #region - Private Methods

    def __columns_containing_missing_values(self, data: pd.DataFrame) -> pd.Index | None:
        __null_columns = data.columns[data.isna().sum() > 0]
        return __null_columns if len(__null_columns) > 0 else None

    def __handle_missing_columns(self, columns: pd.Index) -> dict | None:
        changes = {}
        for column in columns:
            filled_value = self.__fill_missing_values(column)
            changes[column] = filled_value
        return changes

    def __fill_missing_values(self, column: str, user_defined_value: str | int | float | None = None) -> str | int | float | None:
        data = self.__data

        if pd.api.types.is_string_dtype(data[column]):
            fill_value = "undefined" 
            if isinstance(user_defined_value, str):
                fill_value = user_defined_value.strip('., ')
        elif pd.api.types.is_numeric_dtype(data[column]):
            fill_value = 0
            if isinstance(user_defined_value, int) or isinstance(user_defined_value, float):
                fill_value = user_defined_value

        data[column] = data[column].fillna(fill_value)
        return fill_value

    #endregion