# !/usr/local/bin/python

import os
import common
import random
import threading
from PIL import Image, ImageDraw, ImageFont
import string
import hashlib


def change_assets_md5(path):
    os.chdir(path)
    all_files = []
    common.get_all_files(path, all_files, "*")
    for filePath in all_files:
        filename = os.path.splitext(filePath)[1]
        if filename.lower().endswith(".png") or filename.lower().endswith(".ogg"):
            content = open(filePath, "rb").read()
            with open(filePath, "wb") as fi:
                fi.write(content + random.choice(["\@", "\!", "\#", "\%", "\&"]))


def random_color():
    return (random.randint(60, 255), random.randint(60, 255), random.randint(60, 255))


def _add_image_thread(folderPath):
    text = random.sample(string.uppercase, random.randint(10, 26))
    sizex = random.choice([32, 64, 128, 256])
    sizey = random.choice([32, 64, 128, 256])
    im = Image.new("RGB", (sizex, sizey), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    for x in range(sizex):
        for y in range(sizey):
            dr.point((x, y), fill=random_color())
    font = ImageFont.truetype(os.path.join("fonts", "/System/Library/Fonts/Helvetica.ttc"), 18)
    text_width, text_height = dr.textsize("A", font=font)
    for char in text:
        x = random.randint(0, sizex - text_width)
        y = random.randint(0, sizey - text_height)
        dr.text((x, y), char, font=font, fill="yellow")
    # dr.text((10, 5), text, font=font, fill="#000000")
    # im.show()
    md5 = hashlib.md5()
    md5.update(folderPath + "".join(text) + os.times()[4].__str__())
    filepath = os.path.join(folderPath, md5.hexdigest() + ".png")
    # print "save filepath %s " % filepath
    im.save(filepath)
    print "add image thread complete", filepath


def add_image(rootFolder):
    print "add images"
    # os.chdir(rootFolder)
    folders = common.get_all_dirs(rootFolder)
    for folder in folders:
        abspath = os.path.abspath(folder)
        count = random.randint(5, 20)
        for i in range(count):
            t = threading.Thread(target=_add_image_thread(abspath))
            t.start()
            t.join()


if __name__ == "__main__":
    path = "/Users/kaifa/SharpKnife/WorkSpace/UnityProjects/majia_origin_Mix_09-26_18-53/Assets/Res"
    dirArray = common.get_all_dirs(path)
    for dirpath in dirArray:
        print dirpath

    # add_image("/Users/kaifa/SharpKnife/WorkSpace/imageaddtest")
