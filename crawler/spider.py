from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import re
from css_process.get_woff_Image import WoffAndImg
from css_process.get_num_from_img import NumInImg


class SpiderCatEye:

	def __init__(self, url):
		chrome_options = Options()
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--no-sandbox')
		self.__driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='chromedriver_win32/chromedriver.exe')
		self.__url = url

	def run(self):
		self.__driver.get(self.__url)
		self.__wait_time()
		self.__spider_page()
		self.__quit()

	def __spider_page(self):
		while True:
			dl = self.__driver.find_element_by_xpath('//div[@class="movies-list"]/dl[@class="movie-list"]')
			dds = dl.find_elements_by_xpath('//dd')
			for dd in dds:
				dd.click()
				time.sleep(2)
				_lastWindow = self.__driver.window_handles[-1]
				self.__driver.switch_to.window(_lastWindow)
				self.__get_info()
				self.__wait_time(timeNum=15)
				self.__driver.close()
				_lastWindow = self.__driver.window_handles[-1]
				self.__driver.switch_to.window(_lastWindow)
			self.__driver.find_element_by_link_text('下一页').click()


	def __get_info(self):
		woff_rule = r'//vfile\.meituan\.net/colorstone/.*?\.woff'
		woff_url = []
		woff_url = re.findall(woff_rule,self.__driver.page_source)
		if woff_url != []:
			url = 'http:' + woff_url[0]
			wai = WoffAndImg(url)
			imgdir = wai.get_imagedir()
			ni = NumInImg(imgdir)
			css_passwd = ni.run()

			title = self.__driver.find_element_by_xpath('//div[@class="movie-brief-container"]/h1[@class="name"]').text

			info_num = list(self.__driver.find_element_by_xpath('//div[@class="movie-index"]/div[@class="movie-index-content score normal-score"]/span').text)
			for index in range(len(info_num)):
				if info_num[index].lower() in [key for key in css_passwd]:
					info_num[index] = css_passwd[info_num[index].lower()]
			res_info_num = ''.join(info_num)

			
			if len(self.__driver.find_elements_by_xpath('//div[@class="movie-index"]/div[@class="movie-index-content score normal-score"]/div[@class="index-right"]/span[@class="score-num"]')) > 0:
				score_num = list(self.__driver.find_element_by_xpath('//div[@class="movie-index"]/div[@class="movie-index-content score normal-score"]/div[@class="index-right"]/span').text)
				for index in range(len(score_num)):
					if score_num[index].lower() in [key for key in css_passwd]:
						score_num[index] = css_passwd[score_num[index].lower()]
				res_score_num = ''.join(score_num)
			else:
				res_score_num = ''

			if len(self.__driver.find_elements_by_xpath('//div[@class="movie-index"]/div[@class="movie-index-content box"]/span[@class="no-info"]')) > 0:
				res_box_office = ''
			else:
				box_office = list(self.__driver.find_element_by_xpath('//div[@class="movie-index"]/div[@class="movie-index-content box"]/span[1]').text)
				box_office_unit = self.__driver.find_element_by_xpath('//div[@class="movie-index"]/div[@class="movie-index-content box"]/span[2]').text
				for index in range(len(box_office)):
					if box_office[index].lower() in [key for key in css_passwd]:
						box_office[index] = css_passwd[box_office[index].lower()]
				res_box_office = ''.join(box_office) + box_office_unit
			
			text = '{0}={1}={2}={3}\n'.format(title,res_info_num,res_score_num,res_box_office)
			with open('shuju.txt','a',encoding='utf-8') as f:
				f.write(text)
				f.close()


	def __wait_time(self, timeNum = 10):
		timeNum = random.randint(timeNum-5,timeNum+5)
		time.sleep(timeNum)

	def __quit(self):
		self.__driver.quit()