import argparse
import pickle

from anomark.model_handler import MarkovModelHandler as mmh
from anomark.utils.data_handler import process_dataframe

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--data", required=True,
                        help="Path of the CSV data to work on")
    parser.add_argument("-c", "--column", required=True,
                        help="Name of the column in dataframe")
    parser.add_argument("-o", "--order", required=True,
                        help="Model's order, which is the number of letters for the window")
    parser.add_argument("-cc", "--count-column", help="Count column name (only if it exists)")
    parser.add_argument("--output", required=False,
                        help="The path of the output for the new model")

    parser.add_argument("-n", "--nLines", required=False,
                        help="The number of lines you want to take from csv")
    parser.add_argument("-p", "--percentage", required=False,
                        help="The number of lines you want to take in percent")
    parser.add_argument("--fromEnd", required=False, action="store_true",
                        help="Slice nLines from the end of dataset")
    parser.add_argument("-r", "--randomize", required=False, action="store_true",
                        help="Randomize selection for line selection")
    parser.add_argument("--placeholder", action="store_true", required=False,
                        help="Apply GUID, SID, username, and hash replacement by placeholder. See documentation for more "
                             "details about how it is performed")
    parser.add_argument("--filepath-placeholder", action="store_true", required=False,
                        help="Apply filepath replacement by placeholder. See documentation for more "
                             "details about how it is performed. This is a separate because you may want other placeholders applied but not this one.")

    parser.add_argument("--resume", action="store_true", help="Continue training mode for the model")
    parser.add_argument("-m", "--model", help="Path to the model to use (resume training mode)")

    args = parser.parse_args()

    data = mmh.load_data(path=args.data, col_name=args.column)
    data = process_dataframe(data=data, column=args.column, n_lines=args.nLines, percentage=args.percentage,
                             from_end=args.fromEnd, randomize=args.randomize, apply_placeholder=args.placeholder, apply_filepath_placeholder=args.filepath_placeholder)

    print("Training on data...")

    if args.resume:
        if args.model is None:
            parser.error("You did not provide model path with --model")
        with open(args.model, "rb") as f:
            model = pickle.load(f)
        mmh.train_from_df(df=data, model_order=model.order, train_col_name=args.column,
                          count_col_name=args.count_column, save_model=True, save_path=args.output, model=model)
    else:
        try:
            args.order = int(args.order)
        except ValueError:
            parser.error("Order must be an int")
        mmh.train_from_df(df=data, model_order=args.order, train_col_name=args.column,
                          count_col_name=args.count_column, save_model=True, save_path=args.output)
