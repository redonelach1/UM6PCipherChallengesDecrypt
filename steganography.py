import argparse

from PIL import Image


class Steganography:

    BLACK_PIXEL = (0, 0, 0)

    def _int_to_bin(self, rgb):
        """Convert an integer tuple to a binary (string) tuple.

        :param rgb: An integer tuple like (220, 110, 96)
        :return: A string tuple like ("00101010", "11101011", "00010110")
        """
        r, g, b = rgb
        # format (x, '08b') returns x as 8 bits with leading zeros
        return format(r, '08b'), format(g, '08b'), format(b, '08b')

    def _bin_to_int(self, rgb):
        """Convert a binary (string) tuple to an integer tuple.

        :param rgb: A string tuple like ("00101010", "11101011", "00010110")
        :return: Return an int tuple like (220, 110, 96)
        """
        r, g, b = rgb
        # int(x, 2) converts the binary x to a decimal integer
        return int(r, 2), int(g, 2), int(b, 2)

    def _merge_rgb(self, rgb1, rgb2):
        """Merge two RGB tuples.

        :param rgb1: An integer tuple like (220, 110, 96)
        :param rgb2: An integer tuple like (240, 95, 105)
        :return: An integer tuple with the two RGB values merged.
        """
        r1, g1, b1 = self._int_to_bin(rgb1)
        r2, g2, b2 = self._int_to_bin(rgb2)
        # x[:6]+y[:2] concatenates the first 6 characters of x with the first 2 characters of y
        rgb = r1[:6] + r2[:2], g1[:6] + g2[:2], b1[:6] + b2[:2]
        return self._bin_to_int(rgb)

    def merge(self, image1, image2):
        """Merge image2 into image1.

        :param image1: First image
        :param image2: Second image
        :return: A new merged image.
        """
        # Check the images dimensions
        if image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]:
            raise ValueError('Image 2 should be smaller than Image 1!')

        # Get the pixel map of the two images
        map1 = image1.load()
        map2 = image2.load()

        new_image = Image.new(image1.mode, image1.size)
        new_map = new_image.load()

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                is_valid = lambda: i < image2.size[0] and j < image2.size[1]
                rgb1 = map1[i ,j]
                rgb2 = map2[i, j] if is_valid() else self.BLACK_PIXEL
                new_map[i, j] = self._merge_rgb(rgb1, rgb2)

        return new_image

    def _unmerge_rgb(self, rgb):
        """Unmerge RGB.

        :param rgb: An integer tuple like (220, 110, 96)
        :return: An integer tuple with the two RGB values merged.
        """
        r,g,b = self._int_to_bin(rgb)
        
        tail = "000000"

        r1 = r[-2:] + tail
        g1 = g[-2:] + tail
        b1 = b[-2:] + tail

        return self._bin_to_int((r1,g1,b1))

    def unmerge(self, image):
        """Unmerge an image.

        :param image: The input image.
        :return: The unmerged/extracted image.
        """
        # Get the pixel map of the two images
        map = image.load()

        new_image = Image.new(image.mode, image.size)
        new_map = new_image.load()

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                rgb = map[i, j]
                new_map[i, j] = self._unmerge_rgb(rgb)

        print(new_map)
        return new_image  

def main():
    parser = argparse.ArgumentParser(description='Steganography')
    subparser = parser.add_subparsers(dest='command')

    merge = subparser.add_parser('merge')
    merge.add_argument('--image1', required=True, help='Image1 path')
    merge.add_argument('--image2', required=True, help='Image2 path')
    merge.add_argument('--output', required=True, help='Output path')

    unmerge = subparser.add_parser('unmerge')
    unmerge.add_argument('--image', required=True, help='Image path')
    unmerge.add_argument('--output', required=True, help='Output path')

    args = parser.parse_args()

    if args.command == 'merge':
        image1 = Image.open(args.image1)
        image2 = Image.open(args.image2)
        Steganography().merge(image1, image2).save(args.output)
    elif args.command == 'unmerge':
        image = Image.open(args.image)
        Steganography().unmerge(image).save(args.output)


if __name__ == '__main__':
    main()

