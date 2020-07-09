import requests
import os
from fontTools.ttLib import TTFont
from fontTools import ttLib
from fontTools.pens.basePen import BasePen
from reportlab.graphics.shapes import Path
from reportlab.lib import colors
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Group, Drawing, scale
 
class ReportLabPen(BasePen):
 
    """A pen for drawing onto a reportlab.graphics.shapes.Path object."""
 
    def __init__(self, glyphSet, path=None):
        BasePen.__init__(self, glyphSet)
        if path is None:
            path = Path()
        self.path = path
 
    def _moveTo(self, p):
        (x,y) = p
        self.path.moveTo(x,y)
 
    def _lineTo(self, p):
        (x,y) = p
        self.path.lineTo(x,y)
 
    def _curveToOne(self, p1, p2, p3):
        (x1,y1) = p1
        (x2,y2) = p2
        (x3,y3) = p3
        self.path.curveTo(x1, y1, x2, y2, x3, y3)
 
    def _closePath(self):
        self.path.closePath()
 

class WoffAndImg:

    def __init__(self, url):
        self.__url = url
        self.__create_path()
        self.__get_woff()
        self.__woffToImage()



    def __create_path(self):
        name = self.__url.split('/')[-1]
        filedir = 'woff_img/'+ name.replace('.woff','')
        if not os.path.exists(filedir):
            os.mkdir(filedir)
        self.__woffPath = filedir + '/' + name
        imagespath = filedir + '/images'
        if not os.path.exists(imagespath):
            os.mkdir(imagespath)
        self.__imgPath = imagespath + '/'

    def get_imagedir(self):
        return self.__imgPath

    def __get_woff(self):
        text = requests.get(self.__url).content
        with open(self.__woffPath,'wb') as f:
            f.write(text)
            f.close()

    def __woffToImage(self,fmt="png"):
        font = TTFont(self.__woffPath)
        gs = font.getGlyphSet()
        glyphNames = font.getGlyphNames()
        glyphNames.remove('glyph00000')
        glyphNames.remove('x')

        for i in glyphNames:
            if i[0] == '.':#跳过'.notdef', '.null'
                continue
            
            g = gs[i]
            pen = ReportLabPen(gs, Path(fillColor=colors.black, strokeWidth=1))
            g.draw(pen)
            w, h = g.width, g.width
            g = Group(pen.path)
            g.translate(w, h*1.5)
            
            d = Drawing(w*3, h*4.5)
            d.add(g)
            imageFile = self.__imgPath+"/"+i+".png"
            renderPM.drawToFile(d, imageFile, fmt)

if __name__ == "__main__":
    url = 'http://vfile.meituan.net/colorstone/dfba174e6f8d42a8bd26ee39cafcd6df2276.woff'
    test = WoffAndImg(url)
    print(test.get_imagedir())