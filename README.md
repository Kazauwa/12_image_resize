# Image Resizer

Script for image resizing

## Usage
```
python image_resize.py -i --input_file [-s --scale | -w --width -H --height] [-o --output]
```
This script requires path to the image to transform and at least one of the resizing parameters (scale, width/heigth or both). Be sure to specify either scale or width/height/both otherwise ValueError will be raised. If --output_file is provided then result is saved to specified location, otherwise it is saved next to the input.

## Parameters
`-i --input_file` - path to the image to transform

`-s --scale` - resize scale. Float, canb be less than 1.

`-w --width` - output image width. If provided without **heigth**, then it is being calculated in order to preserve aspect_ratio.

`-H --height` - output image height. If provided without **width**, then it is being calculated in order to preserve aspect_ratio.

`-o --otput_file` - path to for saving result. If not specified, saves result next to the input

## Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
