import os
from PIL import Image
import pytesseract
import re

class NumInImg:

    def __init__(self, imgPath):
        self.__imgPath = imgPath

    def run(self):
        result_dit = {}
        img_dit = self.__get_imgList()
        for img in img_dit:
            temp_img = chr(eval(img.replace('uni','0x').lower()))
            result_dit[temp_img] = self.__recognize(img_dit[img])
        text = str(result_dit)
        txt_path = self.__imgPath.replace('images/','dict.txt')
        with open(txt_path,'w',encoding='utf-8') as f:
            f.write(text)
            f.close()
        return result_dit

    def __get_imgList(self):
        img_dit = {}
        for root, dirs, files in os.walk(self.__imgPath):
            for file in files:
                # print(file.split('.'))
                img_dit[file.split('.')[0]] = root + file
        return img_dit

    def __recognize(self, path):
        image = Image.open(path)
        image = image.resize((800,1200))
        text = pytesseract.image_to_string(image, lang='eng', config='--psm 9 --oem 8 -c tessedit_char_whitelist=0123456789')
        
        return text


if __name__ == "__main__":
    ni = NumInImg('woff_img/dfba174e6f8d42a8bd26ee39cafcd6df2276/images/')
    print(ni.run())