"""
Script for generating annotation file from lexicon
"""

import os
import imghdr
import argparse

LEXICON_DIR = ""


def init_parse():
    """
    Parsing argument
    :return:
    """
    parser = argparse.ArgumentParser(
        description="Generate annotation file from lexicon file and image structure.")
    parser.add_argument("-imd", "--img_dir", help="Input image directory", type=str, required=True)
    parser.add_argument("-l", "--lexicon_file", help="Lexicon file path", type=str, required=True)
    parser.add_argument("-cf", "--continue_from",
                        help="(Default 1) - Lexicon line number to continue from"
                             " in annotation, this is useful when merging multiple lexicon files.",
                        type=int, default=1)
    parser.add_argument("-o", "--output_file", help="Output annotation file path",
                        type=str, required=True)
    return parser.parse_args()


def get_images(img_dir):
    """

    :param img_dir:
    :return:
    """
    files = []
    if os.path.isfile(img_dir):
        if imghdr.what(img_dir):
            files.append(img_dir)
        return files
    for root, sub_dir, dir_files in os.walk(img_dir):
        for img_file in dir_files:
            full_img_file = os.path.join(root, img_file)
            # print("img_file", img_file)
            if imghdr.what(full_img_file):
                files.append(img_file)
    return files


if __name__ == "__main__":
    ARGS = init_parse()
    # print(sorted(get_images(ARGS.img_dir)))
    with open(ARGS.lexicon_file, "r") as lexicon_file:
        with open(ARGS.output_file, "w") as output_file:
            lexicon_lines = lexicon_file.readlines()
            result_files = zip(range(ARGS.continue_from, len(lexicon_lines) + ARGS.continue_from),
                               sorted(get_images(ARGS.img_dir)))
            print("lexicon length", len(lexicon_lines), "images length", len(get_images(ARGS.img_dir)))
            if len(lexicon_lines) != len(get_images(ARGS.img_dir)):
                raise Exception("Lexicon Line number must be equal to image files number.")
            for lexicon_num, img_file in result_files:
                output_file.write('{} {}\n'.format(img_file, lexicon_num))
            print("annotation wrote in", ARGS.output_file)
