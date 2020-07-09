from css_process.get_num_from_img import NumInImg
from crawler.spider import SpiderCatEye


if __name__ == "__main__":
    # ni = NumInImg('woff_img/1f5afa166addf8007dc429d9cd72ad4b2276/images/')
    # print(ni.run())
    sc = SpiderCatEye('https://maoyan.com/films?showType=3&sortId=3&offset=0')
    sc.run()