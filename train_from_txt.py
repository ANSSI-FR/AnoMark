import argparse
import pickle

from anomark.model_handler import MarkovModelHandler as mmh
from anomark.utils.data_handler import apply_modules_to_str

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--data", required=True,
                        help="Path of the TXT data to work on")
    parser.add_argument("-o", "--order", required=True,
                        help="Model's order, which is the number of letters for the window")

    parser.add_argument("--output", required=False,
                        help="The path of the output for the new model")
    parser.add_argument("--placeholder", action="store_true", required=False,
                        help="Apply GUID, SID, username, and hash replacement by placeholder. See documentation for more "
                             "details about how it is performed")
    parser.add_argument("--filepath-placeholder", action="store_true", required=False,
                        help="Apply filepath replacement by placeholder. See documentation for more "
                             "details about how it is performed. This is a separate because you may want other placeholders applied but not this one.")

    parser.add_argument("--resume", action="store_true", help="Continue training mode for the model")
    parser.add_argument("-m", "--model", help="Path to the model to use (continue training mode)")

    args = parser.parse_args()

    if args.data is None:
        parser.error('The --train mode requires --data to train on')
    with open(args.data) as f:
        data = f.read()

    if args.placeholder:
        print("Applying placeholder transformation...")
        data = apply_modules_to_str(text=data, apply_filepath_placeholder=args.filepath_placeholder)

    if args.resume:
        if args.model is None:
            parser.error("You did not provide model path with --model")
        with open(args.model, "rb") as f:
            model = pickle.load(f)
        mmh.train_from_txt(training_data=data, model_order=model.order, save_path=args.output, model=model)
    else:
        if args.order is None:
            parser.error("You did not provide the model's --order")
        try:
            args.order = int(args.order)
        except ValueError:
            parser.error("Order must be an int")
        mmh.train_from_txt(training_data=data, model_order=args.order, save_path=args.output, model=None)
