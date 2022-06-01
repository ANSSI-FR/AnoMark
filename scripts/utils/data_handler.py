import re
import random
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


def replace_sid_in_str(some_string, placeholder="<SID>"):
    regex = r"S[-–]1[-–]([0-9]+[-–])+[0-9]+"
    return re.sub(regex, placeholder, some_string, 0, re.MULTILINE & re.IGNORECASE)


def replace_guid_in_str(some_string, placeholder="<GUID>"):
    regex = r"\{?[0-9A-Fa-f]{8}[-–]([0-9A-Fa-f]{4}[-–]){3}[0-9A-Fa-f]{12}\}?"
    return re.sub(regex, placeholder, some_string, 0, re.MULTILINE & re.IGNORECASE)


def replace_user_in_str(some_string, placeholder="<USER>"):
    regex = r'C:\\Users\\[^\\]*\\'
    return re.sub(regex, r"C:\\Users\\{}\\".format(placeholder), some_string, re.MULTILINE & re.IGNORECASE)


def apply_modules_to_str(text):
    """
    Apply all modules to df column.
    :param text: String to apply modules
    :return: dataframe with placeholders
    """
    return replace_user_in_str(replace_sid_in_str(replace_guid_in_str(text)))


def apply_modules_to_pd_series(pd_series):
    """
    Apply all modules to pd Series.
    :param pd_series: pandas Series
    :return: Series with placeholders
    """
    pd_series = pd_series.apply(lambda x: apply_modules_to_str(x))
    return pd_series


def apply_modules_to_df(df, column):
    """
    Apply all modules to df column.
    :param df: pandas DataFrame
    :param column: column to apply the operation on
    :return: dataframe with placeholders
    """
    df[column] = apply_modules_to_pd_series(df[column])
    return df


def process_dataframe(data: pd.DataFrame, column: str, n_lines, percentage, from_end: bool,
                      randomize: bool, apply_placeholder: bool):
    data[column] = data[column].astype(str)
    if n_lines:
        n_lines = int(n_lines)
        if n_lines > len(data):
            raise ValueError("n_lines must be inferior to dataset length")

        if randomize:
            data = data[random.choices(range(len(data)), k=n_lines)]
        else:
            if from_end:
                data = data.iloc[n_lines:]
            else:
                data = data.iloc[:n_lines]
    elif percentage:
        percentage = float(percentage)
        if from_end:
            data = data.iloc[int(len(data) * float(percentage) / 100):]
        else:
            data = data.iloc[:int(len(data) * float(percentage) / 100)]

    if apply_placeholder:
        print("Applying placeholder transformation...")
        data = apply_modules_to_df(data, column)

    return data
