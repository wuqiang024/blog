#!usr/bin/env python
# -*- encoding:utf-8 -*-
import string
import random
import os
import uuid

from PIL import Image,ImageDraw,ImageColor,ImageFilter,ImageFont

class Code(object):
    def random_hexdigits(self,len=1):
        return random.sample(string.hexdigits,len)

    def punctuation(self,len=1):
        return tuple(random.sample(string.punctuation,len))

    def random_color(self,min=64,max=255):
        return tuple((random.randint(min,max) for i in range(3)))

    def create_code(self,width=80,height=24,color=(192,129,192)):
        image = Image.new('RGB',(width,height),color)
        draw = ImageDraw.Draw(image)
        self.fill_color(draw,image,10)
        self.fill_dischar()