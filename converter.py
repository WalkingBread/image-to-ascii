from PIL import Image
from numpy import asarray, ndarray
import argparse

def scale_image(image, scale):
    width, height = image.size

    new_width = int(width * scale)
    new_height = int(height * scale)

    resized = image.resize((new_width, new_height), Image.ANTIALIAS)
    return resized

class Converter:
    def __init__(self, symbol_set):
        self.symbol_set = symbol_set
        self.brightness_level = self.assign_brightness_levels()

    def get_brightness(self, pixel_data):
        if type(pixel_data) == ndarray and len(pixel_data) == 3:
            r = pixel_data[0]
            g = pixel_data[1]
            b = pixel_data[2]
            brightness = 255 - (r + g + b) / 3
            return int(brightness)

        brightness = 255 - pixel_data
        return brightness

    def assign_brightness_levels(self):
        brightness_level = {}

        interval = 256 / len(self.symbol_set)
        for x in range(0, len(self.symbol_set)):
            s = self.symbol_set[x]
        
            lower_threshold = int(x * interval)
            upper_threshold = int(lower_threshold + interval)

            if upper_threshold == 255:
                upper_threshold = 256

            _range = range(lower_threshold, upper_threshold)
            brightness_level[_range] = s

        return brightness_level

    def convert(self, scale, input_path, output_path):
        image = Image.open(input_path, 'r')
        image = scale_image(image, scale)

        pix_arr = asarray(image)

        art = self.get_ascii_art(pix_arr)
        print(art)
        
        if output_path != None:
            f = open(output_path, 'w')
            f.write(art)
            f.close()

    def get_ascii_art(self, pixel_array):
        art = ''
        for y in range(0, len(pixel_array)):
            for x in range(0, len(pixel_array[0])):
                pixel = pixel_array[y][x]
                brightness = self.get_brightness(pixel)

                for level in self.brightness_level:
                    if brightness in level:
                        art += self.brightness_level[level] + ' '
            art += ' \n'
        return art


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('scale', help='art scale in comparison to image', type=float)
    parser.add_argument('input_path', help='path of the input image', type=str)
    parser.add_argument('--out', help='path of txt where the ascii art will be saved', type=str)
    parser.add_argument('--set', help='set of symbols converter uses to create art', type=str)
    args = parser.parse_args()

    output_path = None
    symbol_set = ' .`,-=+:;#%&@"'
    if args.out:
        output_path = args.out
    if args.set:
        symbol_set = args.set

    Converter(symbol_set).convert(args.scale, args.input_path, output_path)