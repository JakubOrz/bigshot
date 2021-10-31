from PIL import Image
import numpy as np
import sys
import os
import time
from math import floor


def main():
    ysize = os.get_terminal_size().lines - 2
    xsize = min(os.get_terminal_size().columns - 2, floor(ysize*1.5))

    grey_scale = [x for x in " .:-=+*#%@"]
    result_table = list()

    with Image.open("resources/spamton-dancing") as img:
        keyFrames = img.n_frames
        for i in range(img.n_frames):
            img.seek(img.n_frames // keyFrames * i)
            img2: Image.Image = img
            img2 = img2.resize((xsize, ysize))
            pixel_array = np.array(img2.convert('L'))

            result_string: str = ""
            for row in pixel_array:
                for pixel in row:
                    result_string += grey_scale[floor(((256 - pixel) / 256) * 10)]
                result_string += "\n"
            result_table.append(result_string)

    while True:
        try:
            for frame in result_table:
                sys.stdout.write(frame)
                sys.stdout.flush()
                time.sleep(0.05)
                sys.stdout.write("\033[{}F".format(ysize))
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            sys.stdout.flush()
            return


if __name__ == '__main__':
    main()
