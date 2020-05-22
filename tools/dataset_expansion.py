import argparse
import os
import cv2
import numpy as np
import add_sys_path
from tools.generate_annotation import get_images
from local_utils.augmentation import DataAugmentor


def init_parse():
    parser = argparse.ArgumentParser(description="Script for dataset expansion.")
    parser.add_argument("-d", '--dataset_dir',
                        help="Dataset directory where images to read from and generated images will be written to ",
                        required=True, type=str)
    parser.add_argument("-a", "--annotation_file", help="annotation file name under Dataset dir.",
                        required=True, type=str)
    parser.add_argument("-spi", "--samples_per_image",
                        help="(Default 4) Number of images to generate from one input image. "
                             "Total generated images will be samples_per_image * total_input_images",
                        default=4,
                        type=int)
    return parser.parse_args()


def get_filename_from_path(fp):
    return os.path.splitext(os.path.basename(fp))[0]


if __name__ == "__main__":
    ARGS = init_parse()
    # images = get_images(ARGS.dataset_dir)
    augmentor = DataAugmentor(ARGS.samples_per_image, ARGS.dataset_dir)
    with open(ARGS.annotation_file, 'r+') as annotation_file:
        lines = annotation_file.readlines()
        annotation_file.write('\n')
        for annotation_line in lines:
            count = 0
            [image_fn, label_idx] = annotation_line.split(" ")
            image = cv2.imread(os.path.join(ARGS.dataset_dir, image_fn))
            image_gen = augmentor.generate_dataset(image)
            print("processing ...", image_fn)
            print("annotating line", annotation_line)
            for generated_image in image_gen:
                count += 1
                if count > ARGS.samples_per_image:
                    break
                if len(generated_image.shape) > 3:
                    generated_image = np.squeeze(generated_image, 0)
                gen_image_filename = 'augmented:{}-{}.jpg'.format(get_filename_from_path(image_fn), count)
                cv2.imwrite(os.path.join(ARGS.dataset_dir, gen_image_filename), generated_image)
                annotation_file.write('{} {}'.format(gen_image_filename, label_idx).strip('\n'))
