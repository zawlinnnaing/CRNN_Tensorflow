import argparse
import os
import add_sys_path
from local_utils.establish_char_dict import CharDictBuilder


def init_argparse():
    parser = argparse.ArgumentParser(
        description="Genrate Character map and ordinal Number words from Character list"
    )
    parser.add_argument(
        "--charlist_file",
        "-csf",
        help="Character list file.",
        required=True,
        action="store",
        type=str,
    )
    parser.add_argument(
        "--save_output_path",
        "-op",
        help="Path for saving output files (char_dict and ord_map)",
        type=str,
        default="data/char_dict",
    )

    parser.add_argument(
        "--language",
        "-l",
        help="specifiy language for character dictionary.",
        type=str,
        default="mm",
    )

    return parser.parse_args()


if __name__ == "__main__":
    ARGS = init_argparse()
    CHAR_DICT_SAVE_PATH = os.path.join(
        ARGS.save_output_path, "char_dict_{}.json".format(ARGS.language)
    )
    ORD_MAP_SAVE_PATH = os.path.join(
        ARGS.save_output_path, "ord_map_{}.json".format(ARGS.language)
    )

    CharDictBuilder.write_char_dict(ARGS.charlist_file, CHAR_DICT_SAVE_PATH)
    CharDictBuilder.map_ord_to_index(ARGS.charlist_file, ORD_MAP_SAVE_PATH)
