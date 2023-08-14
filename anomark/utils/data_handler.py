import random
import re

import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


def replace_sid_in_str(some_string, placeholder="<SID>"):
    regex = r"S[-–]1[-–]([0-9]+[-–])+[0-9]+"
    return re.sub(regex, placeholder, some_string, 0, flags=re.MULTILINE | re.IGNORECASE)


def replace_guid_in_str(some_string, placeholder="<GUID>"):
    regex = r"\{?[0-9A-Fa-f]{8}[-–]([0-9A-Fa-f]{4}[-–]){3}[0-9A-Fa-f]{12}\}?"
    return re.sub(regex, placeholder, some_string, 0, flags=re.MULTILINE | re.IGNORECASE)


def replace_user_in_str(some_string, placeholder="<USER>"):
    regex = r'(C:\\Users)\\[^\\]*\\'
    return re.sub(regex, r"\g<1>\\{}\\".format(placeholder), some_string, flags=re.MULTILINE | re.IGNORECASE)


def replace_hash_in_str(some_string, placeholder="<HASH>"):
    # regex consists of SHA256, SHA1, MD5, common truncation of hash in file name
    regex = r'\b(?:[A-Fa-f0-9]{64}|[A-Fa-f0-9]{40}|[A-Fa-f0-9]{32}|[A-Fa-f0-9]{20})\b'
    return re.sub(regex, placeholder, some_string, flags=re.MULTILINE | re.IGNORECASE)


# This applies to Windows file paths
def replace_filepath_in_str(some_string, placeholder="<FILEPATH>"):
    # From https://regex101.com/r/zWGLMP/25, adapted to Python
    # We need to cover NTFS standard: https://learn.microsoft.com/en-ca/windows/win32/fileio/naming-a-file?redirectedfrom=MSDN
    regex = r"(?P<opening>\b(?P<montage>[a-zA-Z]:[\/\\])|[\/\\][\/\\](?<!http:\/\/)(?<!https:\/\/)(?:>[?.][\/\\](?:[^\/\\<>:\"|?\n\r ]+[\/\\])?(?P=montage)?|(?!(?P=montage)))|%\w+%[\/\\]?)(?:[^\/\\<>:\"|?\n\r ,'][^\/\\<>:\"|?\n\r]*(?<![ ,'])[\/\\])*(?:(?=[^\/\\<>:\"'|?\n\r;, ])(?:(?:[^\/\\<>:\"|?\n\r;, .](?: (?=[\w\-]))?(?:\*(?!= ))?(?!(?P=montage)))+)?(?:\.\w+)*)|(?:'(?P=opening)(?=.*'\W|.*'$)(?:[^\/\\<>:'\"|?\n\r]+(?:'(?=\w))?[\/\\]?)*')|\"(?P=opening)(?=.*\")(?:[^\/\\<>:\"|?\n\r]+[\/\\]?)*\""
    return re.sub(regex, r"\g<1>{}".format(placeholder), some_string, flags=re.MULTILINE | re.IGNORECASE)


def apply_modules_to_str(text, apply_filepath_placeholder=False):
    """
    Apply all modules to df column.
    :param text: String to apply modules
    :param apply_filepath_placeholder: Flag indicating if we want to apply the filepath placeholder
    :return: dataframe with placeholders
    """
    if apply_filepath_placeholder:
        return replace_user_in_str(replace_sid_in_str(replace_guid_in_str(replace_hash_in_str(replace_filepath_in_str(text)))))
    else:
        return replace_user_in_str(replace_sid_in_str(replace_guid_in_str(replace_hash_in_str(text))))


def apply_modules_to_pd_series(pd_series, apply_filepath_placeholder=False):
    """
    Apply all modules to pd Series.
    :param pd_series: pandas Series
    :param apply_filepath_placeholder: Flag indicating if we want to apply the filepath placeholder
    :return: Series with placeholders
    """
    pd_series = pd_series.apply(lambda x: apply_modules_to_str(x, apply_filepath_placeholder))
    return pd_series


def apply_modules_to_df(df, column, apply_filepath_placeholder=False):
    """
    Apply all modules to df column.
    :param df: pandas DataFrame
    :param column: column to apply the operation on
    :param apply_filepath_placeholder: Flag indicating if we want to apply the filepath placeholder
    :return: dataframe with placeholders
    """
    df[column] = apply_modules_to_pd_series(df[column], apply_filepath_placeholder)
    return df


def process_dataframe(data: pd.DataFrame, column: str, n_lines, percentage, from_end: bool,
                      randomize: bool, apply_placeholder: bool, apply_filepath_placeholder: bool = False):
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
        data = apply_modules_to_df(data, column, apply_filepath_placeholder)

    return data
