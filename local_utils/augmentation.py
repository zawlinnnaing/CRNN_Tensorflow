import tensorflow as tf
import numpy as np


def augment_images(images, labels, images_path):
    # for every image in batch
    for i in range(0, images.shape[0]):
        images[i] = tf.keras.preprocessing.image.random_rotation(images[i], channel_axis=images[i].shape[-1],
                                                                 rg=40)
    print("from augmentation", images.shape)
    return images, labels, images_path


class DataAugmentor:
    def __init__(self, samples_per_image, output_dir):
        self._data_generator = tf.keras.preprocessing.image.ImageDataGenerator(rotation_range=15,
                                                                               brightness_range=(0.8, 2),
                                                                               shear_range=0.4,
                                                                               zoom_range=0.4)
        self._samples_per_image = samples_per_image
        self._output_dir = output_dir

    def generate_dataset(self, image):
        if len(image.shape) < 4:
            image = np.expand_dims(image, axis=0)
        image_gen = self._data_generator.flow(image, batch_size=1)
        return image_gen
