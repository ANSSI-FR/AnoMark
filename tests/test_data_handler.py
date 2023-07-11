from unittest import TestCase

import pandas as pd
from anomark.utils.data_handler import (
    process_dataframe,
    replace_guid_in_str,
    replace_hash_in_str,
    replace_sid_in_str,
    replace_user_in_str,
)


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

        # Multiple user placeholders in one line
        str5 = r"c:\users\some_user\some_folder\some_file.exe c:\users\some_user\some_folder\some_file.txt"
        res5 = replace_user_in_str(some_string=str5)
        expected_res5 = r"c:\users\<USER>\some_folder\some_file.exe c:\users\<USER>\some_folder\some_file.txt"

        self.assertEqual(expected_res1, res1)
        self.assertEqual(expected_res2, res2)
        self.assertEqual(expected_res3, res3)
        self.assertEqual(expected_res4, res4)
        self.assertEqual(expected_res5, res5)

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

    def test_replace_hash_in_str(self):
        # SHA256
        str1 = r"Here is some e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        res1 = replace_hash_in_str(some_string=str1)
        expected_res1 = r"Here is some <HASH>"

        # SHA1
        str2 = r"Here is some da39a3ee5e6b4b0d3255bfef95601890afd80709"
        res2 = replace_hash_in_str(some_string=str2)
        expected_res2 = r"Here is some <HASH>"

        # MD5
        str3 = r"Here is some d41d8cd98f00b204e9800998ecf8427e"
        res3 = replace_hash_in_str(some_string=str3)
        expected_res3 = r"Here is some <HASH>"

        # Common truncation of hash in file name
        str4 = r"Here is some d41d8cd98f00b204e980"
        res4 = replace_hash_in_str(some_string=str4)
        expected_res4 = r"Here is some <HASH>"

        str5 = r"Other e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 here"
        res5 = replace_hash_in_str(some_string=str5, placeholder="placeholder")
        expected_res5 = "Other placeholder here"

        str6 = r"Not a hash: d41d8cd98f00b204e9800998ecf84"
        res6 = replace_hash_in_str(some_string=str6)
        expected_res6 = str6

        # Multiple SHA256 placeholders in one line
        str7 = r"c:\users\some_user\some_folder\e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.exe c:\users\some_user\some_folder\e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.txt"
        res7 = replace_hash_in_str(some_string=str7)
        expected_res7 = r"c:\users\some_user\some_folder\<HASH>.exe c:\users\some_user\some_folder\<HASH>.txt"

        self.assertEqual(expected_res1, res1)
        self.assertEqual(expected_res2, res2)
        self.assertEqual(expected_res3, res3)
        self.assertEqual(expected_res4, res4)
        self.assertEqual(expected_res5, res5)
        self.assertEqual(expected_res6, res6)
        self.assertEqual(expected_res7, res7)

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
