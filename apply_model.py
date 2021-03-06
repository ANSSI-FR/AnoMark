import argparse
from scripts.model_handler import MarkovModelHandler as mmh
from scripts.utils.data_handler import process_dataframe

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--data", required=True, help="Path of the data to work on (csv file)")
    parser.add_argument("-m", "--model", required=True, help="Path to the model to use")
    parser.add_argument("-c", "--column", required=True,
                        help="The column name on which we want to execute the model.")

    parser.add_argument("-s", "--store", action="store_true",
                        help="Store output in csv format in the results folder")
    parser.add_argument("--color", action="store_true", required=False,
                        help="Color the least likely letters in the output, according to the model")
    parser.add_argument("-n", "--nLines", default=50, required=False, help="The number of lines you want to display")
    parser.add_argument("--silent", required=False, action="store_true", help="Silent mode")
    parser.add_argument("--placeholder", required=False, action="store_true",
                        help="Apply GUID, SID, and username replacement by placeholder. See documentation for more "
                             "details about how it is performed")

    args = parser.parse_args()

    try:
        args.nLines = int(args.nLines)
    except ValueError:
        parser.error("nLines must be an int")
    mmh.run(model_path=args.model, data_path=args.data, store_bool=args.store, col_name=args.column,
            nb_lines=args.nLines, color_output=args.color, verbose=not args.silent, apply_placeholder=args.placeholder)
