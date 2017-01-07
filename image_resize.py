import os
from argparse import ArgumentParser
from PIL import Image


def scale(image, **kwargs):
    width, height = image.size
    scale = kwargs.get('scale')
    return int(width * scale), int(height * scale)


def linear(image, **kwargs):
    return kwargs.get('width'), kwargs.get('height')


def adjusted_height(image, **kwargs):
    aspect_ratio = get_aspect_ratio(image.size)
    width = kwargs.get('width')
    height = int(width / aspect_ratio)
    return width, height


def adjusted_width(image, **kwargs):
    aspect_ratio = get_aspect_ratio(image.size)
    height = kwargs.get('height')
    width = int(height / aspect_ratio)
    return width, height


def get_resize_method(options):
    if options.scale and (options.width or options.height):
        raise ValueError('Either scale or width/height must be specified!')
    elif options.scale:
        return scale
    elif options.width and options.height:
        return linear
    elif options.width and not options.height:
        return adjusted_height
    elif options.height and not options.width:
        return adjusted_width
    else:
        raise ValueError('Scale or width/height must be specified')


def get_aspect_ratio(image_size):
    width, height = image_size
    return round(width / height, 2)


def is_aspect_ratio_saved(original_size, new_size):
    return get_aspect_ratio(original_size) == get_aspect_ratio(new_size)


def create_filename(path_to_original, image_size):
    path, filename = os.path.split(path_to_original)
    filename = '{0}x{1}__{2}'.format(*image_size, filename)
    return os.path.join(path, filename)


def resize_image(resize_method, options):
    path_to_original = options.input_file
    path_to_result = options.output_file
    original_image = Image.open(path_to_original)
    new_size = resize_method(original_image, **vars(options))
    transformed_image = original_image.resize(new_size, resample=Image.LANCZOS)

    if not is_aspect_ratio_saved(original_image.size, transformed_image.size):
        print('\nWARNING! Current transformation will not preserve original_image aspect ratio!\n')

    if not path_to_result:
        path_to_result = create_filename(path_to_original, transformed_image.size)
    transformed_image.save(path_to_result)


if __name__ == '__main__':
    parser = ArgumentParser(description='Resize images by width, height, both or scale')
    parser.add_argument('-i', '--input_file', type=str, nargs='?', required=True, dest='input_file',
                        help='Path to the image to resize')
    parser.add_argument('-w', '--width', type=int, nargs='?',
                        help='Output image width')
    parser.add_argument('-H', '--height', type=int, nargs='?',
                        help='Output image height')
    parser.add_argument('-s', '--scale', type=float, nargs='?',
                        help='Output image scale normed to 1')
    parser.add_argument('-o', '--output_file', type=str, nargs='?', default=None,
                        help='Output image destination')

    options = parser.parse_args()

    resize_method = get_resize_method(options)
    resize_image(resize_method, options)
