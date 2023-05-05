#!/usr/bin/env python3
# -- coding utf-8 --
# @Author：Cra5h
# GPT-OCR-OCR result view

import pytesseract
from PIL import Image

def test_ocr():
    image_path = input("请输入图片路径：")
    text = pytesseract.image_to_string(Image.open(image_path))
    print(text)

test_ocr()

