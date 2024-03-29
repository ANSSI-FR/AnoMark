import argparse

from anomark.model_handler import MarkovModelHandler as mmh

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--data", required=True, help="Path of the data to work on (csv file)")
    parser.add_argument("-m", "--model", required=True, help="Path to the model to use")
    parser.add_argument("-c", "--column", required=True,
                        help="The column name on which we want to execute the model.")

    # These two options, "store" and "output" should be used exclusively of one another
    parser.add_argument("-s", "--store", required=False, action="store_true",
                        help="Store output in csv format in the results folder")
    parser.add_argument("-o", "--output", required=False, help="Path to file where output in csv format will be stored")

    parser.add_argument("--color", action="store_true", required=False,
                        help="Color the least likely letters in the output, according to the model")
    parser.add_argument("-n", "--nLines", default=50, required=False, help="The number of lines you want to display")
    parser.add_argument("--silent", required=False, action="store_true", help="Silent mode")
    parser.add_argument("--placeholder", action="store_true", required=False,
                        help="Apply GUID, SID, username, and hash replacement by placeholder. See documentation for more "
                             "details about how it is performed")
    parser.add_argument("--filepath-placeholder", action="store_true", required=False,
                        help="Apply filepath replacement by placeholder. See documentation for more "
                             "details about how it is performed. This is a separate because you may want other placeholders applied but not this one.")
    parser.add_argument("--show-percentage", required=False, action="store_true",
                        help="Add human-readable percentage to reflect proximity of Markov score to threshold where threshold is the expected value.")

    args = parser.parse_args()

    try:
        args.nLines = int(args.nLines)
    except ValueError:
        parser.error("nLines must be an int")

    if args.store and args.output:
        parser.error("'--store' and '--output' flags cannot be used at the same time.")

    mmh.run(
        model_path=args.model, data_path=args.data, col_name=args.column, store_bool=args.store, output=args.output,
        nb_lines=args.nLines, color_output=args.color, verbose=not args.silent, apply_placeholder=args.placeholder,
        show_percentage=args.show_percentage
    )
