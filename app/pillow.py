#!usr/bin/env python
# -*- encoding:utf-8 -*-
import os
import random
from flask import Flask,send_from_directory
from PIL import Image,ImageFont,ImageDraw,ImageFilter

app = Flask(__name__)
app.debug = True

class Picture():
    def __init__(self):
        self.size = (240,60)
        self.mode = 'RGB'
        self.color = 'white'
        self.font = ImageFont.truetype(,36)

    def randChar(self):
        basic = '23456789abcdefghijklmnpqrstwxyzABCDEFGHIJKLMNPQRSTWXYZ'
        return basic[random.randint(0,len(basic)-1)]

    def randBdColor(self):
        return (random.randint(64,255),random.randint(64,255),random.randint(64,255))

    def randTextColor(self):
        return (random.randint(32,127),random.randint(32,127),random.randint(32,127))

    def proPicture(self):
        new_image = Image.new(self.mode,self.size,self.color)
        drawObject = ImageDraw.Draw(new_image)
        line_num = random.randint(4,6)
        for i in range(line_num):
            begin = (random.randint(0,self.size[0]),random.randint(0,self.size[1]))
            end = (random.randint(0,self.size[0]),random.randint(0,self.size[1]))
            drawObject.line([begin,end],self.randTextColor())

            for x in range(240):
                for y in range(60):
                    tmp = random.randint(0,50)
                    if tmp>30:
                        drawObject.point((x,y),self.randBdColor())

            randchar = ''
            for i in range(5):
                rand = self.randChar()
                randchar+=rand
                drawObject.text([50*i+10,10])
