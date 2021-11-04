import sys
import os
import getopt
import time
from math import floor

import numpy as np
from PIL import Image

result_table = list()


def find_closer(colors_dict: dict, hue):
    dist: dict = {c[1]: abs(hue - c[0]) for c in colors_dict.items()}
    return sorted(dist.items(), key=lambda x: x[1])[0][0]


def main(gif_source="resources/spamton-dancing", reverse_light=False,
         inColor=False, bigScale=False, ownColor=None, system='linux'):
    if system == "win32":
        ysize = 24
        xsize = min(os.get_terminal_size().columns - 2, floor(ysize * 1.5))
    else:
        ysize = os.get_terminal_size().lines - 2
        xsize = min(os.get_terminal_size().columns - 2, floor(ysize * 1.5))

    colors_dict = {
        0: "\u001b[31m",  # RED
        60: "\u001b[33m",
        120: "\u001b[32m",  # GREEN
        180: "\u001b[36m",
        240: "\u001b[34m",  # BLUE
        300: "\u001b[35m",
        360: "\u001b[31m",  # RED
    }
    if bigScale:
        grey_scale = [x for x in "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]]
    else:
        grey_scale = [x for x in " .:-=+*#%@"]
    with Image.open(gif_source) as img:
        keyFrames = img.n_frames
        for i in range(img.n_frames):
            img.seek(img.n_frames // keyFrames * i)
            img2: Image.Image = img
            img2 = img2.resize((xsize, ysize))

            pixel_array = np.array(img2.convert(mode='HSV' if inColor else 'L'))
            result_string = ""
            for row in pixel_array:
                for pixel in row:
                    if inColor:
                        hue, sat, lig = pixel
                        lig = 256 - lig if reverse_light else lig
                        letter = grey_scale[floor((lig / 257) * len(grey_scale))]
                        color = "\u001b[37;1m" if sat < 20 else find_closer(colors_dict, hue + 60)
                        result_string += color + letter
                    else:
                        lig = 256 - pixel if reverse_light else pixel
                        result_string += \
                            ownColor if ownColor is not None else '' + \
                                                                  grey_scale[floor((lig / 257) * len(grey_scale))]

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
    try:
        opts, args = getopt.getopt(sys.argv[1:], "cbf:hrg:",
                                   ["fill=", "bigscale=", "colorfull=", "help", "reverse=", "gif="])
    except getopt.GetoptError as ex1:
        sys.stdout.write(ex1.msg + "\n")
        sys.exit(2)
    bigscale = False
    reverse = False
    colors = False
    iswindows = False
    owncolor = None
    source = 'resources/spamton-dancing'
    for opt, arg in opts:
        if opt in ('-r', '--reverse'):
            reverse = True
        elif opt in ("-g", "--gif"):
            source = arg
        elif opt in ('-c', '--colorfull'):
            colors = True
        elif opt in ('-f', '--fill'):
            colorsdict = {
                "black": "\u001b[30m",
                "red": "\u001b[31m",
                "green": "\u001b[32m",
                "yellow": "\u001b[33m",
                "blue": "\u001b[34m",
                "magenta": "\u001b[35m",
                "cyan": "\u001b[36m",
                "white": "\u001b[37m"
            }
            colors = False
            sys.stdout.write(colorsdict.get(arg.lower(), "\u001b[0m"))
        elif opt in ('-b', '--bigscale'):
            bigscale = True
        elif opt in ('-h', '--help'):
            sys.stdout.write(f"Big [[SHOT]] czyli coś co pozwoli zmienić zwykłego gifa na animację w konsoli. "
                             f"Możesz popisać się jak bardzo jesteś pro z terminala, że umiesz animować ascii arty "
                             f"w konsoli, a potem wstawić to na TicToka na grupce dla script kiddies linuxa\n\n"
                             f"OPCJE\n"
                             f"-b --bigscale\n\tUżyj większej skali szarości, może zwiększyć czas ładowania animacji\n"
                             f"-c --colorfull\n\tPokoloruj animację na podstawie kolorów w gifie,"
                             f" nie zawsze ładnie wygląda\n"
                             f"-f --fill\n\tWypełnij gifa własnym kolorem wystarczy podać nazwę\n"
                             f"-g --gif\n\tWstaw scieżkę do własnego gifa który chcesz zanimować\n"
                             f"-r --reverse\n\tOdwraca kolory, dzięki czemu niektóre animacje wyglądają lepiej\n"
                             f"-h --help\n\tOtwiera instrukcję, którą właśnie czytasz\n\n")
            sys.exit(0)

    main(gif_source=source, reverse_light=reverse, inColor=colors, bigScale=bigscale, ownColor=owncolor,
         system=sys.platform)
