import os
from argparse import ArgumentParser
from PIL import Image


def scale(image, **kwargs):
    width, height = image.size
    scale = kwargs.get('scale')
    new_size = int(width * scale), int(height * scale)
    image = image.resize(new_size, resample=Image.LANCZOS)
    return image


def linear(image, **kwargs):
    new_size = kwargs.get('width'), kwargs.get('height')
    image = image.resize(new_size, resample=Image.LANCZOS)
    return image


def adjusted_height(image, **kwargs):
    aspect_ratio = get_aspect_ratio(image.size)
    width = kwargs.get('width')
    height = int(width / aspect_ratio)
    new_size = width, height
    image = image.resize(new_size, resample=Image.LANCZOS)
    return image


def adjusted_width(image, **kwargs):
    aspect_ratio = get_aspect_ratio(image.size)
    height = kwargs.get('height')
    width = int(height / aspect_ratio)
    new_size = width, height
    image = image.resize(new_size, resample=Image.LANCZOS)
    return image


def manage_resize_method(options):
    if options.scale and (options.width or options.height):
        raise ValueError('Either scale or width/height must be specified!')
    elif options.scale:
        return 'SCALE'
    elif options.width and options.height:
        return 'LINEAR'
    elif options.width and not options.height:
        return 'ADJUSTED_HEIGHT'
    elif options.height and not options.width:
        return 'ADJUSTED_WIDTH'
    else:
        raise ValueError('Scale or width/height must be specified')


RESIZE_METHODS = {
    'SCALE': scale,
    'LINEAR': linear,
    'ADJUSTED_HEIGHT': adjusted_height,
    'ADJUSTED_WIDTH': adjusted_width
}


def get_aspect_ratio(size):
    width, height = size
    return round(width / height, 2)


def is_aspect_ratio_saved(original_size, new_size):
    return get_aspect_ratio(original_size) == get_aspect_ratio(new_size)


def create_filename(path_to_original, size):
    path, filename = os.path.split(path_to_original)
    filename = '{0}x{1}__{2}'.format(*size, filename)
    return os.path.join(path, filename)


def resize_image(resize_method, options):
    path_to_original = options.input_file
    path_to_result = options.output_file
    original = Image.open(path_to_original)
    transformed = original.copy()
    transformed = resize_method(transformed, **vars(options))

    if not is_aspect_ratio_saved(original.size, transformed.size):
        print('\nWarning! Current transformation will not preserve original aspect ratio!\n')

    if not path_to_result:
        path_to_result = create_filename(path_to_original, transformed.size)
    transformed.save(path_to_result)


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

    resize_method = RESIZE_METHODS[manage_resize_method(options)]
    resize_image(resize_method, options)
