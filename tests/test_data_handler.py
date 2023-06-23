from unittest import TestCase

import pandas as pd

from scripts.utils.data_handler import process_dataframe, replace_guid_in_str, replace_sid_in_str, replace_user_in_str


class Test(TestCase):
    def test_replace_sid_in_str(self):
        str1 = "my_S-1-0-0"
        res1 = replace_sid_in_str(some_string=str1)
        expected_res1 = "my_<SID>"

        str2 = "other SID here: S-1-5-21-4242424242-424242-4242442-4242 should be replaced"
        res2 = replace_sid_in_str(some_string=str2, placeholder="<placeholder>")
        expected_res2 = "other SID here: <placeholder> should be replaced"

        str3 = "not an SID: S-1-1 should not be replaced"
        res3 = replace_sid_in_str(some_string=str3)
        expected_res3 = str3

        self.assertEqual(expected_res1, res1)
        self.assertEqual(expected_res2, res2)
        self.assertEqual(expected_res3, res3)

    def test_replace_user_in_str(self):
        str1 = r"C:\Users\some_user\some_folder"
        res1 = replace_user_in_str(some_string=str1)
        expected_res1 = r"C:\Users\<USER>\some_folder"

        str2 = r"C:\ProgramFiles\some_program\some_folder"
        res2 = replace_user_in_str(some_string=str2, placeholder="<placeholder>")
        expected_res2 = str2

        str3 = r"C:\Users\some_user\some_folder"
        res3 = replace_user_in_str(some_string=str3, placeholder="<OTHER_PLACEDHOLDER>")
        expected_res3 = r"C:\Users\<OTHER_PLACEDHOLDER>\some_folder"

        # Lowercase path test
        str4 = r"c:\users\some_user\some_folder"
        res4 = replace_user_in_str(some_string=str4)
        expected_res4 = r"c:\users\<USER>\some_folder"

        self.assertEqual(expected_res1, res1)
        self.assertEqual(expected_res2, res2)
        self.assertEqual(expected_res3, res3)
        self.assertEqual(expected_res4, res4)

    def test_replace_guid_in_str(self):
        str1 = r"Here is some {12345678-1234-1234-1234-123456789012}"
        res1 = replace_guid_in_str(some_string=str1)
        expected_res1 = r"Here is some <GUID>"

        str2 = r"Other {12345678-1234-1234-1234-123456789012} here"
        res2 = replace_guid_in_str(some_string=str2, placeholder="placeholder")
        expected_res2 = "Other placeholder here"

        str3 = r"Not a guid: {12345678}-{1234}-{1234}-{1234}-{1234}"
        res3 = replace_guid_in_str(some_string=str3)
        expected_res3 = str3

        self.assertEqual(expected_res1, res1)
        self.assertEqual(expected_res2, res2)
        self.assertEqual(expected_res3, res3)

    def test_process_dataframe(self):
        df = pd.DataFrame({"col1": ["Data", "Some SID: {12345678-1234-1234-1234-123456789012}",
                                    "Other line", r"Some process path C:\Users\some_user\some_folder"],
                           "col2": [1, 3, 2, 10]})

        res1 = process_dataframe(df.copy(), column="col1", n_lines=None, percentage=None, from_end=False,
                                 randomize=False, apply_placeholder=True)
        expected_res1 = pd.DataFrame({'col1': ["Data", "Some SID: <GUID>", "Other line",
                                               r"Some process path C:\Users\<USER>\some_folder"],
                                      "col2": [1, 3, 2, 10]})

        res2 = process_dataframe(df.copy(), column="col1", n_lines=2, percentage=None, from_end=False,
                                 randomize=False, apply_placeholder=True)
        expected_res2 = pd.DataFrame({'col1': ["Data", "Some SID: <GUID>"],
                                      "col2": [1, 3]})

        res3 = process_dataframe(df.copy(), column="col1", n_lines=None, percentage=50, from_end=True,
                                 randomize=False, apply_placeholder=True).reset_index(drop=True)
        expected_res3 = pd.DataFrame({'col1': ["Other line", r"Some process path C:\Users\<USER>\some_folder"],
                                      "col2": [2, 10]})

        self.assertEqual(expected_res1.to_dict(), res1.to_dict())
        self.assertEqual(expected_res2.to_dict(), res2.to_dict())
        self.assertEqual(expected_res3.to_dict(), res3.to_dict())
